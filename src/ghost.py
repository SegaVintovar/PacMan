from .creature import Creature
import pygame
from .map import Map

src = "src/assets/sprites/ghost_orange_left.png"

class Ghost(Creature):
    def __init__(self, id: int) -> None:
        self.id = id
        self.image: pygame.Surface = self._upload_pic()
        self.rect: pygame.Rect = self._create_rect()

    def _upload_pic(self) -> pygame.Surface:
        return pygame.image.load(
            "src/assets/sprites/ghost_orange_left.png",
            ).convert_alpha()

    def _create_rect(self) -> pygame.Rect:
        return pygame.Rect((0, 0), (44, 44))

    def move(self, map: Map) -> None:
        ...

    def _out_bound(self, map: Map) -> bool:
        pos = self.postion
    # ids are from 0 till 3(inclusive)