import numpy as np

class OUNoise:
    """Ornstein-Uhlenbeck process."""
    def __init__(self, shape, mu=0.0, theta=0.15, sigma=0.03, dt=1e-2):
        """Initialize parameters and noise process."""
        self.shape = shape
        self.mu = mu
        self.theta = theta
        self.sigma = sigma
        self.dt = dt
        self.state = np.ones(self.shape) * self.mu
        self.reset()

    def reset(self):
        """Reset the internal state (= noise) to mean (mu)."""
        self.state = np.ones(self.shape) * self.mu

    def sample(self):
        """Update internal state and return it as a noise sample."""
        x = self.state
        dx = self.theta * (self.mu - x) * self.dt + self.sigma * np.sqrt(self.dt) * np.random.randn(len(x))
        self.state = x + dx
        return self.state
