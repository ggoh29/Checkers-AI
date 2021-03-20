from ZobristHash import ZobristHash

class Agent:

    def __init__(self):
        self.zb = ZobristHash()
        self.hash = self.zb.start_pos