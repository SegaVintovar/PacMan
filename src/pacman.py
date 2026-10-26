
import pygame
from .config import GameConfig
from .cell import Cell
from .map import Map
from .creature import Creature

TILE = 64

_key_directions: dict[str, tuple[int, int]] = {
    'W': (0, -1),
    'D': (1, 0),
    'S': (0, 1),
    'A': (-1, 0)
}

TILE = 64

class Pacman(Creature):
    def __init__(self, map: Map, config: GameConfig) -> None:
        # initially spawn column is as centralized as possible
        self.x: int = int(config.width / 2)
        self.y: int = int(config.height / 2)
        self.map = map
        self.lives: int = config.lives
        self.points: int = 0
        self._direction: str = 'A'
        self.sprite = pygame.image.load(
            f"src/assets/sprites/pacman_{self._direction}_wide.png",
            ).convert_alpha()
        self.rect: pygame.Rect = pygame.Rect(self.x, self.y, 44, 44)
        self.measure_spawn()

    def spawn(self, screen: pygame.Surface) -> None:
        cell: Cell = self.map.get_cel_by_coords(self.x, self.y)
        if not (self.rect.x, self.rect.y) == cell.position:
            self._move()
        screen.blit(self.sprite,
                    (self.rect.left,
                     self.rect.bottom + self.map.height))

    """Creating an escapable point for pac-man.
       in case of an odd amount it is a right spawn
       within the center unless the cell represents
       as a 42-grid."""
    def measure_spawn(self) -> None:
        row_mid: int = int(self.map.width / 2) - 1
        col_mid: int = int(self.map.height / 2) - 1
        self.rect.left += col_mid * TILE
        self.rect.bottom += row_mid * TILE
        print(f"row: {self.y}\ncol: {self.x}")

    def _move(self) -> None:
        cell: Cell = self.map.get_cel_by_coords(self.x, self.y)
        x, y = cell.position
        direction: tuple[int, int] = _key_directions[self._direction]
        if not self._bounce():
            self.rect.move_ip(direction)

    def _bounce(self) -> bool:
        cell: Cell = self.map.get_cel_by_coords(self.x, self.y)
        if cell.n and self._direction == 'W':
            return True
        if cell.e and self._direction == "D":
            return True
        if cell.s and self._direction == "S":
            return True
        if cell.w and self._direction == "A":
            return True
        return False

    def _out_bound(self) -> bool:
        if self._direction == 'A' and self.x == 0:
            return True
        if self._direction == 'W' and self.y == 0:
            return True
        if self._direction == 'D' and self.x == self.map.width - 1:
            return True
        if self._direction == 'S' and self.y == self.map.height - 1:
            return True
        return False

    def update_direction(self, char: str) -> None:
        self._direction = char
        self.sprite = pygame.image.load(
            f"src/assets/sprites/pacman_{self._direction}_wide.png"
            ).convert_alpha()
        if not self._out_bound():
            row, col = _key_directions[char]
            self.x += row
            self.y += col
        self._move()
