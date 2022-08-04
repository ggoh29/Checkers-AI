from TorchNeuralNetwork.TorchRegressionNeuralNetwork import TorchRegressionNeuralNetwork
from Board import Board
import torch
# DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
DEVICE = torch.device('cpu')
class TorchQstates:

    def __init__(self, TRNN : TorchRegressionNeuralNetwork):
        self.loss_f = torch.nn.MSELoss()
        self.discount = 0.995
        self.learningRate = 0.0001
        self.optimiser = torch.optim.Adam(TRNN.parameters(), lr = self.learningRate, weight_decay=0)
        self.TRNN = TRNN
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
        result_dct = {1 : 1, 0 : 0, -1 : -1}
        self.TRNN.train()
        result = [result_dct[result]]

        for i in range(len(sequence)-1, 0, -1):
            result.append(self.__bellman(sequence[i-1], sequence[i], 1 - i%2))

        result.reverse()
        result = torch.tensor(result, dtype = torch.float, device = DEVICE)
        sequence = [Board.convert(board) for board in sequence]
        sequence = torch.tensor(sequence, dtype = torch.float, device = DEVICE)
        prediction = self.TRNN(sequence).squeeze(1)
        loss = self.loss_f(prediction, result)
        loss.backward()
        self.optimiser.step()


    def choose_optimal_move(self, moves : list, board : list, player_no) -> list:
        func = {1 : torch.argmax, 0 : torch.argmin}
        boards = [Board.convert(Board.play_move(board[:], move, player_no)) for move in moves]
        scores = self.TRNN(torch.tensor(boards, dtype = torch.float, device = DEVICE)).squeeze(1)
        index = int(func[player_no](scores).item())
        return moves[index]

    def __bellman(self, state, next_state, player_no):
        cur_state = Board.convert(next_state)
        cur_score = self.TRNN(cur_state)
        return cur_score + 0.995 * ((self.__get_max_next(state, player_no)) - cur_score)

    def __get_max_next(self, board, player_no):
        side_dct = {0: torch.min, 1: torch.max}

        if player_no:
            steps = [-7, -9]
            player_num = 1
        else:
            steps = [9, 7]
            player_num = -1
        moves = Board.get_valid_moves(board, self.valid_pos, steps, player_num, False, False)
        boards = [Board.convert(Board.play_move(board, move, player_no)) for move in moves]
        scores = self.TRNN(torch.tensor(boards, dtype = torch.float, device = DEVICE)).squeeze(1)

        return self.discount * side_dct[player_no](scores).item()