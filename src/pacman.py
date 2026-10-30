
import pygame
from .config import GameConfig
from .cell import Cell
from .map import Map
from .creature import Creature
from pydantic_extra_types.coordinate import Coordinate
from .constants import TILE, KEY_DIRECTIONS
from typing import Optional


class Pacman(Creature):
    def __init__(self, map: Map, config: GameConfig) -> None:
        # initially spawn column is as centralized as possible
        self.map = map
        self.lives: int = config.lives
        self.points: int = 0
        self._direction: str = 'A'
        self.sprite = pygame.image.load(
            f"src/assets/sprites/pacman_{self._direction}_wide.png",
            ).convert_alpha()
        self.rect = self.sprite.get_rect(topleft=(10, 10))
        self.measure_spawn()
        self._destination: tuple[int, int] = self._cell_center()
        self._interselected: str = None

    def spawn(self, screen: pygame.Surface) -> None:   # draw only
        screen.blit(self.sprite, self.rect)

    """Creating an escapable point for pac-man.
       in case of an odd amount it is a right spawn
       within the center unless the cell represents
       as a 42-grid."""
    def measure_spawn(self) -> None:
        row_mid: int = int(self.map.width / 2)
        col_mid: int = int(self.map.height / 2)
        self.cell_x, self.cell_y = col_mid, row_mid
        self.rect.center = self._cell_center()
        self._destination = self.rect.center

    def _try_next(self) -> bool:
        if self._bounce(None):
            return False
        self._set_destination()
        return True       

    def _set_destination(self) -> None:
        col, row = KEY_DIRECTIONS[self._direction]
        self.cell_y += row
        self.cell_x += col
        centered: tuple[int, int] = self._cell_center()
        destx, desty = centered
        self._destination = (destx, desty)

    def check(self) -> None:        # call once per frame
        if self._at_destination():
            if not self._try_next():
                return
        cx, cy = self.rect.center
        tx, ty = self._destination
        step_x = max(-2, min(2, tx - cx))
        step_y = max(-2, min(2, ty - cy))
        self.rect.move_ip(step_x, step_y)

    def _bounce(self, char: Optional[str]) -> bool:
        cell: Cell = self.map.get_cel_by_coords(self.cell_x, self.cell_y)
        if not char is None:
            if cell.n and char == 'W':
                return True
            elif cell.e and char == "D":
                return True
            elif cell.s and char == "S":
                return True
            elif cell.w and char == "A":
                return True
            else:
                return False
        else:
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


    def _cell_center(self) -> tuple[int, int]:
        return self.cell_x * TILE + TILE // 2, self.cell_y * TILE + TILE // 2

    def _at_destination(self) -> bool:
        return self.rect.center == self._destination

    def update_direction(self, char: str) -> None:
        if self._bounce(char):
            return
        #elif not self._at_direction() and self.rect.x == 0 or self.rect.y == 0:
        #    print("interselected during movement towards one direction") 
        dx, dy = KEY_DIRECTIONS[char]
        self._direction = char
        self.cell_x += dx
        self.cell_y += dy
        self._destination = self._cell_center()
        self.sprite = pygame.image.load(
            f"src/assets/sprites/pacman_{char}_wide.png"
        ).convert_alpha()
