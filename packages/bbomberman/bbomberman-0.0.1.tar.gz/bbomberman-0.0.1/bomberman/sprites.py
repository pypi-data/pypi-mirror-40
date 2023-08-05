from PyQt5.QtGui import QImage
from bomberman.game import *

WALL = QImage('sprites/ceil_wall.png')
GRASS = QImage('sprites/ceil_grass.png')
BOMB = [QImage('sprites/bomb0.png'),
        QImage('sprites/bomb1.png'),
        QImage('sprites/bomb2.png'),
        QImage('sprites/bomb3.png')]
RED_PLAYER = QImage('sprites/red_player.png')
BLUE_PLAYER = QImage('sprites/blue_player.png')
EXPLOSION = QImage('sprites/explosion.png')

SPRITES = {Ceil.WALL: WALL, Ceil.EMPTY: GRASS}
PLAYERS = {0: RED_PLAYER, 1: BLUE_PLAYER}
