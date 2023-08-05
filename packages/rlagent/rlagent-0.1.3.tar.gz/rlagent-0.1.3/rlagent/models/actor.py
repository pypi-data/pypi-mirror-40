import tensorflow as tf
import numpy as np

class ActorFF(tf.keras.Model):

    def __init__(self, state_shape, action_shape, name='actor'):
        super(ActorFF, self).__init__(name=name)
        self.state_shape = state_shape
        self.state_size = np.prod(state_shape)
        self.action_shape = action_shape
        self.action_size = np.prod(self.action_shape)

        #layers
        self.dense1 = tf.layers.Dense(128, kernel_initializer=tf.keras.initializers.glorot_uniform())
        self.dense1_activation = tf.keras.layers.Activation('relu')
        self.dense2 = tf.layers.Dense(64, kernel_initializer=tf.keras.initializers.glorot_uniform())
        self.dense2_activation = tf.keras.layers.Activation('relu')
        self.action_layer = tf.layers.Dense(self.action_size, activation=tf.tanh,
                        kernel_initializer=tf.random_uniform_initializer(minval=-3e-3, maxval=3e-3))

    def call(self, inputs):
        with tf.variable_scope(self.name, reuse=tf.AUTO_REUSE):
            x = self.dense1(inputs)
            x = tf.contrib.layers.layer_norm(x)
            x = self.dense1_activation(x)
            x = self.dense2(x)
            x = tf.contrib.layers.layer_norm(x)
            x = self.dense2_activation(x)
            action = self.action_layer(x)
            return action
