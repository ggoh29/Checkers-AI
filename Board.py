from Agents import MinMaxAgent

v = [1, 3, 5, 7,
         8, 10, 12, 14,
         17, 19, 21, 23,
         24, 26, 28, 30,
         33, 35, 37, 39,
         40, 42, 44, 46,
         49, 51, 53, 55,
         56, 58, 60, 62]


class Board:

    def __init__(self, player1, player2, max_length=150, test=False, board=None):
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

        self.playermove_dct = {0: self.player0_normalMove, 1: self.player1_normalMove}
        self.player_dct = {0: player1, 1: player2}
        self.sequence = []
        self.max_length = max_length
        # test and board are used for situational testing purposes
        if test:
            self.board = board
        else:
            self.board = [0, -1, 0, -1, 0, -1, 0, -1,
                                        -1, 0, -1, 0, -1, 0, -1, 0,
                                        0, -1, 0, -1, 0, -1, 0, -1,
                                        0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0,
                                        1, 0, 1, 0, 1, 0, 1, 0,
                                        0, 1, 0, 1, 0, 1, 0, 1,
                                        1, 0, 1, 0, 1, 0, 1, 0]
            self.copy = [0, -1, 0, -1, 0, -1, 0, -1,
                                     -1, 0, -1, 0, -1, 0, -1, 0,
                                     0, -1, 0, -1, 0, -1, 0, -1,
                                     0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0,
                                     1, 0, 1, 0, 1, 0, 1, 0,
                                     0, 1, 0, 1, 0, 1, 0, 1,
                                     1, 0, 1, 0, 1, 0, 1, 0]

    def player0_normalMove(self):
        return Board.get_valid_moves(self.board, self.valid_pos, self.normal0, -1, False, False)

    def player1_normalMove(self):
        return Board.get_valid_moves(self.board, self.valid_pos, self.normal1, 1, False, False)

    def printboard(self):
        swaps = {-1: 'x',
                         1: 'o',
                         -2: 'X',
                         2: '0',
                         0: ' '}
        thing = [i for i in range(0, 65, 8)]
        for j in range(8):
            start, end = thing[j], thing[j + 1]
            partition = [swaps[i] for i in self.board[start:end]]
            print(partition)
        print("\n")

    def play(self):
        player = 0
        outcome = 0
        self.sequence = [[i for i in self.board]]
        for _ in range(self.max_length):
            self.printboard()
            moves = self.playermove_dct[player]()
            if len(moves) == 0:
                outcome = 1 - player
                # 0, 1 into -1, 1. 1, 0 into 1, -1
                print("Player {} has won the game!".format(outcome))
                outcome = player * -1 + outcome
                break
            if self.board.count(1) == 0 and self.board.count(-1) == 0:
                print("Tie!")
                outcome = 0
                break
            else:
                move = self.player_dct[player].play(moves, self.board)
                Board.play_move(self.board, move, player)
                self.sequence.append([i for i in self.board])
                player = 1 - player
        self.printboard()
        # print("\n")
        self.board = self.copy[:]
        # print("Tie!")
        return outcome

    def getSequence(self):
        return self.sequence

    @staticmethod
    def convert(board):
        return [board[i] for i in v]

    @staticmethod
    def get_valid_moves(board, squares, steps, player_num, movbool, capbool):
        capture = []
        moves = []
        queens = []
        l = len(steps) // 2
        for coords in squares:
            i = coords[-1]
            if board[i] == player_num or capbool or movbool:
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
                    if board[j] == 0 and not capbool:
                        move1 = coords[:]
                        move1.append(j)
                        moves.append(move1)
                    if board[j] * player_num < 0:
                        if j % 8 == 0 or j % 8 == 7 or not -1 < j + move < 64:
                            continue
                        if board[j + move] == 0:
                            if j + move in coords:
                                continue

                            move1 = coords[:]
                            move1.append(j + move)
                            capture.append(move1)

                            move2 = coords[:]
                            move2.append(j + move)
                            moves.append(move2)

            elif board[i] * player_num == 2 and len(steps) == 2:
                queens.append([i])

        if len(capture) != 0:
            further_captures = Board.get_valid_moves(board, capture, steps, player_num, False, True)
            moves.extend(further_captures)

        if len(queens) != 0:
            queen_moves = Board.get_valid_moves(board, queens, [9, -7, 7, -9], player_num, True, False)
            moves.extend(queen_moves)
        return moves

    @staticmethod
    def play_move(board, move, player):
        piece_i = move[0]
        final_pos = move[-1]
        if len(move) == 2 and abs(piece_i - final_pos) < 10:
            # single move
            board[final_pos] = board[piece_i]
            board[piece_i] = 0
        elif len(move) == 2:
            # single move capture
            board[final_pos] = board[piece_i]
            board[piece_i] = 0
            board[(piece_i + final_pos) // 2] = 0
        else:
            # multiple captures
            board[final_pos] = board[piece_i]
            board[piece_i] = 0
            for i in range(len(move) - 1):
                start, end = move[i], move[i + 1]
                board[(start + end) // 2] = 0

        lastrow = {1: [1, 3, 5, 7], 0: [56, 58, 60, 62]}
        true_player = {0: -1, 1: 1}

        for i in lastrow[player]:
            if board[i] == true_player[player]:
                board[i] *= 2

        return board
