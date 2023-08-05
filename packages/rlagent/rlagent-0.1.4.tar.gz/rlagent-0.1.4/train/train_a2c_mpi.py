import gym
import pybullet_envs
import tensorflow as tf
import numpy as np
import argparse

from rlagent.models import ActorCriticFF
from rlagent.agents import NStepMPIAgentFF
from rlagent.memories import NStepMemory
from rlagent.algorithms import A2C

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--env', required=True, help='Environment name for gym.make')
parser.add_argument('-t', '--training_steps', type=int, default=20000, help='Training steps per process')
parser.add_argument('-s', '--save_steps', type=int, default=10000, help='Per steps to save model')
parser.add_argument('-v', '--verbosity', default='INFO', help='Verbosity: choose from {"DEBUG", "ERROR", "FATAL", "INFO", "WARN"}')
parser.add_argument('--lr', type=float, default=0.0001, help='Learning rate')
parser.add_argument('--beta', type=float, default=0.0001, help='Beta for action entropy')
parser.add_argument('--t_max', type=int, default=5, help='Env steps per train')
parser.add_argument('--render', type=bool, default=False, help='if render env: True, otherwise: False')

def main():
    args = parser.parse_args()

    verbosity = {"DEBUG":tf.logging.DEBUG,
                 "ERROR":tf.logging.ERROR,
                 "FATAL":tf.logging.FATAL,
                 "INFO":tf.logging.INFO,
                 "WARN":tf.logging.WARN}
    tf.logging.set_verbosity(verbosity[args.verbosity])

    env = gym.make(args.env)
    state_shape = env.observation_space.shape

    if type(env.action_space) == gym.spaces.Discrete:
        action_shape = (env.action_space.n,)
        discrete_action = True
    elif type(env.action_space) == gym.spaces.Box:
        action_shape = env.action_space.shape
        discrete_action = False
    else:
        raise NotImplementedError('Needs a custom function for action shape...')

    agent = A2C(state_shape, action_shape,
                discrete_action=discrete_action,
                lr=args.lr, beta=args.beta, t_max=args.t_max,
                actor_critic_model=ActorCriticFF,
                memory_model=NStepMemory)

    tf_agent = NStepMPIAgentFF(agent=agent, env=env, save_steps=args.save_steps)
    tf_agent.train(training_steps=args.training_steps, env_render=args.render)

if __name__ == "__main__":
    main()
