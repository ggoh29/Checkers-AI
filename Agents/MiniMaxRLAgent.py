import math
import collections
from Agents.Agent import Agent
from Agents.MinMaxAgent import MinMaxAgent
from Board import Board
from ZobristHash import ZobristHash
from NeuralNetwork import Qstates, RegressionNeuralNetwork as RNN
# a bit of code reuse but wtv

class MinMaxRLAgent(MinMaxAgent):

    def __init__(self, player_no: int, max_depth: int, RNN : RNN.RegressionNeuralNetwork,):
        super(MinMaxRLAgent, self).__init__(player_no, max_depth)
        self.RNN = RNN
        self.Qstates = Qstates.Qstates(self.RNN)


    def _heuristicFunction(self, board: list) -> int:
        return self.RNN.predict(Board.convert(board))

    def update_outcome(self, final_sequence, result):
        self.Qstates.update_NN(final_sequence, result)

    def save_to_file(self):
        self.RNN.saveToFile()
