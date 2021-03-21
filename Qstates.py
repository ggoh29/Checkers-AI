import json
class Qstates:

    def __init__(self):
        self.discountRate = 0.95
        f = open("Qscores.txt")
        d = json.load(f)
        self.dct = {int(k1): {int(k2): v1 for k2, v1 in v.items()} for k1, v in d.items()}
        f.close()
        print(self.dct)


    def save_to_file(self):
        f = open("Qscores.txt", 'w')
        j = json.dumps(self.dct)
        f.write(j)
        f.close()

    def update_dct_bellman(self, moves0, moves1, result):
        # 0 for win, 1 for tie
        result_dct = {0 : 10, 1 : -2}
        i = 0
        sequence = []
        max_len = min(len(moves0), moves1)
        while i < max_len:
            if i < len(moves0):
                sequence.append(moves0[i])
            if i < len(moves1):
                sequence.append(moves1[i])
            i += 1

        state_before_winning = sequence[-2]
        winning_state = sequence[-1]






if __name__ == "__main__":
    q = Qstates()
    q.save_to_file()