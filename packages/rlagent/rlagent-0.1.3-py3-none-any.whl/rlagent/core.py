import tensorflow as tf

class Agent(object):
    def __init__(self, agent=None, env=None, save_steps=5000, model_dir='model',  dtype=tf.float32):
        self.agent = agent
        self.env = env
        self.dtype = dtype
        self.save_steps = save_steps
        self.model_dir = model_dir

        #episode vars
        self.set_episode_vars_and_ops()

        #tf.summary
        self.step_summary_op = self.set_summary_ops_per_step()
        self.episode_summary_op = self.set_summary_ops_per_episode()

        self.config = tf.ConfigProto()
        self.config.gpu_options.allow_growth=True
        self.sess = tf.Session(config=self.config)
        self.summary_writer = tf.summary.FileWriter(self.model_dir)


    def set_summary_ops_per_step(self):
        """
        summary per step
        """
        step_summary_op = tf.summary.scalar('current_reward', self.current_reward)
        return step_summary_op

    def set_summary_ops_per_train(self):
        """
        summary per train
        """
        loss_summary = []
        for name, loss in self.losses.items():
            loss_summary.append(tf.summary.scalar(name, loss, family='losses'))
        train_summary_op = tf.summary.merge(loss_summary)
        return train_summary_op

    def set_summary_ops_per_episode(self):
        """
        summary per episode
        """
        episode_summary = []
        episode_summary.append(tf.summary.scalar('episode_total_reward',
                                                      self.episode_total_reward,
                                                      family='episode_vars'))
        episode_summary.append(tf.summary.scalar('episode_steps',
                                                      self.episode_steps,
                                                      family='episode_vars'))

        episode_summary_op = tf.summary.merge(episode_summary)
        return episode_summary_op

    def set_episode_vars_and_ops(self):
        self.episode_num = tf.Variable(0, name='episode_num', trainable=False)
        self.episode_total_reward = tf.Variable(0.0, name='episode_total_reward', trainable=False)
        self.episode_steps = tf.Variable(0, name='episode_steps', trainable=False)

        self.current_reward = tf.placeholder(self.dtype, name='current_reward')
        self.episode_total_reward_op = tf.assign_add(self.episode_total_reward, self.current_reward)
        self.episode_steps_op = tf.assign_add(self.episode_steps, 1)
        self.episode_num_op = tf.assign_add(self.episode_num, 1)

        self.reset_episode_num_op = tf.assign(self.episode_num, 0)
        self.reset_episode_total_reward_op = tf.assign(self.episode_total_reward, 0.0)
        self.reset_episode_steps_op = tf.assign(self.episode_steps, 0)

        self.ep_num = 0
        self.ep_total_reward = 0.0
        self.ep_steps = 0
        self.tr_steps = 0
        self.done = False

    def reset_episode_vars(self):
        if self.done == True:
            self.ep_num, ep_summary = self.sess.run([self.episode_num_op, self.episode_summary_op])
            tf.logging.info(' Episode {}: total reward={:7.4f}, episode steps={}, trained steps={}'.format(self.ep_num,
                                                                                        self.ep_total_reward,
                                                                                        self.ep_steps,
                                                                                        self.tr_steps))
            self.summary_writer.add_summary(ep_summary, self.ep_num)
            #reset ops
            self.ep_total_reward, self.ep_steps = self.sess.run([self.reset_episode_total_reward_op,
                                                                 self.reset_episode_steps_op])

        self.state = self.env.reset()[None,:]
        self.done = False

    def one_step_update(self):
        pass

    def initialize_training(self, env_render=True):
        pass

    def train(self, max_training_steps=1000000, env_render=True):
        pass

    def act(self, env_render=True, sleep_time=0.005):
        pass

    def save_model(self):
        pass

    def load_model(self, model_path='model/model', memory_path=None):
        pass
