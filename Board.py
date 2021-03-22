from Agent import Agent
from Qstates import Qstates
from ZobristHash import ZobristHash
class Board:

    def __init__(self, player1, player2, test = False, train = -1, board = None):
        self.normal0 = [9, 7]
        self.normal1 = [-7, -9]
        self.queen = [9, -7, 7, -9]
        self.valid_pos = [[1], [3], [5], [7],
                          [8], [10], [12], [14],
                          [17], [19], [21], [23],
                          [24], [26], [28], [30],
                          [33], [35], [37], [39],
                          [40], [42], [44], [46],
                          [49], [51], [53], [55],
                          [56], [58], [60], [62]]

        playermove_dct = {0: self.player0_normalMove,
                          1: self.player1_normalMove}

        player_dct = {0: player1,
                      1: player2}

        # test and board are used for situational testing purposes
        self.board = board

        while not test:
            self.board = [0, 5, 0, 5, 0, 5, 0, 5,
                          5, 0, 5, 0, 5, 0, 5, 0,
                          0, 5, 0, 5, 0, 5, 0, 5,
                          1, 0, 1, 0, 1, 0, 1, 0,
                          0, 1, 0, 1, 0, 1, 0, 1,
                          3, 0, 3, 0, 3, 0, 3, 0,
                          0, 3, 0, 3, 0, 3, 0, 3,
                          3, 0, 3, 0, 3, 0, 3, 0]

            player = 0
            while True:
                moves = playermove_dct[player]()
                if len(moves) == 0:
                    outcome = 1 - player
                    # 0, 1 into -1, 1. 1, 0 into 1, -1
                    s = "Player {} has won the game!".format(outcome)
                    player1.update_outcome(self.board, player * -1 + outcome)
                    # player2.update_outcome(self.board, player * -1 + outcome)
                    break
                if self.board.count(3) == 0 and self.board.count(5) == 0:
                    s = "Tie!"
                    player1.update_outcome(self.board, 0)
                    # player2.update_outcome(self.board, 0)
                    break
                else:
                    move = player_dct[player].play(moves, self.board)
                    self.play_move(move, player)
                    player = 1 - player
                # self.printboard()
                # print("\n")

            if train == -1:
                new_in = input("{} Input 'y' to play again.".format(s))
                if new_in != 'y':
                    break

            elif train == 0:
                return

            else:
                train -= 1





    def player0_normalMove(self):
        return self.__get_valid_moves(self.valid_pos, self.normal0, 5, False, False)



    def player1_normalMove(self):
        return self.__get_valid_moves(self.valid_pos, self.normal1, 3, False, False)


    def __get_valid_moves(self, squares, steps, player_num, movbool, capbool):
        capture = []
        moves = []
        queens = []
        l = len(steps)//2
        for coords in squares:
            i = coords[-1]
            if self.board[i] == player_num or capbool or movbool:
                if i % 8 == 0:
                    pos_moves = steps[:l]
                elif i % 8 == 7:
                    pos_moves = steps[l:]
                else:
                    pos_moves = steps
                for move in pos_moves:
                    if -1 < i + move < 64:
                        j = i + move
                    else:
                        continue
                    if self.board[j] == 1 and not capbool:
                        move1 = coords[:]
                        move1.append(j)
                        moves.append(move1)
                    if self.board[j] & 7 == (player_num & 7) ^ 6:
                        if j % 8 == 0 or j % 8 == 7 or not -1 < j + move < 64:
                            continue
                        if self.board[j + move] == 1:
                            if j + move in coords:
                                continue

                            move1 = coords[:]
                            move1.append(j + move)
                            capture.append(move1)

                            move2 = coords[:]
                            move2.append(j + move)
                            moves.append(move2)

            elif self.board[i] == player_num|8 and len(steps) == 2:
                queens.append([i])

        if len(capture) != 0:
            further_captures = self.__get_valid_moves(capture, steps, player_num, False, True)
            moves.extend(further_captures)

        if len(queens) != 0:
            queen_moves = self.__get_valid_moves(queens, self.queen, player_num, True, False)
            moves.extend(queen_moves)

        return moves


    def play_move(self, move, player):
        piece_i = move[0]
        final_pos = move[-1]
        if abs(piece_i - final_pos) < 10:
            # single move
            self.board[final_pos] = self.board[piece_i]
            self.board[piece_i] = 1
        elif len(move) == 2:
            # single move capture
            self.board[final_pos] = self.board[piece_i]
            self.board[piece_i] = 1
            self.board[(piece_i + final_pos)//2] = 1
        else:
            # multiple captures
            self.board[final_pos] = self.board[piece_i]
            self.board[piece_i] = 1
            for i in range(len(move)-1):
                start, end = move[i], move[i+1]
                self.board[(start + end)//2] = 1

        lastrow = {1 : [1, 3, 5, 7], 0 : [56, 58, 60, 62]}
        true_player = {0 : 5, 1 : 3}

        for i in lastrow[player]:
            if self.board[i] == true_player[player]:
                self.board[i] |= 8

    def printboard(self):
        swaps = {5 : 'x',
                 3 : 'o',
                 13: 'X',
                 11: '0',
                 0 : '~',
                 1 : ' ' }
        thing = [i for i in range(0,65,8)]
        for j in range(8):
            start, end = thing[j], thing[j+1]
            partition = [swaps[i] for i in self.board[start:end]]
            print(partition)





if __name__ == "__main__":
    train_size = 100000
    q = Qstates()
    a = Agent(0, q, train_size, train=True)
    b = Agent(1, q, train_size, train = True)
    b = Board(a, b, train = train_size)
    q.save_to_file()

