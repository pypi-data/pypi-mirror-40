import rlagent
import numpy as np
import tensorflow as tf
import time
from mpi4py import MPI
import sys

class NStepMPIAgent(rlagent.Agent):
    def __init__(self, agent=None, env=None, save_steps=5000, model_dir='model', dtype=tf.float32):
        super(NStepMPIAgent, self).__init__(agent=agent, env=env,
                                             save_steps=save_steps,
                                             model_dir=model_dir,  dtype=dtype)
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
        self.dtype = dtype

        self.state_recvbuf = np.zeros((self.size,) + self.agent.state_shape, dtype=np.float32)
        self.action_recvbuf = np.zeros(self.agent.action_shape, dtype=np.float32)
        self.value_recvbuf = np.zeros((1,1), dtype=np.float32)
        self.target_value_recvbuf = np.zeros((self.size*self.agent.t_max,1), dtype=np.float32)
        self.gathered_action = None
        self.gathered_value = None

        if self.rank == 0:
            self.initialize_root()


    def initialize_root(self):
        #placeholders
        state_input = tf.placeholder(self.dtype, (None,) + self.agent.state_shape, name='state_input')
        action_input = tf.placeholder(self.dtype, (None,) + self.agent.action_shape, name='action_input')
        target_value_input = tf.placeholder(self.dtype, (None,1), name='target_value_input')

        #placeholder to keras input
        state_input_keras = tf.keras.Input(tensor=state_input)
        action_input_keras = tf.keras.Input(tensor=action_input)
        self.inputs = {'state':state_input_keras,
                       'action':action_input_keras,
                       'target_value':target_value_input}

        #config variables
        outputs = self.agent(self.inputs)
        self.outputs = self.agent.convert_output_list_to_dict(outputs)

        #set loss, train ops
        self.agent.set_losses(self.inputs, self.outputs)
        self.losses = self.agent.losses_dict
        self.global_step = tf.train.get_or_create_global_step()
        self.train_ops = self.agent.get_train_ops(self.global_step)

        self.train_summary_op = self.set_summary_ops_per_train()

        self.saver = tf.train.Saver()
        self.local_model_saver = tf.train.Saver(tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES,
                                                                  scope=self.agent.local_model.name))

    def reset_episode_vars(self):
        if self.done == True and self.rank == 0:
            self.ep_num, ep_summary = self.sess.run([self.episode_num_op, self.episode_summary_op])
            tf.logging.info(' Episode {}: total reward={:7.4f}, episode steps={}, trained steps={}'.format(self.ep_num,
                                                                                                self.ep_total_reward,
                                                                                                self.ep_steps,
                                                                                                self.tr_steps))
            sys.stdout.flush()
            self.summary_writer.add_summary(ep_summary, self.ep_num)
            #reset ops
            self.ep_total_reward, self.ep_steps = self.sess.run([self.reset_episode_total_reward_op,
                                                                 self.reset_episode_steps_op])

        self.state = self.env.reset()[None,:]
        self.done = False

    def gather_state(self, state):
        self.comm.Gather(state.astype(np.float32), self.state_recvbuf, root=0)
        return self.state_recvbuf

    def scatter_discrete_action(self, gathered_state):
        if self.rank == 0:
            self.gathered_action = self.sess.run(self.outputs['action_prob'],
                                                 feed_dict={self.inputs['state']:gathered_state})
        self.comm.Scatter(self.gathered_action, self.action_recvbuf, root=0)
        return self.action_recvbuf

    def scatter_continuous_action(self, gathered_state):
        if self.rank == 0:
            self.gathered_action = self.sess.run(self.outputs['action'],
                                                 feed_dict={self.inputs['state']:gathered_state})
        self.comm.Scatter(self.gathered_action, self.action_recvbuf, root=0)
        return self.action_recvbuf

    def scatter_value(self, gathered_state):
        if self.rank == 0:
            self.gathered_value = self.sess.run(self.outputs['value'],
                                                feed_dict={self.inputs['state']:gathered_state})
        self.comm.Scatter(self.gathered_value, self.value_recvbuf, root=0)
        return self.value_recvbuf

    def gather_target_value(self, discounted_value):
        self.comm.Gather(discounted_value.astype(np.float32), self.target_value_recvbuf, root=0)
        return self.target_value_recvbuf


    def gather_data_and_train(self, mem_data):
        last_state = mem_data['next_state'][-1:]
        last_done = mem_data['done'][-1]
        gathered_last_state = self.gather_state(last_state)
        last_value = self.scatter_value(gathered_last_state)
        discounted_value = self.discount(mem_data, last_value * (1.0 - last_done))
        gathered_target_value = self.gather_target_value(discounted_value)
        gathered_mem_data = self.comm.gather(mem_data, root=0)
        if gathered_mem_data is not None:
            gathered_state = np.concatenate([data['state'] for data in gathered_mem_data], axis=0)
            gathered_action = np.concatenate([data['action'] for data in gathered_mem_data], axis=0)
            results = self.sess.run(self.train_ops+[self.train_summary_op],
                         feed_dict={self.inputs['state']:gathered_state,
                                    self.inputs['action']:gathered_action,
                                    self.inputs['target_value']:gathered_target_value})
            tr_steps = self.sess.run(self.global_step)
            self.tr_steps = tr_steps
            self.summary_writer.add_summary(results[-1], self.tr_steps)
        else:
            tr_steps = None
        self.tr_steps = self.comm.bcast(tr_steps, root=0)


    def one_step_update(self):
        pass

    def discount(self, n_step_mem, last_value):
        """
        get target value from n_step_mem, last_value by discounting by gamma
        """
        target_value = np.zeros((len(n_step_mem['reward']),1))
        next_v = last_value
        for i in reversed(range(len(target_value))):
            next_v = n_step_mem['reward'][i] + self.agent.gamma*next_v*(1.-n_step_mem['done'][i])
            target_value[i] = next_v
        return target_value

    def train(self, training_steps=1000000, env_render=True):
        if self.rank == 0 and env_render:
            self.env.render()
        self.sess.run(tf.global_variables_initializer())
        self.comm.barrier()
        tf.logging.info('Process {} started training.'.format(self.rank))
        sys.stdout.flush()

        while self.tr_steps <= training_steps:
            self.reset_episode_vars()
            while self.done == False and self.tr_steps <= training_steps:
                self.one_step_update()
                if self.rank == 0 and env_render:
                    self.env.render()
                if self.agent.memory.length == self.agent.memory.memory_size:
                    n_step_mem = self.agent.memory.get_data()
                    self.gather_data_and_train(n_step_mem)
                    if self.rank == 0 and self.tr_steps % self.save_steps == 0:
                        self.save_model()

        tf.logging.info('Process {} training finished'.format(self.rank))
        if self.rank == 0:
            self.save_model()


    def act(self, env_render=True, sleep_time=0.005):
        #reset ops
        self.ep_total_reward, self.ep_steps = self.sess.run([self.reset_episode_total_reward_op,
                                                             self.reset_episode_steps_op])
        while True:
            self.reset_episode_vars()
            if env_render:
                self.env.render()
            while self.done == False:
                if env_render:
                    self.env.render()
                time.sleep(sleep_time)
                self.one_step_update()

    def save_model(self):
        model_save_path = self.saver.save(self.sess, self.model_dir+'/model',
                                          global_step=self.tr_steps)
        tf.logging.info('Agent model saved in {}'.format(model_save_path))

    def load_model(self, model_path='model/model'):
        self.sess.run(tf.global_variables_initializer())
        self.saver.restore(self.sess, model_path)
        tf.logging.info('Agent model loaded from {}'.format(model_path))

class NStepMPIAgentFF(NStepMPIAgent):
    def __init__(self, agent=None, env=None, save_steps=5000, model_dir='model', dtype=tf.float32):
        super(NStepMPIAgentFF, self).__init__(agent=agent, env=env,
                                             save_steps=save_steps,
                                             model_dir=model_dir,  dtype=dtype)

    def one_step_update(self):
        if self.agent.discrete_action:
            gathered_state = self.gather_state(self.state)
            action_prob = self.scatter_discrete_action(gathered_state)
            action = np.random.choice(self.agent.nb_actions, p=action_prob)
            observation, reward, done, info = self.env.step(action)
            if self.agent.add_memory is not None and self.agent.add_memory == True:
                action_one_hot = np.zeros(self.agent.action_shape)
                action_one_hot[action] += 1.
                self.agent.memory.add(self.state, action_one_hot, reward, observation, done)
        else:
            gathered_state = self.gather_state(self.state)
            action = self.scatter_continuous_action(gathered_state)
            observation, reward, done, info = self.env.step(action)
            if self.agent.add_memory is not None and self.agent.add_memory == True:
                self.agent.memory.add(self.state, action, reward, observation, done)

        self.state = observation[None,:]
        self.done = done
        if self.rank == 0:
            self.ep_total_reward, self.ep_steps, step_summary = self.sess.run([self.episode_total_reward_op,
                                                                               self.episode_steps_op,
                                                                               self.step_summary_op],
                                                                               feed_dict={self.current_reward:reward})
            self.summary_writer.add_summary(step_summary, self.tr_steps)
