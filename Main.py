from Agents import MinMaxAgent, RLAgent, RandomAgent
from NeuralNetwork import Qstates, RegressionNeuralNetwork
from Board import Board


def main():

    train_size = 50
    RNN = RegressionNeuralNetwork.RegressionNeuralNetwork(2, [16,16], 32, init = True, function = 'tanh')
    a = RLAgent.RLAgent(0, RNN, train_size, istrain=True)
    # b = RLAgent.RLAgent(1, RNN, train_size)
    b = RandomAgent.RandomAgent(1)
    board = Board(a, b)
    for i in range(train_size):
        result = board.play()
        sequence = board.getSequence()
        print(result)
        a.update_outcome(sequence, result)

    a.save_to_file()


if __name__ == "__main__":
    main()
