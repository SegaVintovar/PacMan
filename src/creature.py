# from .map import Map
from pydantic_extra_types.coordinate import Coordinate
from abc import ABC, abstractmethod
from .constants import TILE
import pygame
from typing import Optional


class Creature(ABC):
    def __init__(self, name: str, position: Coordinate) -> None:
        self.name = name
        self.position = position
        self.cell_x: int = -1
        self.cell_y: int = -1
        self.sprite: pygame.Surface
        self.start: tuple[int, int]
        self.rect: pygame.Rect
        self._destination: tuple[int, int] | None = None
        self._direction: str | None = None

    @abstractmethod
    def check(self, pacman: pygame.Rect | None) -> bool:
        pass

    @abstractmethod
    def measure_spawn(self) -> None:
        pass

    # @abstractmethod
    # def get_direction_destination(self, direction: str) -> tuple[int, int]:
    #     pass

    def _cell_center(self, coords: tuple[int, int] | None) -> tuple[int, int]:
        if coords is None:
            return (self.cell_x * TILE + TILE // 2,
                    self.cell_y * TILE + TILE // 2)
        x, y = coords
        return x * TILE + TILE // 2, y * TILE + TILE // 2

    @abstractmethod
    def _bounce(self, char: Optional[str]) -> bool:
        pass

    # @abstractmethod
    # def _switchable(self, map: Map) -> bool:
    #     pass

    def spawn(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, self.rect)

    @abstractmethod
    def _set_destination(self) -> None:
        pass

    # src/creature.py:45: error: "Creature" has no attribute "rect"
    # [attr-defined]
    def _at_destination(self) -> bool:
        answer: bool = self.rect.center == self._destination
        return answer
