from Agents import MinMaxAgent, RLAgent, RandomAgent, HumanAgent, MiniMaxRLAgent, TorchRLAgent, TorchMinMaxRLAgent
from NeuralNetwork import Qstates, RegressionNeuralNetwork
from TorchNeuralNetwork import TorchQstates, TorchRegressionNeuralNetwork
from Board import Board
from tqdm import tqdm


def main():
    train_size = 10
    # RNN = RegressionNeuralNetwork.RegressionNeuralNetwork(2, [20,20], 32, init = False, function = 'tanh')
    TRNN = TorchRegressionNeuralNetwork.TorchRegressionNeuralNetwork(2, [128, 128], 32, init = False, function = 'tanh')
    # a = MiniMaxRLAgent.MinMaxRLAgent(0, 5, RNN)
    # a = RLAgent.RLAgent(0, RNN, train_size, istrain=False)
    # a = MinMaxAgent.MinMaxAgent(0, 6)
    # a = RandomAgent.RandomAgent(0)
    # a = TorchRLAgent.TorchRLAgent(0, TRNN, istrain= False)
    a = TorchMinMaxRLAgent.TorchMinMaxRLAgent(0, 9, TRNN)
    # b = HumanAgent.HumanAgent(0)
    # b = RLAgent.RLAgent(1, RNN, train_size, istrain=False)
    # b = MinMaxAgent.MinMaxAgent(1, 11)
    # b = RandomAgent.RandomAgent(1)
    # b = MiniMaxRLAgent.MinMaxRLAgent(1, 8, RNN)
    # b = TorchRLAgent.TorchRLAgent(1, TRNN, istrain= False)
    b = TorchMinMaxRLAgent.TorchMinMaxRLAgent(1, 9, TRNN)
    board = Board(a, b)
    acc = 0
    for _ in range(train_size):
        # 1 means b wins, -1 means a wins
        result = board.play()
        sequence = board.getSequence()
        a.update_outcome(sequence, result)
    a.save_to_file()


if __name__ == "__main__":
    main()

# [' 0', ' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7']
# [' 8', ' 9', '10', '11', '12', '13', '14', '15']
# ['16', '17', '18', '19', '20', '21', '22', '23']
# ['24', '25', '26', '27', '28', '29', '30', '31']
# ['32', '33', '34', '35', '36', '37', '38', '39']
# ['40', '41', '42', '43', '44', '45', '46', '47']
# ['48', '49', '50', '51', '52', '53', '54', '55']
# ['56', '57', '58', '59', '60', '61', '62', '63']