from .gum import Gum
from .map import Map
import pygame


# we need some class for state returns
class Level():
    def __init__(self,
                 id: int,
                 name: str,
                 seed: int,
                 map_size: tuple[int, int]
                 ) -> None:
        self.id = id
        self.name = name
        self.seed = seed
        self.map: Map = Map()
        self.gums: list[Gum]
        

    def process(self, events: list[pygame.event.Event]) -> None:
        ...
