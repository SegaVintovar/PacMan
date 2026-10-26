from enum import Enum
from . import GameConfig
from . import MazeGenerator
from .creature import Creature
from .map import Map
from .pacman import Pacman
import pygame

TILE = 64
WINDOW_SIZE = (1400, 800)


class Main(Enum):
    start_game = 0,
    view_highscores = 1,
    instructions = 2,
    settings = 3,
    exit = 4


class ScoreBoard():
    ...


class Player():
    def __init__(self, lives: int) -> None:
        self.score: int = 0
        self.lives: int = lives
        self.gumsCollected: int = 0


class Timer():
    def __init__(self, level_max_time: int) -> None:
        self.level_max_time = level_max_time
        self.start_time = 0

    def start_timer(self) -> None:
        self.start_time = pygame.time.get_ticks()

    def time_since_start(self) -> int:
        return int((pygame.time.get_ticks() - self.start_time) / 1000)


class Menu():
    def __init__(self):
        ...


# has timer and current score and highest score
class Header():
    def __init__(self, config: GameConfig, highest_score: int = 0) -> None:
        self.score: int = 0
        self.config: GameConfig = config
        self.width = config.width
        self.highest_score: int = highest_score
        self.image: pygame.Surface = pygame.Surface((TILE * self.width, 100))
        self.font: pygame.font.Font = pygame.font.SysFont("Arial", 50)
        self.level: int = 0

    def current_score_n_lvl(self) -> None:
        self.image.blit(
            self.font.render(
                f"Score: {self.score}", True, (0, 0, 255)),
            dest=(10, 30)
        )
        self.image.blit(
            self.font.render(
                f"Highest Score: {self.highest_score}", True, (255, 0, 0)
            ),
            dest=(int((self.width / 2) * TILE - 200), 30)
        )
        self.image.blit(
            self.font.render(
                f"Level: {self.level}", True, (0, 255, 0)
            ),
            dest=(int((self.width) * TILE - 200), 30)
        )

    def show_me(self, screen: pygame.Surface) -> None:
        self.current_score_n_lvl()
        screen.blit(self.image, dest=(0, 0))

# has lives and fruits
class Footer():
    def __init__(self, config: GameConfig, lives: int) -> None:
        self.config: GameConfig = config
        self.width: int = config.width
        self.lives: int = lives
        self.image: pygame.Surface = pygame.Surface((TILE * self.width, 100))
        timer = Timer(config.level_max_time)
        self.timer: Timer = timer
        self.timer.start_timer()
        self.font: pygame.font.Font = pygame.font.SysFont("Arial", 50)

    def current_lives_n_timer(self) -> None:
        self.image.blit(
            self.font.render(f"Lives left: {self.lives}", True, (255, 0, 0)
                             ),
            dest=(10, 30)
        )
        self.image.blit(
            self.font.render(
                f"Time left: {
                    self.timer.level_max_time - self.timer.time_since_start()
                    }", True, (255, 0, 0)
                ),
            dest=(int(self.width / 2) * TILE - 50, 30)
        )

    def show_me(self, screen: pygame.Surface) -> None:
        self.image.fill("black")
        self.current_lives_n_timer()
        screen.blit(self.image, (0, (100 + self.config.height * TILE)))


# start the game
# - open the window, prepare a map/maps?, images
# - blit into the screen the menu
class Game():
    def __init__(self, config: GameConfig,
                 maze_gen: MazeGenerator = MazeGenerator) -> None:
        self.config = config
        # should this attribute be in Player class???
        self.gumsCollected: int = 0
        self.creatures: list[Creature] = []
        self.maps: list[Map] = []
        self.maze_gen: MazeGenerator = maze_gen
        self.timer: Timer = Timer(config.level_max_time)
        self.player: Player = Player(config.lives)
        pygame.init()
        # screen in the window of the app itself, main screen
        screen = pygame.display.set_mode(
            (config.width * TILE, config.height * TILE + 200))
        self.screen: pygame.Surface = screen  # 1. window first
        clock = pygame.time.Clock()
        self.clock: pygame.time.Clock = clock
        self._prepare_maps()
        self.pacman: Pacman = Pacman(self.maps[0], config)
        header = Header(self.config, 1000)
        self.header: Header = header
        footer = Footer(self.config, self.config.lives)
        self.footer: Footer = footer

    def process(self, events: list[pygame.event.Event]) -> bool:
        # static state: dict
        for event in events:
            if event.type == pygame.KEYDOWN:  # or event.type == pygame.KEYUP
                if event.key == pygame.K_w:
                    self.pacman.update_direction('W')
                elif event.key == pygame.K_a:
                    self.pacman.update_direction('A')
                elif event.key == pygame.K_s:
                    self.pacman.update_direction('S')
                elif event.key == pygame.K_d:
                    self.pacman.update_direction('D')
                elif event.key == pygame.K_q:
                    print("q")
                    return False
                # elif event.key == pygame.K_ESCAPE:
                #     state["menu"] = True
            if event.type == pygame.QUIT:
                print("Quit")
                return False
        # according to the state we are showing or game or menu or leadeboard
        scaled_map = pygame.transform.scale(self.maps[0].map_image,
                                            (self.config.width * TILE,
                                             self.config.height * TILE))
        self.screen.blit(scaled_map, dest=(0, 100))
        self.render_creatures()
        self.header.show_me(self.screen)
        self.footer.show_me(self.screen)
        return True

    def _prepare_maps(self) -> None:
        # for _ in range(len(self.config.level)):
        for _ in range(1):
            one_more_map = Map(self.config)
            self.maps.append(one_more_map)

    def display_one_map(self) -> None:
        # self.screen.fill("black")
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

    def render_creatures(self) -> None:
        self.pacman.spawn(self.screen)

    def navigate(option: Menu) -> int:
        return 1


if __name__ == "__main__":
    game = Game()
    game.display_one_map()
    running: bool = True
    print("doing it designated")
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
