from .creature import Creature
import pygame
import random
from .cell import Cell
from .constants import GHOSTS, SPEED
from .config import GameConfig
from .map import Map
from enum import Enum


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
        self.start: tuple[int, int] = ()
        self.rect: pygame.Rect = self._create_rect()
        self.rect.center = self._cell_center(None)
        self.sprite: pygame.Surface = self._upload_pic()
        self.pussy_mod: bool = False
        self._destination: tuple[int, int] = self._cell_center(None)
        self._direction: str = "left"

    def _upload_pic(self) -> pygame.Surface:
        return pygame.image.load(
            f"src/assets/sprites/ghost_{GHOSTS[self.name][0]}_down.png",
            ).convert_alpha()

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
        picked: int = random.randrange(0, 3)
        self._direction = directions[picked]
        print(f"{self.name} is going {self._direction}")
        if not self._bounce():
            self._set_destination()
        else:
            print(f"boink by {self.name}")

    def _bounce(self) -> bool:
        cell: Cell = self.map.get_cel_by_coords(self.cell_x, self.cell_y)
        if self._direction == "up" and cell.n:
            return True
        if self._direction == "right" and cell.e:
            return True
        if self._direction == "down" and cell.s:
            return True
        if self._direction == "left" and cell.w:
            return True
        return False

    def retreat_spawn_point() -> None:
        ...

    def check(self) -> None:
        if self._at_destination() or self._destination is None:
            self._pick_random_dest()
            if self._bounce():
                return
        cx, cy = self.rect.center
        tx, ty = self._destination
        step_x = max(-SPEED, min(SPEED, tx - cx))
        step_y = max(-SPEED, min(SPEED, ty - cy))
        self.rect.move_ip(step_x, step_y)
        ...

    def _out_bound(self, map: Map) -> bool:
        ...
    # ids are from 0 till 3(inclusive)
