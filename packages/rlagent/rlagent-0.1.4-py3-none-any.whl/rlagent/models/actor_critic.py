import tensorflow as tf
import numpy as np

class ActorCriticFF(tf.keras.Model):

    def __init__(self, state_shape, action_shape, name='actor_critic', discrete_action=True):
        super(ActorCriticFF, self).__init__(name=name)
        self.state_shape = state_shape
        self.state_size = np.prod(state_shape)
        self.action_shape = action_shape
        self.action_size = np.prod(self.action_shape)
        self.discrete_action = discrete_action

        #layers
        self.dense1 = tf.layers.Dense(128, kernel_initializer=tf.keras.initializers.glorot_normal())
        self.dense1_activation = tf.keras.layers.Activation('relu')
        self.dense2 = tf.layers.Dense(128, kernel_initializer=tf.keras.initializers.glorot_normal())
        self.dense2_activation = tf.keras.layers.Activation('relu')
        if self.discrete_action:
            self.action_logits_layer = tf.layers.Dense(self.action_size, kernel_initializer=tf.keras.initializers.glorot_normal())
        else:
            self.action_mean_layer = tf.layers.Dense(self.action_size, activation=tf.nn.tanh, kernel_initializer=tf.keras.initializers.glorot_normal())
            self.action_variance_layer = tf.layers.Dense(1, activation=tf.nn.softplus, kernel_initializer=tf.keras.initializers.glorot_normal())

        self.value_layer = tf.layers.Dense(1, kernel_initializer=tf.keras.initializers.glorot_normal())

    def call(self, state):
        with tf.variable_scope(self.name, reuse=tf.AUTO_REUSE):
            x = self.dense1(state)
            x = tf.contrib.layers.layer_norm(x)
            x = self.dense1_activation(x)
            x = self.dense2(x)
            x = tf.contrib.layers.layer_norm(x)
            x = self.dense2_activation(x)
            value = self.value_layer(x)
            if self.discrete_action:
                action_logits = self.action_logits_layer(x)
                action_prob = tf.nn.softmax(action_logits)
                return action_prob, value, action_logits
            else:
                action_mean = self.action_mean_layer(x)
                action_variance = self.action_variance_layer(x)
                self.action_dist = tf.distributions.Normal(loc=action_mean, scale=tf.sqrt(action_variance))
                action = tf.clip_by_value(tf.squeeze(self.action_dist.sample(1), axis=0), -1.0, 1.0)
                return action, value
