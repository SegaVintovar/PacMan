import pygame
from pydantic_extra_types.coordinate import Coordinate


class Gum():
    def __init__(self, coords: Coordinate) -> None:
        self.position = coords
        self.sprite = pygame.Rect(self.position[0], self.position[1], 5, 5)
        self.super: bool = False
