import random

class ZobristHash:

    def __init__(self, player_no):
        self.mask = 18446744073709551615 # (1 << 64) - 1
        self.bit = 18446744073709551616# 1 << 64
        self.no = player_no

        self.index = [0, 0, 0, 1, 0, 2, 0, 3,
                      4, 0, 5, 0, 6, 0, 7, 0,
                      0, 8, 0, 9, 0,10, 0,11,
                      12, 0,13, 0,14, 0,15,0,
                      0,16, 0,17, 0,18, 0,19,
                      20, 0,21, 0,22, 0,23,0,
                      0,24, 0,25, 0,26, 0,27,
                      28, 0,29, 0,30, 0,31, 0]

        self.dct = {1: [8573464455728772410, 3812234814380220568, 1324594347823164713, 1415888276376246394,
                        7628498578705963513, 3251181100259143949, 2011175603378478192, 1814811465737317951,
                        1026664323836933638, 4249613480748690878, 8760903906780171258, 2074993730180278109,
                        7018108001008431556, 3416855274766204696, 1249894347292460021, 3433736708224924975,
                        7632327504783926002, 5250908856926993007, 3030290256790925825, 2773908644794671833,
                        7507019478074540036, 2427499510710257943, 1255367649140085011, 4526452059045562071,
                        2816405704667043345, 1548834041994514577, 9175097590187062845, 6296047408621801026,
                        7882019727226636975, 2695556518135825626, 3896401531898343422, 7400640296330047349]
,
                   -1: [7322525052012529283, 2477505990638341500, 525164982438141739, 4297508004819492468,
                       6408993884371846203, 8535856506123290134, 7036646721306772305, 6819642087692266660,
                       5408412974186471519, 9083645782218586927, 4310808062787811460, 6954279156735262827,
                       4678154234807455438, 4626997667804171021, 563810470702089106, 6492125308037528348,
                       549564207874190386, 2321996661200153774, 1922705839576797275, 3347690267642640486,
                       7338690412295539367, 3585382545871967523, 1365651218219765096, 5568531096724902386,
                       5456956418087735024, 1419057440191735250, 5682755804351627995, 344152752702012389,
                       2751928036851702068, 2340734466004296909, 6930086149625337008, 4287950634287167476],

                   2:[7760926987693138769, 1629418641313836275, 5907976995659974996, 7055826624154025682,
                       5127904700630396533, 7316040588247835686, 1870305476313065791, 5570653253553015254,
                       1409551517455409501, 5085129967110008172, 3845689998309754573, 2628005957658688404,
                       7766729029397063546, 6179905958483473184, 7520385814978083616, 4728279702429595913,
                       736544311276818485, 3323590375268776473, 7550597215871515710, 8463775596094793534,
                       2128222326266384284, 6988506098640003860, 6671730875558230449, 4170130961478212686,
                       3220532224339531231, 5461140274014563165, 5738121763942310963, 5928350885688129051,
                       755455412398629887, 8430875935296131474, 8555373573191522400, 9083857704444783530],

                   -2:[7618822500843624311, 522700114800316290, 287673607482686095, 8778733082052786750,
                       5933220884983285812, 989183962252030140, 8902825581283107810, 3632187009114778099,
                       6047639167262524646, 8267793188302926323, 6195008040449284743, 5490842790599340239,
                       5481370001054868785, 1197526143723433518, 6620194874457431528, 4291667377317687362,
                       2980819284206867803, 8095340087023281401, 2141608418902034088, 7843968519971785766,
                       2279794173252421854, 2627956654317435275, 971175716439909999, 9161202889319190023,
                       5923838895826636383, 2965197430475113308, 1733009468774949027, 4116680940335399918,
                       2694927007650900820, 7355143655687592914, 3766175214532342844, 3005749888752320977]
                    }


        self.start_pos = 6923587450116205105


    def update_hash(self, hash, move, board, player):
        hash &= self.mask
        first = move[0]
        end_token = board[first]
        update = self.dct[end_token][self.index[first]]
        for i in range(len(move)-1):
            start, end = move[i], move[i+1]
            if abs(start - end) > 10:
                mid = (start + end)//2
                piece_at_location = board[mid]
                if piece_at_location != 0 and piece_at_location != 1:
                    index = self.index[mid]
                    update ^= self.dct[piece_at_location][index]

        last_pos = self.index[move[-1]]
        if end_token == 1 and last_pos in [1,3,5,7]:
            update ^= self.dct[2][last_pos]
        elif end_token == -1 and last_pos in [56,58,60,62]:
            update ^= self.dct[-2][last_pos]
        else:
            update ^= self.dct[end_token][last_pos]

        return hash ^ update | (1 - player) * self.bit


    def calculate_hash(self, board, player):
        start = 0
        for i in range(64):
            key = board[i]
            if key == 0 or key == 1:
                continue
            else:
                index = self.index[i]
                start ^= self.dct[key][index]
        return start | player * self.bit


if __name__ == "__main__":
    z = ZobristHash(1)
    board1 = [0, 5, 0, 5, 0, 5, 0, 5,
              5, 0, 5, 0, 5, 0, 5, 0,
              0, 5, 0, 5, 0, 5, 0, 5,
              1, 0, 1, 0, 1, 0, 1, 0,
              0, 1, 0, 1, 0, 1, 0, 1,
              3, 0, 3, 0, 3, 0, 3, 0,
              0, 3, 0, 3, 0, 3, 0, 3,
              3, 0, 3, 0, 3, 0, 3, 0]
    print(z.calculate_hash(board1, 0))
    #
    # board2 = [0, 5, 0, 5, 0, 5, 0, 5,
    #           5, 0, 1, 0, 5, 0, 5, 0,
    #           0, 5, 0, 5, 0, 5, 0, 5,
    #           1, 0, 1, 0, 1, 0, 1, 0,
    #           0, 3, 0, 5, 0, 1, 0, 1,
    #           3, 0, 1, 0, 3, 0, 3, 0,
    #           0, 3, 0, 3, 0, 3, 0, 3,
    #           3, 0, 3, 0, 3, 0, 3, 0]
    # move = [42, 33]
    # hash = z.calculate_hash(board1,0)
    # hash1 = z.update_hash(hash, move, board1,0)
    # hash2 = z.calculate_hash(board2,1)


