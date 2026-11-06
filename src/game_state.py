# from .config import GameConfig
# from enum import Enum, auto
# from .module import Module
import pygame


class GameState():
    def __init__(self,
                 next_module: int,
                 running: bool,
                 extra: str) -> None:
        # for now extra is a string, but it maybe changed
        self.next_module = next_module
        self.running = running
        self.extra = extra

    def __repr__(self) -> tuple[int, bool, str]:
        return (self.next_module, self.running, self.extra)


# class GameState(Enum):
#     MENU = auto()
#     PLAY = auto()
#     SCOREBOARD = auto()
#     QUIT = auto()
