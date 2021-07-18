from NeuralNetwork import Qstates, RegressionNeuralNetwork as RNN
import random
from Agents.Agent import Agent

class RLAgent(Agent):

    def __init__(self, player_no, RNN : RNN.RegressionNeuralNetwork, size = 1000, istrain = True):
        super(RLAgent, self).__init__(player_no)
        self.RNN = RNN
        self.Qstates = Qstates.Qstates(self.RNN)
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
        if self.istrain:
            self.games_played = (1 + self.games_played) % self.size
            self.Qstates.update_NN(final_sequence, result)

    def save_to_file(self):
        self.RNN.saveToFile()

