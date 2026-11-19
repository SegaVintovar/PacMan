from .creature import Creature
import pygame
import random
from .cell import Cell
from .constants import GHOSTS, SPEED, GHOST_DIRECTIONS
from .config import GameConfig
from .map import Map
from .pacman import Pacman
from .spriteBank import SpriteBank
from enum import Enum
from typing import Optional
from .paths import ASSETS_DIR
from .pathfinder import Pathfinder


class behavior(Enum):
    chasing = 0,
    blocking = 1,
    wandering = 2,
    cowardish = 3


class Ghost(Creature):
    def __init__(self, name: str, map: Map, config: GameConfig) -> None:
        self.name: str = name
        self.map = map
        self.config = config
        self._direction: str = "left"
        self.eaten: bool = False
        self.pussy_mod: bool = False
        self.start: tuple[int, int]
        self._sprite_id: str = f"{self.name}-{self._direction}"
        self.rect: pygame.Rect = self._create_rect()
        self.rect.center = self._cell_center(None)
        self.sprite: pygame.Surface = SpriteBank.get_sprite("ghost", self._sprite_id)
        self._destination: tuple[int, int] = self._cell_center(None)
        self.path: list[Cell] = []

    def _set_destination(self) -> None:
        if self._direction not in GHOST_DIRECTIONS:
            print(f"skipping '{self._direction}'")
            return
        col, row = GHOST_DIRECTIONS[self._direction]
        self.cell_y += row
        self.cell_x += col
        centered: tuple[int, int] = self._cell_center(None)
        destx, desty = centered
        self._destination = (destx, desty)

    def measure_spawn(self) -> None:
        coords: tuple[str, str] = GHOSTS[self.name][1]
        _x, _y = coords
        self.cell_x = self.config.width - 1 if not _x == 'left' else 0
        self.cell_y = self.config.height - 1 if not _y == 'top' else 0
        self.start = (self.cell_x, self.cell_y)
        self.rect.center = self._cell_center(None)

    def get_eaten(self) -> None:
        self._sprite_id = f"eyes-{self._direction}"
        self.sprite = SpriteBank.get_sprite("ghost", self._sprite_id)
        self.rect = self.sprite.get_rect(topleft=self.start)

    def fear_paccie(self) -> None:
        self.pussy_mod = True
        self._update_pic()

    def disrespect_paccie(self) -> None:
        self.pussy_mod = False
        self._update_pic()

    def _update_pic(self) -> None:
        self._sprite_id: str = (f"{self.name}-{self._direction}"
                                if not self.pussy_mod
                                else f"frightened-blue")

        self.sprite = SpriteBank.get_sprite("ghost", self._sprite_id)

    def _create_rect(self) -> pygame.Rect:
        coords: tuple[str, str] = GHOSTS[self.name][1]
        _x, _y = coords
        self.cell_x = self.config.width - 1 if not _x == 'left' else 0
        self.cell_y = self.config.height - 1 if not _y == 'top' else 0
        self.start = (self.cell_x, self.cell_y)
        return pygame.Rect((self.cell_x, self.cell_y), (44, 44))

    def _pick_random_dest(self) -> None:
        directions: dict[int, str] = {
            0: "up",
            1: "right",
            2: "down",
            3: "left"
        }
        picked: int = random.randrange(0, 4)
        self._direction = directions[picked]
        if not self._bounce(None):
            self._set_destination()

    def _bounce(self, char: Optional[str]) -> bool:
        # def _bounce(self) -> bool:
        cell: Cell = self.map.get_cel_by_coords(self.cell_x, self.cell_y)
        if not cell:
            return True
        if self._direction == "up" and cell.n:
            return True
        if self._direction == "right" and cell.e:
            return True
        if self._direction == "down" and cell.s:
            return True
        if self._direction == "left" and cell.w:
            return True
        return False

    def check(self, pacman: Pacman | None, extra: str = "") -> bool:
        def pick_dir(cell: Cell, next_cell: Cell) -> tuple[int, int]:
            def one(v: int) -> int:
                if v == 0:
                    return 0
                elif v > 0:
                    return 1
                else:
                    return -1
            curr = cell.grid_coord
            target = next_cell.grid_coord
            delta_x = target[0] - curr[0]
            delta_y = target[1] - curr[1]
            if abs(one(delta_x)) == abs(one(delta_y)):
                delta_x = 0
            return (one(delta_x), one(delta_y))

        directions: dict[int, str] = {
            (0, -1): "up",
            (1, 0): "right",
            (0, 1): "down",
            (-1, 0): "left"
        }

        if self._at_destination():
            if not extra:
                if not self.path:
                    return False

                next_cell = self.path.pop(0)
                picked = pick_dir(
                    self.map.map[self.cell_y][self.cell_x], next_cell)
                self._direction = directions[picked]
                self._set_destination()
            else:
                self._pick_random_dest()
            self._update_pic()
            if self._bounce(None):
                return False
        if self.rect.colliderect(pacman.rect):
            if not self.pussy_mod:
                pacman.die()
                self.measure_spawn()
                self.path = []
                self._destination = self._cell_center(None)
                return True
            else:
                pacman.points += self.config.points_per_ghost
                self.get_eaten()
        cx, cy = self.rect.center
        tx, ty = self._destination

        speed: int = SPEED if not self.pussy_mod else SPEED//2
        step_x = max(-speed, min(speed, tx - cx))
        step_y = max(-speed, min(speed, ty - cy))
        self.rect.move_ip(step_x, step_y)
        return False
