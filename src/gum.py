import pygame
# from pydantic_extra_types.coordinate import Coordinate
from .cell import Cell


class Gum():
    def __init__(self, cell: Cell) -> None:
        self.position = cell.position
        self.sprite = pygame.Rect(self.position[0], self.position[1], 5, 5)
