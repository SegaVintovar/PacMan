# from .config import GameConfig
from enum import Enum, auto
# from .screen import Screen
import pygame

class GameState():
    next_screen: int
    main_screen: pygame.Surface
    extra: str

    def __repr__(self):
        return (self.next_screen, self.screen, self.extra)


# class GameState(Enum):
#     MENU = auto()
#     PLAY = auto()
#     SCOREBOARD = auto()
#     QUIT = auto()
