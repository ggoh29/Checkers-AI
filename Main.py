from Agents import MinMaxAgent, RLAgent, RandomAgent
from NeuralNetwork import Qstates, RegressionNeuralNetwork
from Board import Board


def main():

    train_size = 1000
    RNN = RegressionNeuralNetwork.RegressionNeuralNetwork(2, [16,16], 32, init = True)
    a = RLAgent.RLAgent(0, RNN, train_size)
    b = RLAgent.RLAgent(1, RNN, train_size)
    board = Board(a, b)
    for _ in range(train_size):
        result = board.play()
        sequence = board.getSequence()
        a.update_outcome(sequence, result)

    a.save_to_file()


if __name__ == "__main__":
    main()
