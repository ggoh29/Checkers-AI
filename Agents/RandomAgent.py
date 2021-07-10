import random
from Agents.Agent import Agent

class RandomAgent(Agent):

    def play(self, moves : list, board : list):
        return random.choice(moves)