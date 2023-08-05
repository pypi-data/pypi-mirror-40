import rlagent
import tensorflow as tf
import time
import pickle

class ExperienceReplayAgent(rlagent.Agent):
    def __init__(self, agent=None, env=None, save_steps=5000, model_dir='model',  dtype=tf.float32):
        super(ExperienceReplayAgent, self).__init__(agent=agent, env=env,
                                             save_steps=save_steps,
                                             model_dir=model_dir,  dtype=dtype)
        #placeholders
        self.state_input = tf.placeholder(self.dtype, (None,) + self.agent.state_shape, name='state_input')
        self.action_input = tf.placeholder(self.dtype, (None,) + self.agent.action_shape, name='action_input')
        self.reward_input = tf.placeholder(self.dtype, (None,1), name='reward_input')
        self.next_state_input = tf.placeholder(self.dtype, (None,) + self.agent.state_shape, name='next_state_input')
        self.done_input = tf.placeholder(self.dtype, (None,1), name='done_input')

        #placeholder to keras input
        self.state_input_keras = tf.keras.Input(tensor=self.state_input)
        self.action_input_keras = tf.keras.Input(tensor=self.action_input)
        self.reward_input_keras = tf.keras.Input(tensor=self.reward_input)
        self.next_state_input_keras = tf.keras.Input(tensor=self.next_state_input)
        self.done_input_keras = tf.keras.Input(tensor=self.done_input)
        self.inputs = [self.state_input_keras,
                       self.action_input_keras,
                       self.reward_input_keras,
                       self.next_state_input_keras,
                       self.done_input_keras]

        #config variables
        outputs = self.agent(self.inputs)
        self.outputs = self.agent.convert_output_list_to_dict(outputs)

        #set losses, train ops
        self.agent.set_losses(self.inputs, outputs)
        self.losses = self.agent.losses_dict
        self.global_step = tf.train.get_or_create_global_step()
        self.train_ops, self.train_init_ops = self.agent.get_train_ops(self.global_step)

        #tf.summary
        self.train_summary_op = self.set_summary_ops_per_train()

        #saver
        self.saver = tf.train.Saver()

    def one_step_update(self):
        action = self.sess.run(self.outputs['actor_action'],
                               feed_dict={self.state_input:self.state})
        if self.agent.action_noise is not None and self.agent.action_noise == True:
            action[0] += self.agent.noise.sample()
        observation, reward, done, info = self.env.step(action[0])
        if self.agent.add_memory is not None and self.agent.add_memory == True:
            self.agent.memory.add(self.state, action, reward, observation, done)
        self.state = observation[None,:]
        self.done = done
        self.ep_total_reward, self.ep_steps, self.tr_steps, step_summary = self.sess.run([self.episode_total_reward_op,
                                                                            self.episode_steps_op,
                                                                            self.global_step,
                                                                            self.step_summary_op],
                                                                            feed_dict={self.current_reward:reward})
        self.summary_writer.add_summary(step_summary, self.tr_steps)

    def initialize_training(self, env_render=True):
        self.sess.run(tf.global_variables_initializer())
        self.sess.run(self.train_init_ops)
        tf.logging.info('Done running initial ops.')
        if env_render:
            self.env.render()
        while self.agent.memory.length < self.agent.batch_size:
            self.reset_episode_vars()
            while self.done == False:
                self.one_step_update()
        tf.logging.info('Added {} to ReplayBuffer. Starting training.'.format(len(self.agent.memory)))

    def train(self, max_training_steps=1000000, env_render=True):
        self.initialize_training(env_render=env_render)
        while (self.tr_steps <= max_training_steps):
            self.reset_episode_vars()
            while self.done == False:
                self.one_step_update()
                sampled = self.agent.memory.sample()
                results = self.sess.run(self.train_ops + [self.train_summary_op],
                                        feed_dict={self.state_input:sampled['state'],
                                                   self.action_input:sampled['action'],
                                                   self.reward_input:sampled['reward'],
                                                   self.next_state_input:sampled['next_state'],
                                                   self.done_input:sampled['done']})
                self.summary_writer.add_summary(results[-1], self.tr_steps)
                if self.tr_steps % self.save_steps == self.save_steps - 1:
                    self.save_model()
        self.save_model()

    def act(self, env_render=True, sleep_time=0.005):
        self.sess.run([self.reset_episode_num_op,
                       self.reset_episode_total_reward_op,
                       self.reset_episode_steps_op])
        if env_render:
            self.env.render()
        if self.agent.action_noise is not None and self.agent.action_noise == True:
            self.agent.action_noise = False
        if self.agent.add_memory is not None and self.agent.add_memory == True:
            self.agent.add_memory = False
        while True:
            self.reset_episode_vars()
            while self.done == False:
                time.sleep(sleep_time)
                self.one_step_update()

    def save_model(self):
        model_save_path = self.saver.save(self.sess, self.model_dir+'/model', global_step=self.tr_steps)
        memory_save_path = self.model_dir+'/agent_memory-'+str(self.tr_steps)+'.p'
        mem_file = open(memory_save_path,'wb')
        pickle.dump(self.agent.memory, mem_file)
        mem_file.close()
        tf.logging.info('Agent model saved in {}, memory saved in {}: '.format(model_save_path, memory_save_path))

    def load_model(self, model_path='model/model', memory_path=None):
        self.sess.run(tf.global_variables_initializer())
        self.saver.restore(self.sess, model_path)
        if memory_path is not None:
            mem_file = open(memory_path,'rb')
            self.agent.memory = pickle.load(mem_file)
            mem_file.close()
