import numpy as np
import pandas as pd


class Game:
    game_name = 'Unnamed Game'
    players = 0

    def __init__(self, seed=0):
        self.history = []

    def get_state_and_actions(self):  # Does not mutate data!
        return None

    def execute_actions(self, actions):
        return None


class Agent:
    agent_type = 'Unnamed Agent'

    def __init__(self):
        pass

    def get_move(self, sna):
        if not sna:
            return None
        return None

    def end(self, score):
        pass

    def __repr__(self):
        return "{}:{}".format(self.agent_type, self.id)


def run_single_game(game, agents_w_kwargs):
    agents = [agent(**y) for agent, y in agents_w_kwargs]
    game = game()
    game_over = False
    while not game_over:
        snas = game.get_state_and_actions()
        acts = tuple([a.get_move(sna) for a, sna in zip(agents, snas)])
        result = game.execute_actions(acts)
        if result:
            game_over = True
    for res, agent in zip(result, agents):
        agent.end(res)
    return result, game.history


def random_unlimited_tournament(game, agents, n=11):
    agents = {str(a(**k)): (a, k) for a, k in agents}
    agent_names = list(agents.keys())
    results = []
    histories = []
    for i in range(n):
        player_ids = np.random.choice(agent_names, game.players, replace=False)
        result, moves = run_single_game(game, [agents[pid] for pid in player_ids])
        results.append({pid: score for pid, score in zip(player_ids, result)})
        histories.append(moves)
    return pd.DataFrame(results), histories
