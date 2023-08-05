import numpy as np
import tensorflow as tf
from mpi4py import MPI

from rlagent.memories import NStepMemory
from rlagent.models import ActorCriticFF

class A2C(tf.keras.Model):

    def __init__(self, state_shape, action_shape,
                 gamma=0.99, beta=0.01, lr=0.0003,
                 clip_grad_by_norm_ratio=10.0, t_max=5,
                 discrete_action=True,
                 add_memory=True,
                 actor_critic_model=ActorCriticFF,
                 memory_model=NStepMemory):
        super(A2C, self).__init__()

        self.state_shape = state_shape
        self.action_shape = action_shape
        self.nb_actions = np.prod(self.action_shape)
        self.discrete_action = discrete_action


        # Algorithm parameters
        self.gamma = gamma # discount factor
        self.beta = beta #action_entropy coeff
        self.lr = lr
        self.clip_grad_by_norm_ratio = clip_grad_by_norm_ratio
        self.t_max = t_max

        #classes
        self.actor_critic_model = actor_critic_model
        self.memory_model = memory_model


        #local_model
        self.local_model = self.actor_critic_model(self.state_shape, self.action_shape, name='local_model',
                                                   discrete_action=self.discrete_action)

        #memory
        self.add_memory = add_memory
        self.memory = self.memory_model(self.t_max, self.state_shape, self.action_shape)


        #optimizer
        self.optimizer = tf.train.AdamOptimizer(self.lr, epsilon=1.5e-8)



    def call(self, inputs):
        local_model_output = self.local_model(inputs['state'])
        return local_model_output

    def convert_output_list_to_dict(self, outputs):
        if self.discrete_action:
            action_prob, value, action_logits = outputs
            return {'action_prob':action_prob, 'value':value, 'action_logits':action_logits}
        else:
            action, value = outputs
            return {'action':action, 'value':value, 'action_dist':self.local_model.action_dist}

    def set_losses(self, inputs, outputs):
        value_loss = tf.losses.mean_squared_error(inputs['target_value'], outputs['value'],
                                                  reduction=tf.losses.Reduction.SUM)

        #policy_loss
        advantage = inputs['target_value'] - outputs['value']
        if self.discrete_action:
            action_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(labels=outputs['action_prob'], logits=outputs['action_logits'])
            policy_xen = tf.nn.softmax_cross_entropy_with_logits_v2(labels=inputs['action'], logits=outputs['action_logits'])
            policy_loss = policy_xen * tf.stop_gradient(advantage) - self.beta * tf.reduce_sum(action_entropy)
        else:
            action_entropy = outputs['action_dist'].entropy()
            policy_log_prob = -outputs['action_dist'].log_prob(inputs['action'])
            policy_loss = policy_log_prob * tf.stop_gradient(advantage) - self.beta * tf.reduce_sum(action_entropy)

        self.total_loss = value_loss + tf.reduce_sum(policy_loss)
        self.add_loss([self.total_loss])
        self.losses_dict = {'total_loss':self.total_loss}

    def get_train_ops(self, global_step):
        #adding regularization
        total_loss = self.total_loss
        for l in self.local_model.losses:
            total_loss += l

        local_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=self.local_model.name)
        local_grads_and_vars = self.optimizer.compute_gradients(total_loss, var_list=local_vars)
        local_grads = [local_grad for local_grad, local_var in local_grads_and_vars]
        clipped_local_grads, _ = tf.clip_by_global_norm(local_grads, self.clip_grad_by_norm_ratio)
        clipped_local_grads_and_vars = [[clipped_local_grads[i], local_vars[i]] for i in range(len(clipped_local_grads))]
        local_update_op = self.optimizer.apply_gradients(clipped_local_grads_and_vars, global_step=global_step)
        train_ops = [local_update_op]

        #adding other ops (batchnorm, etc.)
        train_ops += self.local_model.updates
        return train_ops
