from copy import deepcopy

import numpy as np

from ..base import Agent


class SillyAgent(Agent):
    agent_name = 'Silly Agent'

    def __init__(self, name='basic'):
        self.name = name

    def get_move(self, sna):
        if not sna:
            return None
        state = sna['state']
        actions = sna['actions']
        choice = self.make_choice(state, actions)
        return choice

    def end(self, score):
        pass

    def check_player_win(self, state, player):
        for j in range(3):
            win = True
            for i in range(3):
                win &= state[3*j+i] == player
            if win:
                return win
        for j in range(3):
            win = True
            for i in range(3):
                win &= state[j+i*3] == player
            if win:
                return win
        if state[0] == state[4] == state[8] == player:
            return True
        if state[2] == state[4] == state[6] == player:
            return True
        return False

    def make_choice(self, state, actions):
        temp = deepcopy(state[0])
        for action in actions:
            temp[action] = 1.0
            if self.check_player_win(temp, 1.0):
                return action
            else:
                temp = deepcopy(state[0])
        for action in actions:
            temp[action] = 0.0
            if self.check_player_win(temp, 0.0):
                return action
            else:
                temp = deepcopy(state[0])
        return np.random.choice(actions)
