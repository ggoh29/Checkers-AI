from ZobristHash import ZobristHash

class Agent:

    def __init__(self, player_no):
        self.player_no = player_no
        self.zb = ZobristHash()
        self.hash = self.zb.start_pos

        self.moves = []
        self.other_moves = []