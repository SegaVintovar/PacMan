
import pygame
from typing import Any
from .cell import Cell
from .map import Map

_key_directions: dict[str, tuple[int, int]] = {
    'W': (-1, 0),
    'D': (0, 1),
    'S': (1, 0),
    'A': (0, -1)
}


class Pacman:
    def __init__(self, map: Map, config: dict[str, Any]) -> None:
        self.x: int = int(config["width"]) / 2
        self.y: int = int(config["height"]) / 2
        self.map = map
        self.lives: int = int(config["lives"])
        self.points: int = 0
        self.direction: str = 'A'
        self.sprite = pygame.image.load(
            f"src/assets/sprites/pacman_{self.direction}_wide.png",
            ).convert_alpha()
        self.coords = self.measure_spawn(self.map)

    def spawn(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, self.coords)

    """Creating an escapable point for pac-man.
       in case of an odd amount it is a right spawn
       within the center unless the cell represents
       as a 42-grid."""
    def measure_spawn(self, _map: Map) -> tuple[int, int]:
        row_mid: int = int(len(_map.map) / 2)
        col_mid: int = int(len(_map.map[0]) / 2)
        cell: Cell = _map.map[row_mid][col_mid]
        while cell.n and cell.e and cell.s and cell.w:
            col_mid -= 1
            cell = _map.map[row_mid][col_mid]
        return cell.position

    def _move(self) -> None:
        ...

    def _moveable(self) -> bool:
        updating: tuple[int, int]
        match self.direction:
            case 'W':
                updating = (-1, 0)
            case 'D':
                updating = (0, 1)
            case 'S':
                updating = (1, 0)
            case 'A':
                updating = (0, -1)
        newy, newx = updating
        posy, posx = self.coords
        if (posy+newy) < 0 or (posy+newy) >= self.map.height:
            return False
        if (posx+newx) < 0 or (posx+newx) >= self.map.width:
            return False
        self.coords = (posy+newy, posx+newx)
        return True

    def _bounce(self) -> bool:
        row, col = self.coords
        cell: Cell = self.map.map[row][col]
        return (
            cell.n and self.direction == 'W'
            or cell.e and self.direction == "D"
            or cell.s and self.direction == "S"
            or cell.w and self.direction == "A"
            )

    def update_direction(self, char: str) -> None:
        self.direction = char
        self.sprite = pygame.image.load(
            f"src/assets/sprites/pacman_{self.direction}_wide.png"
            ).convert_alpha()
        print(f"This is a potential bounce? {self._bounce()}")
