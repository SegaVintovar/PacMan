from .creature import Creature
import pygame
from .constants import GHOSTS
from .map import Map

src = "src/assets/sprites/ghost_orange_left.png"


class Ghost(Creature):
    def __init__(self, name: str, start: tuple[int, int]) -> None:
        self.name: str = name
        self.start: tuple[int, int] = start
        self.rect: pygame.Rect = self._create_rect()
        self.sprite: pygame.Surface = self._upload_pic()
        self.pussy_mod: bool = False

    def _upload_pic(self) -> pygame.Surface:
        return pygame.image.load(
            f"src/assets/sprites/ghost_{GHOSTS[self.name][0]}_left.png",
            ).convert_alpha()

    def _create_rect(self) -> pygame.Rect:
        startx, starty = self.start
        return pygame.Rect((startx, starty), (44, 44))

    def _pick_random_dest() -> None:
        ...

    def retreat_spawn_point() -> None:
        ...

    def move(self, map: Map) -> None:
        ...

    def _out_bound(self, map: Map) -> bool:
        pos = self.postion
    # ids are from 0 till 3(inclusive)