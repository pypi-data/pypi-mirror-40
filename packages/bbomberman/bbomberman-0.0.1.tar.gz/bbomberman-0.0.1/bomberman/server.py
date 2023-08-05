import socket
import time
import pickle
from bomberman import game
from threading import Thread
from bomberman.communications import *


class PlayerData:
    def __init__(self, my_id):
        self.id = my_id
        self.action = set()
        self.try_place_bomb = False


class Server:
    def __init__(self):
        self.GAME_RATE = 0.02
        self.ADDRESS = ("localhost", 7400)
        self.game = game.Game()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.ADDRESS)
        self.next_id = 0

        self.players = dict()
        self.players[0] = PlayerData(0)
        self.players[1] = PlayerData(1)
        self.load_game()

        print("Settled at " + self.ADDRESS[0] + ":" + str(self.ADDRESS[1]))

    def run(self):
        act_thread = Thread(target=self.update)
        act_thread.start()

        self.listen()

    def load_game(self):
        with open("map.txt", "rb") as fh:
            self.game = pickle.load(fh)
        return None

    # unused?
    def is_blast_intersect(self, explosion, obj):
        return not ((explosion.X + 1) * self.game.cell_size < obj.X or
                    obj.X + self.game.cell_size < explosion.X * self.game.cell_size or
                    (explosion.Y + 1) * self.game.cell_size < obj.Y or
                    obj.Y + self.game.cell_size < explosion.Y * self.game.cell_size)

    def update(self):
        while True:
            time.sleep(self.GAME_RATE)
            self.game.act()

            for player in self.players.values():
                if PlayerAction.DOWN in player.action:
                    self.game.move_player(player.id, 0, 1)
                if PlayerAction.UP in player.action:
                    self.game.move_player(player.id, 0, -1)
                if PlayerAction.RIGHT in player.action:
                    self.game.move_player(player.id, 1, 0)
                if PlayerAction.LEFT in player.action:
                    self.game.move_player(player.id, -1, 0)

                if player.try_place_bomb:
                    self.game.try_place_bomb(player.id)

                player.action = set()
                player.try_place_bomb = False

    def process_player(self, data):
        self.players[data.id].action = data.action
        self.players[data.id].try_place_bomb = data.try_place_bomb

    def handle_connection(self, *args):
        raw_data, address = args[0], args[1]
        if raw_data == b'init':
            answer = InitMessage()
            answer.map = self.game.map
            answer.id = self.next_id
            self.next_id += 1
            self.sock.sendto(pickle.dumps(answer), address)
        else:
            data = pickle.loads(raw_data)
            self.process_player(data)

            answer = ServerAnswer()
            answer.bombs = self.game.bombs
            answer.explosions = self.game.explosions
            answer.players = self.game.players
            self.sock.sendto(pickle.dumps(answer), address)

    def listen(self):
        while True:
            raw_data, address = self.sock.recvfrom(2048)
            handle = Thread(target=self.handle_connection,
                            args=(raw_data, address))
            handle.start()


if __name__ == "__main__":
    server = Server()
    server.run()
