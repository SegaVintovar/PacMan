import pygame
from .config import GameConfig
from .cell import Cell
from .map import Map
from .creature import Creature
from pydantic_extra_types.coordinate import Coordinate
from .constants import TILE, KEY_DIRECTIONS, SPRIE_SIZE, SPEED
from typing import Optional

# lets make it move not by cells but by pixels
# by dividing coordinates in pixels by TILE
# we will get Cell position in the grid


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
        coord = (TILE - SPRIE_SIZE) // 2
        self.rect = self.sprite.get_rect(topleft=(coord, coord))
        self.measure_spawn()
        self._destination: tuple[int, int] = self._cell_center(None)
        self._origin: tuple[int, int] = self.rect
        self._pixel_moved: int = 0

    def spawn(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, self.rect)

    """Creating an escapable point for pac-man.
       in case of an odd amount it is a right spawn
       within the center unless the cell represents
       as a 42-grid."""
    def measure_spawn(self) -> None:
        row_mid: int = int(self.map.width / 2)
        col_mid: int = int(self.map.height / 2)
        self.cell_x, self.cell_y = col_mid, row_mid
        self.rect.center = self._cell_center(None)
        self._destination = self.rect.center

    def _try_next(self) -> bool:
        if self._bounce(None):
            return False
        self._set_destination()
        return True

    def get_direction_destination(self, chr: str | None) -> tuple[int, int]:
        print(f"the chosen direction: {chr}")
        direction: tuple[int, int] = KEY_DIRECTIONS[self._direction
                                                    if chr is None
                                                    else chr.capitalize()]
        x, y = direction
        diff: tuple[int, int] = (self.cell_x + x, self.cell_y + y)
        coords: tuple[int, int] = self._cell_center(diff)
        return coords

    def _pass_pixel(self) -> None:
        if self._pixel_moved >= TILE:
            self._pixel_moved = SPEED
        else:
            self._pixel_moved += SPEED

    def _set_destination(self) -> None:
        col, row = KEY_DIRECTIONS[self._direction]
        self.cell_y += row
        self.cell_x += col
        centered: tuple[int, int] = self._cell_center(None)
        destx, desty = centered
        self._destination = (destx, desty)

    def check(self) -> None:
        if self._at_destination():
            self._origin = (self.rect.x, self.rect.y)
            if not self._try_next():
                return
        cx, cy = self.rect.center
        tx, ty = self._destination
        self._pass_pixel()
        if (self._pixel_moved > (TILE * 0.45) and
           self._pixel_moved < (TILE * 0.55)):
            self.sprite = pygame.image.load(
                f"src/assets/sprites/pacman_{self._direction}_closed.png"
                ).convert_alpha()
        elif (self._pixel_moved > (TILE * 0.2) and
              self._pixel_moved < (TILE * 0.8)):
            self.sprite = pygame.image.load(
                f"src/assets/sprites/pacman_{self._direction}_narrow.png"
                ).convert_alpha()
        else:
            self.sprite = pygame.image.load(
                f"src/assets/sprites/pacman_{self._direction}_wide.png"
                ).convert_alpha()
        step_x = max(-SPEED, min(SPEED, tx - cx))
        step_y = max(-SPEED, min(SPEED, ty - cy))
        self.rect.move_ip(step_x, step_y)

    def _bounce(self, char: Optional[str]) -> bool:
        cell: Cell = self.map.get_cel_by_coords(self.cell_x, self.cell_y)
        if char is not None:
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

    def _at_destination(self) -> bool:
        return self.rect.center == self._destination

    def update_direction(self, char: str) -> None:
        if self._bounce(char):
            return
        dx, dy = KEY_DIRECTIONS[char]
        self._direction = char
        if self._at_destination():
            self.cell_x += dx
            self.cell_y += dy
            self._destination = self._cell_center(None)
        self.sprite = pygame.image.load(
            f"src/assets/sprites/pacman_{char}_wide.png"
        ).convert_alpha()
