import abc

class Agent(abc.ABC):

    def __init__(self, player_no : int):
        self.player_no = player_no

    @abc.abstractmethod
    def play(self, moves : list, board : list):
        pass