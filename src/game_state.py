# from .config import GameConfig
from enum import Enum, auto


class GameState(Enum):
    MENU = auto()
    PLAY = auto()
    SCOREBOARD = auto()
    QUIT = auto()
