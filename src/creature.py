from .map import Map
from pydantic_extra_types.coordinate import Coordinate
from abc import ABC
from pygame import Surface, draw
import pygame

class Creature(ABC):
    def __init__(self, name: str, position: Coordinate) -> None:
        self.name = name
        self.postion = position
        self.picture: Surface | None = None

    def move(self, map: Map) -> None:
        pass

# tmp = Surface((5, 5))
# obj = draw.rect(tmp, (137, 137, 137), (4, 4))
# obj.move()