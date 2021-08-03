from Agents import MinMaxAgent, RLAgent, RandomAgent, HumanAgent
from NeuralNetwork import Qstates, RegressionNeuralNetwork
from Board import Board


def main():
    train_size = 100000
    RNN = RegressionNeuralNetwork.RegressionNeuralNetwork(2, [20,20], 32, init = False, function = 'tanh')
    a = RLAgent.RLAgent(0, RNN, train_size, istrain=False)
    b = RLAgent.RLAgent(1, RNN, train_size, istrain=False)
    # b = MinMaxAgent.MinMaxAgent(1, 5)
    acc = 0
    board = Board(a, b)
    for i in range(train_size):
        # 1 means b wins, -1 means a wins
        result = board.play()
        sequence = board.getSequence()
        print(result)
        a.update_outcome(sequence, result)

    a.save_to_file()


if __name__ == "__main__":
    main()
