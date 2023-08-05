class PlayerAction:
    NONE = 0
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class PlayerMessage:
    def __init__(self):
        self.id = 0
        self.action = set()
        self.try_place_bomb = False


class ServerAnswer:
    def __init__(self):
        self.players = []
        self.bombs = []
        self.explosions = []


class InitMessage:
    def __init__(self):
        self.map = 0
        self.id = 0
