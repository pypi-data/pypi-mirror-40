import numpy as np

from ..base import Agent


class RandomAgent(Agent):
    agent_type = 'Random Agent'

    def __init__(self, name='basic'):
        self.name = name

    def get_move(self, sna):
        if not sna:
            return None
        # state = sna['state']
        actions = sna['actions']
        choice = np.random.choice(actions)
        return choice

    def end(self, score):
        pass

    def __repr__(self):
        return self.agent_type + ":" + self.name
