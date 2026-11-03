from .creature import Creature
import pygame
from .constants import GHOSTS
from .map import Map

src = "src/assets/sprites/ghost_orange_left.png"


class Ghost(Creature):
    def __init__(self, name: str) -> None:
        self.image: pygame.Surface = self._upload_pic()
        self.rect: pygame.Rect = self._create_rect()
        self.name: str = "Clyde" | "Blinky" | "Pinky" | "Inky"

    def _upload_pic(self) -> pygame.Surface:
        return pygame.image.load(
            f"src/assets/sprites/ghost_{GHOSTS[self.name]}_left.png",
            ).convert_alpha()

    def _create_rect(self) -> pygame.Rect:
        match self.name:
            case "Blinky":
                return pygame.Rect((0, 0), (44, 44))
            case "Clyde":
                return pygame.Rect((1356, 0), (44, 44))
            case "Pinky":
                return pygame.Rect((0, 1156), (44, 44))
            case "Inky":
                return pygame.Rect((1356, 1156), (44, 44))

    def _pick_random_dest() -> None:
        ...

    def retreat_spawn_point() -> None:
        ...

    def move(self, map: Map) -> None:
        ...

    def _out_bound(self, map: Map) -> bool:
        pos = self.postion
    # ids are from 0 till 3(inclusive)