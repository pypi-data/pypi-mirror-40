from ..base import Agent


class HumanAgent(Agent):
    agent_type = 'Human Agent'

    def __init__(self, name='basic'):
        self.name = name

    def get_move(self, sna):
        if not sna:
            return None
        state = sna['state']
        actions = sna['actions']
        print(state)
        print(actions)
        while True:
            try:
                choice = int(input("Select an action:"))
                assert choice in actions
            except Exception:
                pass
            else:
                break
        return choice

    def end(self, score):
        pass

    def __repr__(self):
        return self.agent_type + ":" + self.name
