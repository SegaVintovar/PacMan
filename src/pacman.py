
import pygame
from .config import GameConfig
from .cell import Cell
from .map import Map
from .creature import Creature
from pydantic_extra_types.coordinate import Coordinate
from .constants import TILE, KEY_DIRECTIONS


_key_directions: dict[str, tuple[int, int]] = {
    'W': (0, -1),
    'D': (1, 0),
    'S': (0, 1),
    'A': (-1, 0)
}



class Pacman(Creature):
    def __init__(self, map: Map, config: GameConfig) -> None:
        # initially spawn column is as centralized as possible
        self.cell_x: int = -1
        self.cell_y: int = -1
        self.map = map
        self.lives: int = config.lives
        self.points: int = 0
        self._direction: str = 'A'
        self.sprite = pygame.image.load(
            f"src/assets/sprites/pacman_{self._direction}_wide.png",
            ).convert_alpha()
        # self.rect: pygame.Rect = pygame.Rect(self.cell_x, self.cell_y, 44, 44)
        self.rect = self.sprite.get_rect(topleft=(10, 44))
        self.measure_spawn()

    def spawn(self, screen: pygame.Surface) -> None:
        cell: Cell = self.map.get_cel_by_coords(self.cell_x, self.cell_y)
        if not (self.rect.x, self.rect.y) == cell.position:
            self._move()
        screen.blit(self.sprite, self.rect)

    """Creating an escapable point for pac-man.
       in case of an odd amount it is a right spawn
       within the center unless the cell represents
       as a 42-grid."""
    def measure_spawn(self) -> None:
        def get_avail_neighbours(map: Map, pos: Coordinate) -> Cell:
            """
            Looking for available neighbours
            """
            print("get available neighours")
            result: list[Cell] = []
            if (pos[1] + 1) < len(map.map) and map.map[pos[1] + 1][pos[0]].value != 15:
                result.append(map.map[pos[1] + 1][pos[0]])
            if (pos[0] + 1) < len(map.map[0]) and map.map[pos[1]][pos[0] + 1].value != 15:
                result.append(map.map[pos[1]][pos[0] + 1])
            if (pos[1] - 1) >= 0 and map.map[pos[1] - 1][pos[0]].value != 15:
                result.append(map.map[pos[1] - 1][pos[0]])
            if (pos[0] - 1) >= 0 and map.map[pos[1]][pos[0] - 1].value != 15:
                result.append(map.map[pos[1]][pos[0] - 1])
            return result[0]

        row_mid: int = int(self.map.width / 2)
        col_mid: int = int(self.map.height / 2)
        if self.map.map[col_mid][row_mid].value == 15:
            col_mid, row_mid = get_avail_neighbours(
                self.map, (col_mid, row_mid)).position
        self.rect.left += col_mid * TILE
        self.rect.bottom += row_mid * TILE
        self.cell_x = col_mid
        self.cell_y = row_mid

    def check_spawn(self) -> bool:
        obtained: Cell = self.map.get_cel_by_coords(self.cell_x, self.cell_y)
        if self._destination is None:
            x, y = obtained.creature_destination()
            current: tuple[int, int] = self.rect.x, self.rect.y
            cx, cy = current
            if not x == cx and y == cy:
                self._move()
                return False
        return True

    def _move(self) -> None:
        cell: Cell = self.map.get_cel_by_coords(self.cell_x, self.cell_y)
        x, y = cell.position
        direction: tuple[int, int] = _key_directions[self._direction]
        if (not self._bounce()
           and not self.rect.x == x and not self.rect.y == y):
            self.rect.move_ip(direction)
            # print(f"option {self._direction} is walled")

    def _bounce(self) -> bool:
        cell: Cell = self.map.get_cel_by_coords(self.cell_x, self.cell_y)
        print(f"options stats ({self.cell_x}, {self.cell_y}):")
        if cell.n and self._direction == 'W':
            return True
        elif cell.e and self._direction == "D":
            return True
        elif cell.s and self._direction == "S":
            return True
        elif cell.w and self._direction == "A":
            return True
        else:
            return False

    def _out_bound(self) -> bool:
        if self._direction == 'A' and self.cell_x == 0:
            return True
        if self._direction == 'W' and self.cell_y == 0:
            return True
        if self._direction == 'D' and self.cell_x == self.map.width - 1:
            return True
        if self._direction == 'S' and self.cell_y == self.map.height - 1:
            return True
        return False

    def update_direction(self, char: str) -> None:
        self._direction = char
        if not self._bounce():
            self.sprite = pygame.image.load(
                f"src/assets/sprites/pacman_{self._direction}_wide.png"
                ).convert_alpha()
            print(f"we can go there{char}")
            row, col = _key_directions[char]
            self.cell_x += row
            self.cell_y += col
        self._move()
