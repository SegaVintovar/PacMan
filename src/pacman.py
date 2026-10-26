
from enum import Enum
import pygame
from typing import Any
from .cell import Cell
from .map import Map
from .config import GameConfig

TILE = 64

class Controls(Enum):
    W = 0,
    D = 1,
    S = 2,
    A = 3


class Pacman:
    def __init__(self, map: Map, config: GameConfig) -> None:
        self.x: int = (int(config.width)) / 2
        self.y: int = (int(config.height)) / 2
        self.map = map
        self.lives: int = int(config.lives)
        self.points: int = 0
        self.lastDirection: Controls = 3
        self.coords = self.measure_spawn(self.map)
        self.sprite = pygame.image.load(
            "src/assets/sprites/pacman_A_wide.png").convert_alpha()
        self.image: pygame.Surface = pygame.Surface(
            (TILE, TILE)).blit(self.sprite, dest=(0, 0))
        # self.coords = self.measure_spawn(self.map)
        self.rect: pygame.Rect = pygame.Rect(
            self.coords[0], self.coords[1], 64, 64)

    def spawn(self, screen: pygame.Surface) -> None:
        scaled = pygame.transform.scale(self.sprite, (64, 64))
        screen.blit(scaled, self.rect)

    """Creating an escapable point for pac-man.
       in case of an odd amount it is a right spawn
       within the center unless the cell represents 
       as a 42-grid."""
    def measure_spawn(self, _map: Map) -> tuple[int, int]:
        row_mid: int = int((len(_map.map)) / 2)
        col_mid: int = int((len(_map.map[0])) / 2)
        cell: Cell = _map.map[row_mid][col_mid]
        return (cell.position[0], cell.position[1])

    def move(keyEvent: pygame.event.Event) -> None:
        ...

    def process(event: pygame.event.Event) -> None:
        ...



for event in pygame.event.get():
    if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        if event.mod == pygame.KMOD_NONE:
