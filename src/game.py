
from enum import Enum
from . import Pacman, GameConfig
from . import Maze
from .creature import Creature


class Menu(Enum):
    start_game = 0,
    view_highscores = 1,
    instructions = 2,
    settings = 3,
    exit = 4


class Game:
    def __init__(self, pacman: Pacman, config: GameConfig) -> None:
        self.pacman = pacman
        self.config = config
        self.gumsCollected: int = 0
        self.creatures: list[Creature] = []

        self.map: Maze = Maze(size=(int(config["width"]),int(config["height"])))

    def launch_game() -> None:
        ...

    """"after launching a window frame,
    this must be representing as a landing page"""
    def menu() -> None:
        ...

    def render_game() -> None:
        ...

    def navigate(option: Menu) -> int:
        return 1
