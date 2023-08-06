from ..base import random_unlimited_tournament
from ..agents import RandomAgent
from ..games import TicTacToe


def test_random_unlimited_tournament():
    results = random_unlimited_tournament(TicTacToe, ((RandomAgent, {'name': 'p1'}), (RandomAgent, {'name': 'p2'})))
    assert(len(results) == 2)
