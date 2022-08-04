from Agents.MinMaxAgent import MinMaxAgent
from Board import Board
import torch
from TorchNeuralNetwork import TorchQstates
# a bit of code reuse but wtv

class TorchMinMaxRLAgent(MinMaxAgent):

    def __init__(self, player_no: int, max_depth: int, TRNN):
        super(TorchMinMaxRLAgent, self).__init__(player_no, max_depth)
        self.TRNN = TRNN
        self.Qstates = TorchQstates.TorchQstates(self.TRNN)


    def _heuristicFunction(self, board: list) -> int:
        return self.TRNN(Board.convert(board))

    def update_outcome(self, final_sequence, result):
        self.Qstates.update_NN(final_sequence, result)

    def save_to_file(self):
        torch.save(self.TRNN.state_dict(), self.TRNN.weightsPath)