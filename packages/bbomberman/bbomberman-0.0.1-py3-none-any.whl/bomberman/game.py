class Player:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.bomb_cooldown = 0


class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 2
        self.time_left = 60


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time_left = 20


class Ceil:
    EMPTY = 0
    WALL = 1
    PLAYER = 2


class Game:
    def __init__(self):
        self.players = {}
        self.bombs = []
        self.explosions = []
        self.map = []
        self.cell_size = 64
        self.player_speed = 3
        self.player_size = 40

    def map_size(self):
        return len(self.map)

    def set_ceil(self, value, x, y):
        self.map[x][y] = value

    def get_ceil(self, x, y):
        return self.map[x][y]

    def set_player(self, x, y, id):
        self.players[id] = Player(x, y, id)

    def _can_move(self, player, dx, dy):
        return self.map[
                   (player.x + dx) // self.cell_size][
                   (player.y + dy) // self.cell_size] == Ceil.EMPTY

    def _get_player_ceil(self, id):
        player = self.players[id]
        return (int((player.x + self.player_size // 2) // self.cell_size),
                int((player.y + self.player_size // 2) // self.cell_size))

    def _set_bomb(self, x, y):
        self.bombs.append(Bomb(x, y))

    def _blast(self, x, y, dx, dy, radius):
        for i in range(1, radius + 1):
            if self.map[x + dx * i][y + dy * i] == Ceil.WALL:
                break
            self.explosions.append(
                Explosion(x + dx * i, y + dy * i)
            )

    def _detonate(self, bomb):
        self.bombs.remove(bomb)
        self.explosions.append(Explosion(bomb.x, bomb.y))

        self._blast(bomb.x, bomb.y, 1, 0, bomb.radius)
        self._blast(bomb.x, bomb.y, 0, 1, bomb.radius)
        self._blast(bomb.x, bomb.y, -1, 0, bomb.radius)
        self._blast(bomb.x, bomb.y, 0, -1, bomb.radius)

    def act(self):
        for player in self.players:
            if player.bomb_cooldown > 0:
                player.bomb_cooldown -= 1

        for explosion in self.explosions:
            explosion.time_left -= 1
            if explosion.time_left <= 0:
                self.explosions.remove(explosion)

        for bomb in self.bombs:
            bomb.time_left -= 1
            if bomb.time_left <= 0:
                self._detonate(bomb)

    def try_place_bomb(self, id):
        player = self.players[id]
        if player.bomb_cooldown == 0:
            pos = self._get_player_ceil(id)
            self._set_bomb(pos[0], pos[1])
            player.bomb_cooldown = 60

    def move_player(self, id, dx, dy):
        player = self.players[id]
        if dy > 0:
            if self._can_move(player, 0,
                              (self.player_speed * dy) + self.player_size) and \
                    self._can_move(player, self.player_size,
                                   (self.player_speed * dy) + self.player_size):
                player.y += self.player_speed * dy

        if dy < 0:
            if self._can_move(player, 0, self.player_speed * dy) and \
                    self._can_move(player, self.player_size,
                                   self.player_speed * dy):
                player.y += self.player_speed * dy

        if dx > 0:
            if self._can_move(player,
                              (self.player_speed * dx) + self.player_size,
                              0) and \
                    self._can_move(player,
                                   (self.player_speed * dx) + self.player_size,
                                   self.player_size):
                player.x += self.player_speed * dx

        if dx < 0:
            if self._can_move(player, (self.player_speed * dx), 0) and \
                    self._can_move(player, self.player_speed * dx,
                                   self.player_size):
                player.x += self.player_speed * dx
