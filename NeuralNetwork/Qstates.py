from NeuralNetwork.RegressionNeuralNetwork import RegressionNeuralNetwork
from Board import Board

class Qstates:

    def __init__(self, RegressionNeuralNetwork : RegressionNeuralNetwork):
        self.discountRate = 0.95
        self.alpha = 0.95
        self.learningRate = 0.5
        self.RNN = RegressionNeuralNetwork
        self.valid_pos = [[1], [3], [5], [7],
                     [8], [10], [12], [14],
                     [17], [19], [21], [23],
                     [24], [26], [28], [30],
                     [33], [35], [37], [39],
                     [40], [42], [44], [46],
                     [49], [51], [53], [55],
                     [56], [58], [60], [62]]

    def update_NN(self, sequence, result):
        # 1 for win, 0 for tie
        result_dct = {1 : 100, 0 : 0, -1 : -100}

        result = [result_dct[result]]

        for i in range(len(sequence)-1, 0, -1):
            result.append(self.__bellman(sequence[i-1], sequence[i], 1 - i%2))

        result.reverse()
        self.RNN.updateNetwork(sequence, result, self.learningRate)


    def choose_optimal_move(self, moves : list, board : list, player_no) -> list:
        func = {1 : max, 0 : min}
        boards = [Board.convert(Board.play_move([i for i in board], move, player_no)) for move in moves]
        scores = [self.RNN.predict(board) for board in boards]
        index = scores.index(func[player_no](scores))
        return moves[index]

    def __bellman(self, state, next_state, player_no):
        cur_state = Board.convert(next_state)
        cur_score = self.RNN.predict(cur_state)
        return cur_score + self.alpha * ((self.__get_max_next(state, player_no)) - cur_score)


    def __get_max_next(self, board, player_no):
        side_dct = {0: min, 1: max}

        if player_no:
            steps = [-7, -9]
            player_num = 3
        else:
            steps = [9, 7]
            player_num = 5
        moves = Board.get_valid_moves(board, self.valid_pos, steps, player_num, False, False)
        boards = [Board.convert(Board.play_move(board, move, player_no)) for move in moves]
        # print(boards)
        scores = [self.RNN.predict(board) for board in boards]
        # print(scores)

        return self.discountRate * side_dct[player_no](scores)

    def save_to_file(self):
        self.RNN.saveToFile()
