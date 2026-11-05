from .map import Map
from pydantic_extra_types.coordinate import Coordinate
from abc import ABC
from .constants import TILE
import pygame


class Creature(ABC):
    def __init__(self, name: str, position: Coordinate) -> None:
        self.name = name
        self.postion = position
        self.cell_x: int = -1
        self.cell_y: int = -1
        self.sprite: pygame.Surface | None = None
        self._destination: tuple[int, int] | None = None

    def move(self, map: Map) -> None:
        pass

    def get_direction_destination(direction: str) -> tuple[int, int]:
        pass

    def _cell_center(self, coords: tuple[int, int] | None) -> tuple[int, int]:
        if coords is None:
            return (self.cell_x * TILE + TILE // 2,
                    self.cell_y * TILE + TILE // 2)
        x, y = coords
        return x * TILE + TILE // 2, y * TILE + TILE // 2

    def _out_bound(self, map: Map) -> bool:
        pass

    def _switchable(self, map: Map) -> bool:
        pass

    def spawn(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, self.rect)

# tmp = Surface((5, 5))
# obj = draw.rect(tmp, (137, 137, 137), (4, 4))
# obj.move()
