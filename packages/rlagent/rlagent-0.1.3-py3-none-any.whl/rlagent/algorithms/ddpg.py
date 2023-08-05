import numpy as np
import tensorflow as tf
from rlagent.memories import ReplayBuffer
from rlagent.noises import OUNoise
from rlagent.models import ActorFF, QCriticFF

class DDPG(tf.keras.Model):
    """
    Deep Deterministic Policy Gradient Model
    """
    def __init__(self, state_shape, action_shape, replay_buffer_size=100000, batch_size=128,
                 gamma=0.995, tau=0.001, actor_lr=0.0001, critic_lr=0.001,
                 action_noise=True, add_memory=True,
                 actor_model=ActorFF, critic_model=QCriticFF):
        super(DDPG, self).__init__()
        self.state_shape = state_shape
        self.action_shape = action_shape
        self.nb_actions = np.prod(self.action_shape)

        # Replay buffer
        self.replay_buffer_size = replay_buffer_size
        self.batch_size = batch_size
        self.memory = ReplayBuffer(self.replay_buffer_size, self.state_shape, self.action_shape)
        self.add_memory = add_memory

        # Noise process
        self.noise = OUNoise(self.action_shape)
        self.action_noise = action_noise

        # Algorithm parameters
        self.gamma = gamma # discount factor
        self.tau = tau #soft update
        self.actor_lr = actor_lr
        self.critic_lr = critic_lr

        #layers
        self.actor = actor_model(self.state_shape, self.action_shape)
        self.critic = critic_model(self.state_shape, self.action_shape)

        self.target_actor = actor_model(self.state_shape, self.action_shape, name='target_actor')
        self.target_critic = critic_model(self.state_shape, self.action_shape, name='target_critic')

        #optimizer
        self.actor_optimizer = tf.train.AdamOptimizer(self.actor_lr)
        self.critic_optimizer = tf.train.AdamOptimizer(self.critic_lr)

    def call(self, inputs):
        state, action, reward, next_state, done = inputs
        #training actor
        actor_action = self.actor(state)
        actor_critic_q = self.critic([state, actor_action])
        #training critic
        critic_q = self.critic([state, action])
        #training target net
        target_actor_action = self.target_actor(next_state)
        target_actor_critic_q = self.target_critic([next_state, target_actor_action])
        return actor_action, actor_critic_q, critic_q, target_actor_critic_q

    def convert_output_list_to_dict(self, outputs):
        actor_action, actor_critic_q, critic_q, target_actor_critic_q = outputs
        return {'actor_action':actor_action,
                'actor_critic_q':actor_critic_q,
                'critic_q':critic_q,
                'target_actor_critic_q':target_actor_critic_q}

    def set_losses(self, inputs, outputs):
        state, action, reward, next_state, done = inputs
        _, actor_critic_q, critic_q, target_actor_critic_q = outputs
        Q_targets = reward + (self.gamma * target_actor_critic_q) * (1. - done)
        self.actor_loss = tf.reduce_mean(-actor_critic_q)
        self.critic_loss = tf.losses.huber_loss(Q_targets, critic_q)
        self.add_loss([self.actor_loss, self.critic_loss])
        self.losses_dict = {'actor_loss':self.actor_loss, 'critic_loss':self.critic_loss}

    def convert_output_list_to_dict(self, outputs):
        actor_action, actor_critic_q, critic_q, target_actor_critic_q = outputs
        return {'actor_action':actor_action,
                'actor_critic_q':actor_critic_q,
                'critic_q':critic_q,
                'target_actor_critic_q':target_actor_critic_q}

    def get_train_ops(self, global_step):
        """
        returns model's training operations
        return: train_ops, train_init_ops
        train_ops: operations for the training loop
        train_init_opts: operations before the training loop
        note: This function should be called after set_losses
        """
        #adding regularization
        actor_total_loss = self.actor_loss
        for l in self.actor.losses:
            actor_total_loss += l
        critic_total_loss = self.critic_loss
        for l in self.critic.losses:
            critic_total_loss += l

        actor_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=self.actor.name)
        critic_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=self.critic.name)
        target_actor_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=self.target_actor.name)
        target_critic_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=self.target_critic.name)

        actor_ops = [self.actor_optimizer.minimize(actor_total_loss,
                                                   var_list=list(set(actor_vars + self.actor.variables)),
                                                   global_step=global_step)]
        critic_ops = [self.critic_optimizer.minimize(critic_total_loss,
                                                     var_list=list(set(critic_vars + self.critic.variables)))]

        #adding other ops (batchnorm, etc.)
        actor_ops += self.actor.updates
        critic_ops += self.critic.updates

        target_init_ops = []
        soft_update_ops = []
        for var, target_var in zip(actor_vars, target_actor_vars):
            soft_update_ops.append(tf.assign(target_var, (1. - self.tau) * target_var + self.tau * var))
            target_init_ops.append(tf.assign(target_var,var))
        for var, target_var in zip(critic_vars, target_critic_vars):
            soft_update_ops.append(tf.assign(target_var, (1. - self.tau) * target_var + self.tau * var))
            target_init_ops.append(tf.assign(target_var,var))

        train_ops = actor_ops + critic_ops + soft_update_ops
        train_init_ops = target_init_ops
        return train_ops, train_init_ops
