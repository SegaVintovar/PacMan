
from enum import Enum
from . import Pacman, GameConfig
from . import Maze
from .creature import Creature
from .map import Map
from pygame import Surface


class Menu(Enum):
    start_game = 0,
    view_highscores = 1,
    instructions = 2,
    settings = 3,
    exit = 4


class Game:
    def __init__(self, config: GameConfig, maze_gen: Maze) -> None:
        # self.pacman = pacman
        self.config = config
        self.gumsCollected: int = 0
        self.creatures: list[Creature] = []
        self.maps: list[Map] = []
        self.maze_gen: Maze = maze_gen

    def launch_game(self) -> None:
        # upload all images
        # render all maps
        # open the menu
        ...

    def start_lvl(self, level: int):
        ...

    def _init_creatures() -> None:
        """init PacMan, Ghosts"""
        ...

    
    def menu() -> None:
        """
        after launching a window frame,
        this must be representing as a landing page
        """
        ...

    def render_game() -> None:
        ...

    def navigate(option: Menu) -> int:
        return 1
