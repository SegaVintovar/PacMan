from .map import Map
from pydantic_extra_types.coordinate import Coordinate
from abc import ABC
from pygame import Surface


class Creature(ABC):
    def __init__(self, name: str, position: Coordinate) -> None:
        self.name = name
        self.postion = position
        self.cell: Cell = map[position[1]][position[0]]
        
        self.picture: Surface | None = None

    def move(self, map: Map) -> None:
        pass

    def _out_bound(self, map: Map) -> bool:
        pass

# tmp = Surface((5, 5))
# obj = draw.rect(tmp, (137, 137, 137), (4, 4))
# obj.move()
