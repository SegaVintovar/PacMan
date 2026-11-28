import pygame
from .config import GameConfig
from .cell import Cell
from .map import Map
from .creature import Creature
from .spriteBank import SpriteBank
from .constants import TILE, KEY_DIRECTIONS, SPRIE_SIZE, SPEEDS
from typing import Optional
from .paths import ASSETS_DIR

SPRITES = ASSETS_DIR / "sprites"


class Pacman(Creature):
    def __init__(self, map: Map, config: GameConfig) -> None:
        # initially spawn column is as centralized as possible
        self.map = map
        self.lives: int = config.lives
        self.points: int = 0
        self._direction: str = 'A'
        self._next_direction: str = ''
        self._opening: str = "wide"
        self._sprite_id: str = f"{self._direction}-{self._opening}"
        self.sprite = SpriteBank.get_sprite("pacman", self._sprite_id)
        coord = (TILE - SPRIE_SIZE) // 2
        self.rect: pygame.Rect = self.sprite.get_rect(topleft=(coord, coord))
        self.measure_spawn()
        self._destination: tuple[int, int] = self._cell_center(None)
        self._origin: tuple[int, int] = self.rect.center
        self._pixel_moved: float = 0
        self.invincible = False

    """Creating an escapable point for pac-man.
       in case of an odd amount it is a right spawn
       within the center unless the cell represents
       as a 42-grid."""
    def measure_spawn(self) -> None:
        # cell_x is a column (width), cell_y is a row (height)
        x = self.map.width // 2
        y = self.map.height // 2
        if self.map.map[y][x].value == 15:
            x -= 1
        self.cell_x = x
        self.cell_y = y
        self.start = (self.cell_x, self.cell_y)
        self.rect.center = self._cell_center(None)
        self._destination = self.rect.center
        self._next_direction = ''

    def go_to_next_level(self, map: Map) -> None:
        self.map = map
        self.measure_spawn()

    def _update_pic(self) -> None:
        if (self._pixel_moved > TILE * 0.5 and
           self._pixel_moved <= TILE * 0.75):
            self._opening = "closed"
        elif ((self._pixel_moved <= TILE * 0.5 and
              self._pixel_moved > TILE * 0.25) or
                (self._pixel_moved > TILE * 0.75)):
            self._opening = "narrow"
        else:
            self._opening = "wide"
        self._sprite_id = f"{self._direction}-{self._opening}"
        self.sprite = SpriteBank.get_sprite("pacman", self._sprite_id)

    def _in_linear(self, new: str) -> bool:
        return (True if self._direction == 'W' and new == 'S'
                or self._direction == 'S' and new == 'W'
                or self._direction == 'D' and new == 'A'
                or self._direction == 'A' and new == 'D' else False)

    def _pass_pixel(self) -> None:
        if self._pixel_moved >= TILE:
            self._pixel_moved = SPEEDS["pacman"]
        else:
            self._pixel_moved += SPEEDS["pacman"]

    def _start_walking(self, direction: str) -> None:
        """Start walking one cell in the given direction.

        cell_x / cell_y always point to the cell we are walking to
        (or standing in), so we move them exactly ONE step here.
        """
        dx, dy = KEY_DIRECTIONS[direction]
        self._direction = direction
        self.cell_x += dx
        self.cell_y += dy
        self._destination = self._cell_center(None)

    def check(self, pacman: "Pacman | None" = None) -> bool:
        """Move pacman one frame. Called every frame by the level."""
        if self._at_destination():
            # we are standing in the middle of a cell: choose what to do.
            # 1. the turn the player asked for, if there is no wall there
            wanted = self._next_direction
            self._next_direction = ''
            if wanted and not self._bounce(wanted):
                self._start_walking(wanted)
            # 2. otherwise keep going straight, if there is no wall there
            elif not self._bounce(self._direction):
                self._start_walking(self._direction)
            # 3. wall in front of us: stand still
            else:
                return False
        speed = int(SPEEDS["pacman"])  # rect works with whole pixels
        cx, cy = self.rect.center
        tx, ty = self._destination
        self._pass_pixel()
        self._update_pic()
        # never step further than what is left to the destination
        step_x = max(-speed, min(speed, tx - cx))
        step_y = max(-speed, min(speed, ty - cy))
        self.rect.move_ip(step_x, step_y)
        return False

    def die(self) -> None:
        self.lives -= 1
        dying_stage: int = 0
        while not dying_stage == 11:
            self._sprite_id = (f"death-0{dying_stage}"
                               if dying_stage < 10 else f"death-{dying_stage}")
            self.sprite = SpriteBank.get_sprite("pacman", self._sprite_id)
            dying_stage += 1
        self.measure_spawn()

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

    def _set_destination(self) -> None:
        if self._direction not in KEY_DIRECTIONS:
            print(f"skipping '{self._direction}'")
            return
        col, row = KEY_DIRECTIONS[self._direction]
        self.cell_y += row
        self.cell_x += col
        centered: tuple[int, int] = self._cell_center(None)
        destx, desty = centered
        self._destination = (destx, desty)

    def update_direction(self, char: str) -> None:
        """Handle a key press (W, A, S or D)."""
        if self._in_linear(char) and not self._at_destination():
            # turning around between two cells is always possible:
            # we just walk back to the cell we came from
            self._start_walking(char)
            self._next_direction = ''
        else:
            # remember the wish, check() uses it as soon as we are
            # standing in the middle of a cell
            self._next_direction = char
