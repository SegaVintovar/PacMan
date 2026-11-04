# from .config import GameConfig
# from enum import Enum, auto
from .module import Module
import pygame


class GameState():
    def __init__(self,
                 next_module: Module,
                 main_window: pygame.Surface,
                 extra: str) -> None:
        self.next_module = next_module
        self.main_window = main_window  # not sure
        self.extra = extra

    def __repr__(self):
        return (self.next_screen, self.screen, self.extra)


# class GameState(Enum):
#     MENU = auto()
#     PLAY = auto()
#     SCOREBOARD = auto()
#     QUIT = auto()
