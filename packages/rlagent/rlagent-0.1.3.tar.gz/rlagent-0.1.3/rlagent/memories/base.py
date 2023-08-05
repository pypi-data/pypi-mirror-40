import numpy as np

class Memory(object):

    def __init__(self, memory_size, state_shape, action_shape, dtype=np.float32):
        self.memory_size = memory_size
        self.state_shape = state_shape
        self.action_shape = action_shape
        self.dtype = dtype
        self.length = 0
        self.state_data = np.zeros((self.memory_size,) + self.state_shape).astype(self.dtype)
        self.action_data = np.zeros((self.memory_size,) + self.action_shape).astype(self.dtype)
        self.reward_data = np.zeros((self.memory_size, 1)).astype(self.dtype)
        self.next_state_data = np.zeros((self.memory_size,) + self.state_shape).astype(self.dtype)
        self.done_data = np.zeros((self.memory_size, 1)).astype(self.dtype)
        self.data_dict = {'state':self.state_data,
                          'action':self.action_data,
                          'reward':self.reward_data,
                          'next_state':self.next_state_data,
                          'done':self.done_data}

    def __len__(self):
        return self.length

    def clear(self):
        self.length = 0
        self.state_data.fill(0)
        self.action_data.fill(0)
        self.reward_data.fill(0)
        self.next_state_data.fill(0)
        self.done_data.fill(0)

    def get_data(self):
        return self.data_dict
