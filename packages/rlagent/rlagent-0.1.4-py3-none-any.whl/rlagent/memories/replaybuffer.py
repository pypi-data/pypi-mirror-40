import numpy as np
from rlagent.memories.base import Memory

class ReplayBuffer(Memory):

    def __init__(self, memory_size, state_shape, action_shape, batch_size=128, dtype=np.float32):
        super(ReplayBuffer, self).__init__(memory_size, state_shape, action_shape, dtype=dtype)
        self.start = 0
        self.batch_size = batch_size

    def add(self, state, action, reward, next_state, done):
        """Add a new experience to memory."""
        if self.length == self.memory_size:
            self.start = (self.start + 1) % self.memory_size
        else:
            self.length += 1
        idx = (self.start + self.length - 1) % self.memory_size
        self.state_data[idx] = state
        self.action_data[idx] = action
        self.reward_data[idx] = reward
        self.next_state_data[idx] = next_state
        self.done_data[idx] = done

    def sample(self):
        """Randomly sample a batch of experiences from memory."""
        idxs = np.random.randint(0,self.length - 1, size=self.batch_size)
        sampled = {'state':self.state_data[idxs],
                   'action':self.action_data[idxs],
                   'reward':self.reward_data[idxs],
                   'next_state':self.next_state_data[idxs],
                   'done':self.done_data[idxs]}
        return sampled
