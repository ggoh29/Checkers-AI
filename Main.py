from Agents import MinMaxAgent, RLAgent, RandomAgent, HumanAgent, MiniMaxRLAgent
from NeuralNetwork import Qstates, RegressionNeuralNetwork
from Board import Board



def main():
    train_size = 3
    RNN = RegressionNeuralNetwork.RegressionNeuralNetwork(2, [20,20], 32, init = False, function = 'tanh')
    # a = MiniMaxRLAgent.MinMaxRLAgent(0, 5, RNN)
    # a = RLAgent.RLAgent(0, RNN, train_size, istrain=False)
    # a = MinMaxAgent.MinMaxAgent(0, 6)
    # a = RandomAgent.RandomAgent(0)
    a = HumanAgent.HumanAgent(0)
    # b = RLAgent.RLAgent(1, RNN, train_size, istrain=False)
    # b = MinMaxAgent.MinMaxAgent(1, 6)
    # b = RandomAgent.RandomAgent(1)
    b = MiniMaxRLAgent.MinMaxRLAgent(1, 8, RNN)
    board = Board(a, b)
    acc = 0
    for i in range(train_size):
        # 1 means b wins, -1 means a wins
        result = board.play()
        sequence = board.getSequence()
        # a.update_outcome(sequence, result)
    print(acc)
    # a.save_to_file()


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