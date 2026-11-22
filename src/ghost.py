from .creature import Creature
import pygame
import random
from .cell import Cell
from .constants import GHOSTS, SPEEDS, GHOST_DIRECTIONS, GHOST_COWARD_TIME
from .config import GameConfig
from .map import Map
from .pacman import Pacman
from .spriteBank import SpriteBank
from .timer import Timer
from enum import Enum
from typing import Optional
# from .paths import ASSETS_DIR
from .pathfinder import Pathfinder


class behavior(Enum):
    chasing = 0,
    blocking = 1,
    wandering = 2,
    cowardish = 3


class Ghost(Creature):
    def __init__(self, name: str, map: Map, config: GameConfig) -> None:
        # self.name = name
        super().__init__(name, (0, 0))
        self.map = map
        self.config = config
        self._direction: str = "left"
        self.eaten: bool = False
        self.being_coward: bool = False
        pussy_timer: Timer = Timer(GHOST_COWARD_TIME)
        self.pussy_timer: Timer = pussy_timer
        self._coward_switch: int = 0
        self._coward_color: str = "blue"
        self._sprite_id: str = f"{self.name}-{self._direction}"
        self.rect: pygame.Rect = self._create_rect()
        self.rect.center = self._cell_center(None)
        self.sprite: pygame.Surface = SpriteBank.get_sprite("ghost",
                                                            self._sprite_id)
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

    def get_eaten(self, _finder: Pathfinder) -> None:
        self.eaten = True
        self._sprite_id = f"eyes-{self._direction}"
        self.sprite = SpriteBank.get_sprite("ghost", self._sprite_id)
        sx, sy = self.start
        self.path = _finder.build_path(
                           _finder.map.map[self.cell_y][self.cell_x],
                           _finder.map.map[sy][sx])

    def fear_paccie(self) -> None:
        self.being_coward = True
        # start_timer() does nothing when the timer already runs,
        # so reset first: a second super-pacgum gives a full new period
        self.pussy_timer.reset()
        self.pussy_timer.start_timer()
        self._update_pic()

    def disrespect_paccie(self) -> None:
        self.being_coward = False
        self._update_pic()
        self.pussy_timer.reset()

    def _switch_coward_color(self) -> str:
        if not self.being_coward:
            return ""
        if self.pussy_timer.time_since_start() >= (GHOST_COWARD_TIME / 3) * 2:
            self._coward_switch += 1
            if self._coward_switch % 2 == 1:
                return "white"
            else:
                return "blue"
        return "blue"

    def _update_pic(self) -> None:
        start_x, start_y = self.start
        at_home = self.cell_x == start_x and self.cell_y == start_y
        if self.eaten and at_home:
            # an eaten ghost (only eyes) made it back: it is normal again
            self.rect.center = self._cell_center(self.start)
            self.eaten = False
            self.being_coward = False
            self.path = []
        if self.eaten:
            self._sprite_id = f"eyes-{self._direction}"
        else:
            self._sprite_id = (f"{self.name}-{self._direction}"
                               if not self.being_coward
                               else
                               f"frightened-{self._switch_coward_color()}")
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
        dir_update: tuple[int, int] = GHOST_DIRECTIONS[self._direction]
        ux, uy = dir_update
        if self.map.off_grid(self.cell_x + ux, self.cell_y + uy):
            return True
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

    # @staticmethod
    # def pick_dir(cell: Cell, next_cell: Cell) -> tuple[int, int]:
    #     def one(v: int) -> int:
    #         if v == 0:
    #             return 0
    #         elif v > 0:
    #             return 1
    #         else:
    #             return -1
    #     curr = cell.grid_coord
    #     target = next_cell.grid_coord
    #     delta_x = target[0] - curr[0]
    #     delta_y = target[1] - curr[1]
    #     if abs(one(delta_x)) == abs(one(delta_y)):
    #         if delta_y != 0:
    #             delta_x = 0
    #         else:
    #             if delta_x == 0:
    #                 delta_x == 1
    #     return (one(delta_x), one(delta_y))
    @staticmethod
    def pick_dir(cell: Cell, next_cell: Cell,
                 fallback: str = "left") -> tuple[int, int]:
        """Return a unit step (dx, dy) leading from cell towards next_cell.

        The result is always one of the four valid directions:
        (0, -1) up, (1, 0) right, (0, 1) down, (-1, 0) left.
        If both cells are the same (nothing to move towards), the step of
        the fallback direction is returned instead.
        """
        def sign(v: int) -> int:
            """Return -1, 0 or 1 depending on the sign of v."""
            if v == 0:
                return 0
            return 1 if v > 0 else -1

        delta_x = next_cell.grid_coord[0] - cell.grid_coord[0]
        delta_y = next_cell.grid_coord[1] - cell.grid_coord[1]

        if delta_x == 0 and delta_y == 0:
            # same cell: there is no direction to pick, keep going as before
            return GHOST_DIRECTIONS.get(fallback, GHOST_DIRECTIONS["left"])
        if delta_y != 0:
            # vertical wins on diagonals, so we never return (1, 1)
            return (0, sign(delta_y))
        return (sign(delta_x), 0)

    def check(self,
              pacman: Pacman | None,
              finder: Pathfinder,
              extra: str = ""
              ) -> bool:
        directions: dict[int, str] = {
            (0, -1): "up",
            (1, 0): "right",
            (0, 1): "down",
            (-1, 0): "left"
        }
        # the timer of a ghost that is not scared was never started, then
        # time_since_start() is the uptime of the whole program: only
        # look at it while the ghost is really scared
        if (self.being_coward and
                self.pussy_timer.time_since_start() >= GHOST_COWARD_TIME):
            self.disrespect_paccie()

        if self._at_destination():
            if extra:
                self._pick_random_dest()
            elif self.path:
                # path[0] is the next cell (the own cell is not in there)
                next_cell = self.path.pop(0)
                picked = self.pick_dir(
                    self.map.map[self.cell_y][self.cell_x],
                    next_cell,
                    self._direction)
                self._direction = directions[picked]
                self._set_destination()
            # always refresh the picture: this is also where an eaten
            # ghost notices it is back home and becomes normal again
            self._update_pic()
        if self.rect.colliderect(pacman.rect):
            if self.eaten:
                # only the eyes are left, they pass through pacman
                pass
            elif self.being_coward:
                pacman.points += self.config.points_per_ghost
                self.get_eaten(finder)
            elif pacman.invincible:
                # cheat mode: ghost touches pacman, nothing happens
                pass
            else:
                pacman.die()
                self.pussy_timer.reset()
                self.disrespect_paccie()
                self.measure_spawn()
                self.path = []
                self._destination = self._cell_center(None)
                return True
        cx, cy = self.rect.center
        tx, ty = self._destination

        speed: float = (SPEEDS["ghost"]
                        if not self.being_coward else SPEEDS["ghost_coward"])
        if self.eaten:
            speed = SPEEDS["ghost_eaten"]
        step_x = max(-speed, min(speed, tx - cx))
        step_y = max(-speed, min(speed, ty - cy))
        self.rect.move_ip(step_x, step_y)
        return False
