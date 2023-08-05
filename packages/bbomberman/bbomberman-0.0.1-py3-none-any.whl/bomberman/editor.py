import sys
import pickle
from bomberman import game, sprites
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QPainter


class Cursor:
    wall = (game.Ceil.WALL, sprites.WALL)
    player_one = (game.Ceil.PLAYER, sprites.RED_PLAYER, 0)
    player_two = (game.Ceil.PLAYER, sprites.BLUE_PLAYER, 1)


class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mouse_pos = QPoint()
        self.setMouseTracking(True)
        self.game = game.Game()
        self.cursor = Cursor.wall
        self.create_map(11)

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.setInterval(30)
        timer.start()

        action_save = QAction("Save map", self)
        action_save.setShortcut('Ctrl+S')
        action_save.setStatusTip('Save map')
        action_save.triggered.connect(self.save_game)

        self.statusBar()
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(action_save)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_0:
            self.cursor = Cursor.wall
        elif e.key() == Qt.Key_1:
            self.cursor = Cursor.player_one
        elif e.key() == Qt.Key_2:
            self.cursor = Cursor.player_two

    def save_game(self):
        with open("map.txt", "wb") as fh:
            pickle.dump(self.game, fh)

    def align(self, numb):
        return (numb // self.game.cell_size) * self.game.cell_size

    def create_map(self, size):
        game_map = []
        for x in range(size):
            line = []
            for y in range(size):
                if x == size - 1 or x == 0 or y == size - 1 or y == 0:
                    line.append(game.Ceil.WALL)
                else:
                    line.append(game.Ceil.EMPTY)
            game_map.append(line)

        self.game.map = game_map
        self.game.players.append(game.Player(64, 64, 0))
        self.game.players.append(game.Player(64 * 9, 64 * 9, 1))

    # unused
    def delete_all_instances(self, value):
        for x in range(self.map_size):
            for y in range(self.map_size):
                if self.game.get_ceil(x, y):
                    self.game.set_ceil(game.Ceil.EMPTY, x, y)

    def set_ceil(self, x, y):
        if self.game.get_ceil(x, y) == self.cursor[0]:
            self.game.set_ceil(game.Ceil.EMPTY, x, y)
        else:
            self.game.set_ceil(game.Ceil.WALL, x, y)

    def mousePressEvent(self, QMouseEvent):
        x = self.mouse_pos.x() // self.game.cell_size
        y = self.mouse_pos.y() // self.game.cell_size
        if self.cursor[0] == game.Ceil.WALL:
            self.set_ceil(x, y)
        elif self.cursor[0] == game.Ceil.PLAYER:
            self.game.set_player(self.mouse_pos.x(), self.mouse_pos.y(),
                                 self.cursor[2])

    def mouseMoveEvent(self, QMouseEvent):
        self.mouse_pos = QMouseEvent.pos()

    def initUI(self):
        self.setGeometry(100, 100, 64 * 11, 64 * 11)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_editor(qp)
        qp.end()

    def draw_editor(self, qp):
        for x in range(self.game.map_size()):
            for y in range(self.game.map_size()):
                sprite = sprites.SPRITES[self.game.get_ceil(x, y)]
                qp.drawImage(x * self.game.cell_size, y * self.game.cell_size,
                             sprite)

        for player in self.game.players:
            qp.drawImage(player.x, player.y, sprites.PLAYERS[player.id])

        qp.drawImage(self.align(self.mouse_pos.x()),
                     self.align(self.mouse_pos.y()),
                     self.cursor[1])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = EditorWindow()
    sys.exit(app.exec_())
