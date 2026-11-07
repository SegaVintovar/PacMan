from enum import Enum
from . import GameConfig
from . import MazeGenerator
from .pacman import Pacman
import pygame
from .constants import WINDOW_SIZE, HEADER_HEIGHT, FONT_SIZE
from .gum import Gum
from .level import Level
from .timer import Timer
from .game_state import GameState


class Main(Enum):
    start_game = 0,
    view_highscores = 1,
    instructions = 2,
    settings = 3,
    exit = 4


class Player():
    def __init__(self, lives: int) -> None:
        self.score: int = 0
        self.lives: int = lives
        self.gumsCollected: int = 0


# has timer and current score and highest score
class Header():
    def __init__(self, config: GameConfig, highest_score: int = 0) -> None:
        self.score: int = 0
        self.config: GameConfig = config
        self.width = config.width
        self.highest_score: int = highest_score
        self.image: pygame.Surface = pygame.Surface(
            (WINDOW_SIZE[0], HEADER_HEIGHT))
        self.font: pygame.font.Font = pygame.font.SysFont("Arial", FONT_SIZE)
        self.level: int = 0

    def update_score(self, add: int) -> None:
        ...

    def _current_score_n_lvl(self) -> None:
        self.image.blit(
            self.font.render(
                f"Score: {self.score}", True, (0, 0, 255)),
            dest=(10, 30)
        )
        self.image.blit(
            self.font.render(
                f"Highest Score: {self.highest_score}", True, (255, 0, 0)
            ),
            dest=(int((WINDOW_SIZE[0] / 2) - FONT_SIZE * 4), 30)
        )
        self.image.blit(
            self.font.render(
                f"Level: {self.level}", True, (0, 255, 0)
            ),
            dest=(int((WINDOW_SIZE[0]) - FONT_SIZE * 4), 30)
        )

    def show_me(self, screen: pygame.Surface) -> None:
        self._current_score_n_lvl()
        screen.blit(self.image, dest=(0, 0))


# has lives and fruits
class Footer():
    def __init__(self, config: GameConfig, lives: int) -> None:
        self.config: GameConfig = config
        self.width: int = config.width
        self.lives: int = lives
        self.image: pygame.Surface = pygame.Surface(
            (WINDOW_SIZE[0], HEADER_HEIGHT))
        timer = Timer(config.level_max_time)
        self.timer: Timer = timer
        self.timer.start_timer()
        self.font: pygame.font.Font = pygame.font.SysFont("Arial", FONT_SIZE)

    # what if here we will take a time to display as an argument
    def _current_lives_n_timer(self, time: int) -> None:
        self.image.blit(
            self.font.render(f"Lives left: {self.lives}", True, (255, 0, 0)
                             ),
            dest=(10, 30)
        )
        time = self.timer.level_max_time - self.timer.time_since_start()
        if time < 0:
            return
        self.image.blit(
            self.font.render(
                f"Time left: {
                    time
                    }", True, (255, 0, 0)
                ),
            dest=(int(WINDOW_SIZE[0]) - 300, 30)
        )

    def show_me(self, screen: pygame.Surface) -> None:
        self.image.fill("black")
        self._current_lives_n_timer(time)
        screen.blit(self.image, (0, (WINDOW_SIZE[1] + HEADER_HEIGHT)))


# start the game
# - open the window, prepare a map/maps?, images
# - load levels
# - blit into the screen the menu/map/scoreboard
class Game():
    # lets think about it if we are running the game for the first time
    # or we continue playing after pause
    # timer per level
    def __init__(self, config: GameConfig,
                 maze_gen: MazeGenerator = MazeGenerator) -> None:
        self.config = config
        # should this attribute be in Player class???
        self.gumsCollected: int = 0
        self.lives: int = config.lives
        self.levels: list[Level] = []
        self._prepare_levels()
        # try ???
        self.current_lvl: Level = self.levels[0]
        # prepare levels
        # self._prepare_creatures()
        # self.pacman: Pacman = Pacman(self.map, config)
        header = Header(self.config, 1000)
        self.header: Header = header
        footer = Footer(self.config, self.config.lives)
        self.footer: Footer = footer
        self.done = False
        self.running = False
        self.paused = False
        self.gums: list[Gum] = []
        # self._gen_gums()
        # if we are done with a lvl - then we poping it away
        self.points: int = 0

    # def _gen_gums(self) -> None:
    #     # amount = self.config.pacgum
    #     corner_cells = (
    #         self.maps[0].map[0][0],
    #         self.maps[0].map[0][self.config.height - 1],
    #         self.maps[0].map[self.config.width - 1][0],
    #         self.maps[0].map[self.config.width - 1][self.config.height - 1]
    #     )
    #     for row in self.maps[0].map:
    #         for c in row:
    #             if c.value not in (15, 1):
    #                 px, py = c.position
    #                 self.gums.append(
    #                         Gum(
    #                             (px, py),
    #                             t="super" if c in corner_cells else ""
    #                         )
    #                 )

    # def show_gums(self, screen: pygame.Surface) -> None:
    #     for g in self.gums:
    #         if self.pacman.rect.center == g.rect.center:
    #             self.header.score += (self.config.points_per_pacgum
    #                                   if not g.type else
    #                                   self.config.points_per_super_pacgum)
    #             self.gums.remove(g)
    #         else:
    #             screen.blit(g.image, dest=g.rect)

    # should return 0 , 1 , 2
    # or GameState that will store
    def process(self,
                events: list[pygame.event.Event],
                game_state: GameState,
                screen: pygame.Surface
                ) -> GameState:
        # static state: dict
        if self.done:
            # open the page to enter the name of the player
            # so it will add this score to the file
            return (2, (self.player.name, self.player.score))  # game is done WIN/LOOSE, so we need to store the result
        if not self.running:
            self.running = True
        # shall lvl process return smth
        self.current_lvl.process(events=events, game_state=game_state)
        for event in events:
            if event.type == pygame.KEYDOWN:  # or event.type == pygame.KEYUP
                ch: str = event.unicode
                if ch in "wasd":
                    self.pacman.update_direction(ch.upper())
                elif (event.key == pygame.K_SPACE or
                        event.key == pygame.K_q or
                        event.key == pygame.K_ESCAPE):
                    # timer needs to be paused here
                    self.footer.timer.pause()
                    self.paused = True
                    game_state.next_module = 2
                    return game_state
            if event.type == pygame.QUIT:
                game_state.next_module = 0
                game_state.running = False
                return game_state
        map_image = self.maps[0].map_image.copy()
        self.render_creatures(map_image)
        self.show_gums(map_image)
        # render gums, ghosts
        scaled_map = pygame.transform.scale(
            map_image, WINDOW_SIZE)
        self.header.show_me(screen)
        self.footer.show_me(screen)
        # if not self.footer.show_me(screen):
        #     return (2, self.)
        screen.blit(scaled_map, dest=(0, HEADER_HEIGHT))
        return game_state

    def _prepare_levels(self) -> list[Level]:
        for i in range(len(self.config.level)):
            self.levels.append(Level(
                int(self.config.level[i]),
                self.config.level[i],
                self.config.seed + i,
                config=self.config
            ))
        print(f"Game: {len(self.config.level)} levels prepared")

    # def _awake_ghosts(self) -> None:
    #     for name in GHOSTS:
    #         d: dict[str, Any] = GHOSTS[name]

    def place_gums(self) -> None:
        # self.screen.blits()
        ...

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

    # def render_creatures(self, map: pygame.Surface) -> None:
    #     for creature in self.creatures:
    #         creature.spawn(map)
    #     self.pacman.check()
    #     self.pacman.spawn(map)

    # def navigate(option: Menu) -> int:
    #     return 1

