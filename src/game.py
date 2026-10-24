from enum import Enum
from . import GameConfig
from . import MazeGenerator
from .creature import Creature
from .map import Map
import pygame


WINDOW_SIZE = (1400, 800)


class Menu(Enum):
    start_game = 0,
    view_highscores = 1,
    instructions = 2,
    settings = 3,
    exit = 4

class Score():
    ...


class Player():
    def __init__(self, lives: int) -> None:
        self.score: int = 0
        self.lives: int = lives
        self.gumsCollected: int = 0


class Timer():
    def __init__(self, level_max_time: int) -> None:
        self.level_max_time = level_max_time
        self.current_time: None = None

class Menu():
    def __init__(self):
        ...


# start the game
# - open the window, prepare a map/maps?, images
# - blit into the screen the menu
class Game:
    def __init__(self, config: GameConfig, maze_gen: MazeGenerator = MazeGenerator) -> None:
        # self.pacman = pacman
        self.config = config
        self.gumsCollected: int = 0  # should this attribute be in Player class???
        self.creatures: list[Creature] = []
        self.maps: list[Map] = []
        # self.maze_gen: Maze = maze_gen
        self.timer: Timer = Timer(config.level_max_time)
        self.player: Player = Player(config.lives)
        pygame.init()
        # screen in the window of the app itself, main screen
        screen = pygame.display.set_mode(WINDOW_SIZE)
        self.screen: pygame.Surface = screen  # 1. window first
        clock = pygame.time.Clock()
        self.clock: pygame.time.Clock = clock
        self._prepare_maps()

    def _prepare_maps(self) -> None:
        # for _ in range(len(self.config.level)):
        for _ in range(1):    
            one_more_map = Map(self.config)
            self.maps.append(one_more_map)

    def display_one_map(self) -> None:
        self.screen.blit(self.maps[0].map_image, (0, 0))

    def launch_game(self) -> None:
        # open main window - done in init
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


if __name__ == "__main__":
    game = Game()
    game.display_one_map()
    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # game.run(screen)
        # scaled_map = pygame.transform.scale(ourMap.map_image, WINDOW_SIZE)
        # screen.blit(scaled_map, dest=(0, 0))
        # ourHero.spawn(screen)
        pygame.display.update()
    pygame.quit()