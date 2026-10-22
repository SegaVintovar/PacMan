
from enum import Enum
import pygame
from typing import Any
from .cell import Cell
from .map import Map


class Controls(Enum):
    W = 0,
    D = 1,
    S = 2,
    A = 3


class Pacman:
    def __init__(self, map: Map, config: dict[str, Any]) -> None:
        self.x: int = int(config["width"]) / 2
        self.y: int = int(config["height"]) / 2
        self.map = map
        self.lives: int = int(config["lives"])
        self.points: int = 0
        self.lastDirection: Controls = 3
        self.sprite = pygame.image.load("src/assets/sprites/pacman_A_wide.png").convert_alpha()
        self.coords = self.measure_spawn(self.map)
        self.rect: pygame.Rect = pygame.Rect(self.x, self.y, 44, 44)


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
        return cell.position

    def move(keyEvent: Any) -> None:
        ...
