from Agents.Agent import Agent
from ZobristHash import ZobristHash

class HumanAgent(Agent):

    def play(self, moves : list, board : list):
        i = int(input(moves))
        return moves[i]