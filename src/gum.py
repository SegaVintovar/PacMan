import pygame
from pydantic_extra_types.coordinate import Coordinate
# from .cell import Cell
from .constants import TILE


class Gum():
    def __init__(self, position: Coordinate, t: str = "") -> None:
        self.position = position
        self.type: str = t if not t else "super"
        self.size: Coordinate = (5, 5) if not self.type else (10, 10)
        self.image: pygame.Surface = pygame.Surface(self.size)
        self.image.fill("white")
        self.hovered: bool = False
        self.rect = pygame.Rect(
            (
                self.position[0] + TILE // 2 - self.size[0] // 2,
                self.position[1] + TILE // 2 - self.size[1] // 2
            ),
            self.size,
        )
        self.x: int = self.rect.centerx
        self.y: int = self.rect.centery
