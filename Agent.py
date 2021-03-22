from ZobristHash import ZobristHash
from Qstates import Qstates
import random

class Agent:

    def __init__(self, player_no : int, Qstates : Qstates, train_size : int, train : bool):
        self.Qstates = Qstates
        self.player_no = player_no
        self.zb = ZobristHash(player_no)
        self.hash = self.zb.start_pos
        self.cur = 0
        self.train_size = train_size
        player_dct = {0 : [], 1 : [self.zb.start_pos]}

        self.istrain = train

        self.moves = player_dct[player_no]


    def play(self, moves : list, board : list) -> list:
        if self.istrain:
            return self.train(moves, board)
        else:
            return self.test(moves, board)

    def train(self, moves : list, board : list) -> list:
        cur_hash = self.zb.calculate_hash(board, self.player_no)
        self.moves.append(cur_hash)
        prob = self.cur/self.train_size
        if random.random() < prob:
            move = self.choose_random_move(moves)
        else:
            move = self.choose_optimal_move(moves, board)
        next_hash = self.zb.update_hash(cur_hash, move, board, self.player_no)
        self.moves.append(next_hash)
        return move


    def choose_random_move(self, moves : list) -> list:
        return random.choice(moves)


    def choose_optimal_move(self, moves : list, board : list) -> list:
        cur_hash = self.zb.calculate_hash(board, 1 - self.player_no)
        next_hash_list = [self.zb.update_hash(cur_hash, move, board, self.player_no) for move in moves]
        try:
            if cur_hash in self.Qstates.dct:
                dct = self.Qstates.dct[cur_hash]
                if len(dct) != 0:
                    dct_mx_key = max(dct, key=lambda x: dct[x])
                    move = moves[next_hash_list.index(dct_mx_key)]
                else:
                    move = random.choice(moves)
            else:
                move = random.choice(moves)
        except ValueError:
            print(board)
            print(next_hash_list)
            print(self.Qstates.dct[cur_hash])
            x = 1/0
        return move

    def test(self, moves : list, board : list) -> list:
        return self.choose_optimal_move(moves, board)

    def update_outcome(self, final_board, result):
        if self.istrain:
            self.cur += 1
            hash = self.zb.calculate_hash(final_board, self.player_no)
            if self.moves[-1] != hash:
                self.moves.append((hash))
            self.Qstates.update_dct(self.moves, abs(result))

