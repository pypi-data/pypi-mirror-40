import socket
import sys
import pickle
from bomberman import game, sprites
from bomberman.communications import *
from threading import Thread
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter


class GameWindow(QMainWindow):
    def __init__(self, addr):
        super().__init__()
        self.initUI()
        self.time = 0
        self.server_address = ("localhost", 7400)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 7401 to be changed
        self.sock.bind(addr)
        self.game = game.Game()
        self.pressedKeys = set()
        self.id = 0

        network_tread = Thread(target=self.talk_with_server)
        network_tread.start()

        timer = QTimer(self)
        timer.timeout.connect(self.act)
        timer.setInterval(30)
        timer.start()

    def get_init_message(self):
        self.sock.sendto(b'init', self.server_address)

        recv_data, address = self.sock.recvfrom(2048)
        answer = pickle.loads(recv_data)
        self.game.map = answer.map
        self.id = answer.id

    def form_player_message(self):
        message = PlayerMessage()
        message.id = self.id

        if Qt.Key_Right in self.pressedKeys:
            message.action.add(PlayerAction.RIGHT)
        if Qt.Key_Left in self.pressedKeys:
            message.action.add(PlayerAction.LEFT)
        if Qt.Key_Up in self.pressedKeys:
            message.action.add(PlayerAction.UP)
        if Qt.Key_Down in self.pressedKeys:
            message.action.add(PlayerAction.DOWN)

        if Qt.Key_Space in self.pressedKeys:
            message.try_place_bomb = True

        return message

    def process_data(self, data):
        self.game.players = data.players
        self.game.bombs = data.bombs
        self.game.explosions = data.explosions

    def talk_with_server(self):
        self.get_init_message()

        while True:
            raw_data = self.form_player_message()
            data = pickle.dumps(raw_data)
            self.sock.sendto(data, self.server_address)

            recv_data, address = self.sock.recvfrom(2048)
            self.process_data(pickle.loads(recv_data))

            # print(data)

    def initUI(self):
        self.setGeometry(100, 100, 64 * 11, 64 * 11)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_game(qp)
        qp.end()

    def draw_game(self, qp):
        for x in range(self.game.map_size()):
            for y in range(self.game.map_size()):
                qp.drawImage(self.game.cell_size * x,
                             self.game.cell_size * y,
                             sprites.SPRITES[self.game.get_ceil(x, y)])

        for bomb in self.game.bombs:
            qp.drawImage(bomb.x * self.game.cell_size,
                         bomb.y * self.game.cell_size,
                         sprites.BOMB[bomb.time_left % 4])

        for player in self.game.players:
            qp.drawImage(player.x, player.y, sprites.PLAYERS[player.id])

        for explosion in self.game.explosions:
            qp.drawImage(explosion.x * self.game.cell_size,
                         explosion.y * self.game.cell_size,
                         sprites.EXPLOSION)

    def act(self):
        self.time += 1
        self.update()

    def keyPressEvent(self, e):
        self.pressedKeys.add(e.key())

    def keyReleaseEvent(self, e):
        self.pressedKeys.remove(e.key())


if __name__ == "__main__":
    addr = ("localhost", int(input("введите порт")))
    app = QApplication(sys.argv)
    w = GameWindow(addr)
    sys.exit(app.exec_())