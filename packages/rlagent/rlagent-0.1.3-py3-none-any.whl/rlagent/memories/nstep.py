import numpy as np
from rlagent.memories.base import Memory

class NStepMemory(Memory):

    def __init__(self, memory_size, state_shape, action_shape, dtype=np.float32):
        super(NStepMemory, self).__init__(memory_size, state_shape, action_shape, dtype=dtype)


    def add(self, state, action, reward, next_state, done):
        if self.length == self.memory_size:
            self.clear()
        self.state_data[self.length] = state
        self.action_data[self.length] = action
        self.reward_data[self.length] = reward
        self.next_state_data[self.length] = next_state
        self.done_data[self.length] = done
        self.length += 1
