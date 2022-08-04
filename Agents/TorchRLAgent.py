from TorchNeuralNetwork import TorchQstates
import random
from Agents.Agent import Agent
import torch


class TorchRLAgent(Agent):

    def __init__(self, player_no, TRNN, size = 10000, istrain = True):
        super(TorchRLAgent, self).__init__(player_no)
        self.TRNN = TRNN
        self.Qstates = TorchQstates.TorchQstates(self.TRNN)
        self.istrain = istrain
        self.size = size
        self.games_played = 0


    def play(self, moves : list, board : list) -> list:
        if self.istrain:
            return self.train(moves, board)
        else:
            return self.actual(moves, board)


    def train(self, moves : list, board : list) -> list:
        prob = self.games_played/self.size
        boolean = random.random() > prob
        if boolean:
            return random.choice(moves)
        else:
            return self.choose_optimal_move(moves, board)


    def actual(self, moves : list, board : list) -> list:
        return self.choose_optimal_move(moves, board)


    def choose_random_move(self, moves : list) -> list:
        return random.choice(moves)


    def choose_optimal_move(self, moves : list, board : list) -> list:
        return self.Qstates.choose_optimal_move(moves, board, self.player_no)


    def update_outcome(self, final_sequence, result):
        self.games_played = (1 + self.games_played) % self.size
        self.Qstates.update_NN(final_sequence, result)

    def save_to_file(self):
        torch.save(self.TRNN.state_dict(), self.TRNN.weightsPath)