import math
import collections
from Agents.Agent import Agent
from Board import Board
from ZobristHash import ZobristHash


class MinMaxAgent(Agent):

    def __init__(self, player_no: int, max_depth: int):
        super(MinMaxAgent, self).__init__(player_no)
        self.max_depth = max_depth
        self.zb = ZobristHash(player_no)
        self.squares = [[1], [3], [5], [7],
                        [8], [10], [12], [14],
                        [17], [19], [21], [23],
                        [24], [26], [28], [30],
                        [33], [35], [37], [39],
                        [40], [42], [44], [46],
                        [49], [51], [53], [55],
                        [56], [58], [60], [62]]

    def play(self, moves: list, board: list):
        self.z_hash = {}
        _, move_index= self._minmax_ab(self.max_depth, -math.inf, math.inf, bool(self.player_no), board, self.player_no)
        return moves[move_index]

    def _minmax_ab(self, depth, alpha, beta, max_player, board, player_no):

        if player_no:
            steps = [-7, -9]
            player_num = 1
        else:
            steps = [9, 7]
            player_num = -1

        moves = Board.get_valid_moves(board, self.squares, steps, player_num, False, False)[::-1]

        length = len(moves)
        if depth == 0 or length == 0:
            return self._get_board_hash_score(board, player_no), 0

        if max_player:
            max_eval = -math.inf
            for i in range(length):
                next_board = [i for i in board]
                next_board = Board.play_move(next_board, moves[i], player_no)
                hash = self.zb.calculate_hash(next_board, player_no)
                if hash in self.z_hash:
                    eval = self.z_hash[hash]
                else:
                    eval, _ = self._minmax_ab(depth - 1, alpha, beta, False, next_board,  1 - player_no)
                if eval > max_eval:
                    max_index = i
                    max_eval = eval
                alpha = max(eval, alpha)
                if beta <= alpha:
                    break
            return max_eval, (length - 1) - max_index

        else:
            min_eval = math.inf
            for i in range(length):
                next_board = [i for i in board]
                next_board = Board.play_move(next_board, moves[i], player_no)
                hash = self.zb.calculate_hash(next_board, player_no)
                if hash in self.z_hash:
                    eval = self.z_hash[hash]
                else:
                    eval, _ = self._minmax_ab(depth - 1, alpha, beta, True, next_board, 1 - player_no)
                if eval < min_eval:
                    min_eval = eval
                    min_index = i
                min_eval = min(min_eval, eval)
                beta = min(eval, beta)
                if beta <= alpha:
                    break
            return min_eval, (length - 1) - min_index

    def _get_board_hash_score(self, board, player_no):
        hash = self.zb.calculate_hash(board, player_no)
        if hash not in self.z_hash:
            score = self._heuristicFunction(board)
            self.z_hash[hash] = score
        else:
            score = self.z_hash[hash]
        return score

    def _heuristicFunction(self, board: list) -> int:
        counter = collections.Counter(board)
        if -1 not in counter and -2 not in counter:
            return 72
        elif 1 not in counter and 2 not in counter:
            return -72

        return sum(board)
