
import json
class Qstates:

    def __init__(self):
        self.discountRate = 0.95
        self.alpha = 0.95
        f = open("Qscores.txt")
        d = json.load(f)
        self.dct = {int(k1): {int(k2): v1 for k2, v1 in v.items()} for k1, v in d.items()}
        f.close()


    def save_to_file(self):
        f = open("Qscores.txt", 'w')
        j = json.dumps(self.dct)
        f.write(j)
        f.close()

    def update_dct(self, sequence, result):
        # 1 for win, 0 for tie, -1 for taking too long
        result_dct = {1 : 10, 0 : -2, -1 : 0}

        state_before_winning = sequence[-2]
        winning_state = sequence[-1]
        if state_before_winning not in self.dct:
            self.dct[state_before_winning] = {}
        if winning_state not in self.dct[state_before_winning]:
            self.dct[state_before_winning][winning_state] = result_dct[result]
        side = 1 - result
        for i in range(len(sequence)-2, 0, -1):
            self.__bellman(sequence[i-1], sequence[i], side)
            side = 1 - side


    def __bellman(self, state, next_state, side):
        if state not in self.dct:
            self.dct[state] = {}
        if next_state not in self.dct[state]:
            self.dct[state][next_state] = 0

        cur_q = self.dct[state][next_state]
        self.dct[state][next_state] = cur_q + self.alpha * ((- self.__get_max_next(state, side)) - cur_q)


    def __get_max_next(self, state, side):
        # Best state for 0 is worst state for 1 so reverse it?
        side_dct = {0: max, 1: min}
        mx = 0
        for key in self.dct[state]:
            if key in self.dct:
                dct = self.dct[key]
                dct_mx_key = side_dct[side](dct, key=lambda x: dct[x])
                mx = side_dct[side](mx, dct[dct_mx_key])
        return self.discountRate * mx

