from enum import Enum
from . import GameConfig
from . import MazeGenerator
from .creature import Creature
from .ghost import Ghost
from .map import Map
from .pacman import Pacman
import pygame
from .constants import WINDOW_SIZE, HEADER_HEIGHT, FONT_SIZE, GHOSTS
from typing import Any
# from .game_state import GameState
from .gum import Gum


class Main(Enum):
    start_game = 0,
    view_highscores = 1,
    instructions = 2,
    settings = 3,
    exit = 4


# we need some class for state returns
class Level():
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.map: Map
        self.gums: list[Gum]


class Player():
    def __init__(self, lives: int) -> None:
        self.score: int = 0
        self.lives: int = lives
        self.gumsCollected: int = 0


class Timer():
    def __init__(self, level_max_time: int) -> None:
        self.level_max_time = level_max_time
        self.start_time: int = 0
        # when we started a pause
        self.paused_time: int = 0

    def start_timer(self) -> None:
        self.start_time = pygame.time.get_ticks()

    def time_since_start(self) -> int:
        return int((pygame.time.get_ticks() - self.start_time) / 1000)

    def pause(self) -> None:
        self.paused_time = pygame.time.get_ticks()

    def resume(self) -> None:
        now = pygame.time.get_ticks()
        self.start_time += now - self.paused_time
        # self.start_time += self.paused_time


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
            dest=(int((WINDOW_SIZE[0] / 2) - FONT_SIZE * 4), 30)
        )
        self.image.blit(
            self.font.render(
                f"Level: {self.level}", True, (0, 255, 0)
            ),
            dest=(int((WINDOW_SIZE[0]) - FONT_SIZE * 4), 30)
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
        self.image: pygame.Surface = pygame.Surface(
            (WINDOW_SIZE[0], HEADER_HEIGHT))
        timer = Timer(config.level_max_time)
        self.timer: Timer = timer
        self.timer.start_timer()
        self.font: pygame.font.Font = pygame.font.SysFont("Arial", FONT_SIZE)

    def _current_lives_n_timer(self) -> None:
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
        self._current_lives_n_timer()
        screen.blit(self.image, (0, (WINDOW_SIZE[1] + HEADER_HEIGHT)))


# start the game
# - open the window, prepare a map/maps?, images
# - blit into the screen the menu/map/scoreboard
class Game():
    # lets think about it if we are running the game for the first time
    # or we continue playing after pause
    def __init__(self, config: GameConfig,
                 maze_gen: MazeGenerator = MazeGenerator) -> None:
        self.config = config
        # should this attribute be in Player class???
        self.gumsCollected: int = 0
        self.creatures: list[Creature] = []
        self.maps: list[Map] = []
        self.maze_gen: MazeGenerator = maze_gen
        # self.timer: Timer = Timer(config.level_max_time)
        self.player: Player = Player(config.lives)
        self._prepare_maps()
        self.pacman: Pacman = Pacman(self.maps[0], config)
        self.creatures.append(self.pacman)
        self._awake_ghosts()
        header = Header(self.config, 1000)
        self.header: Header = header
        footer = Footer(self.config, self.config.lives)
        self.footer: Footer = footer
        self.done = False
        self.running = False
        self.paused = False
        self.gums: list[Gum] = []
        self._gen_gums()
        # if we are done with a lvl - then we poping it away
        self.levels: list[Level] = []
        self.points: int = 0

    def _gen_gums(self) -> None:
        # amount = self.config.pacgum
        corner_cells = (
            self.maps[0].grid[0][0],
            self.maps[0].grid[0][self.config.height - 1],
            self.maps[0].grid[self.config.width - 1][0],
            self.maps[0].grid[self.config.width - 1][self.config.height - 1]
        )
        for row in self.maps[0].grid:
            for c in row:
                if c.value not in (15, 1):
                    px, py = c.position
                    self.gums.append(
                            Gum(
                                (px, py),
                                t="super" if c in corner_cells else ""
                            )
                    )

    def show_gums(self, screen: pygame.Surface) -> None:
        for g in self.gums:
            if self.pacman.rect.center == g.rect.center:
                self.header.update_score(self.config.points_per_pacgum
                                         if not g.type else
                                         self.config.points_per_super_pacgum)
                if g.type == "super":
                    print("all the ghosts should be pussies")
                self.gums.remove(g)
            else:
                screen.blit(g.image, dest=g.rect)

    # should return 0 , 1 , 2
    # or GameState that will store
    def process(self,
                events: list[pygame.event.Event],
                screen: pygame.Surface
                ) -> tuple[int, Any]:
        # static state: dict
        if self.done:
            # open the page to enter the name of the player
            # so it will add this score to the file
            # game is done WIN/LOOSE, so we need to store the result
            return (2, (self.player.name, self.player.score))
        if not self.running:
            self.running = True
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
                    return (2, None)
            if event.type == pygame.QUIT:
                return (0, None)
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
        return (1, None)

    def _prepare_maps(self) -> None:
        for _ in range(1):
            one_more_map = Map(self.config)
            self.maps.append(one_more_map)

    def _prepare_lvl(self) -> None:
        for i in range((self.config.level)):
            one_more_map = Level(i, self.config.level[i])
            self.maps.append(one_more_map)

    def _awake_ghosts(self) -> None:
        for name in GHOSTS:
            ghost: Creature = Ghost(
                name=name,
                map=self.maps[0],
                config=self.config
            )
            self.creatures.append(ghost)

    def place_gums(self) -> None:
        # self.screen.blits()
        ...

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

    def render_creatures(self, map: pygame.Surface) -> None:
        for creature in self.creatures:
            creature.check((self.pacman.cell_x, self.pacman.cell_y))
            creature.spawn(map)
        self.pacman.check()
        self.pacman.spawn(map)

    # def navigate(option: Menu) -> int:
    #     return 1


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
