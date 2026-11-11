from . import GameConfig
from .pacman import Pacman
import pygame
from .constants import WINDOW_SIZE, HEADER_HEIGHT, FONT_SIZE, FONT_PATH
from .level import Level
from .game_state import GameState
import random
from .module import Module

# from bastiaan
# from . import MazeGenerator
# from .creature import Creature
# from .ghost import Ghost
# from .map import Map
# from .pacman import Pacman
# import pygame
# from .constants import WINDOW_SIZE, HEADER_HEIGHT, FONT_SIZE, GHOSTS
# from typing import Any
# # from .game_state import GameState
# from .gum import Gum


class Header():
    def __init__(self, config: GameConfig) -> None:
        self.config: GameConfig = config
        self.width = config.width
        self.image: pygame.Surface = pygame.Surface(
            (WINDOW_SIZE[0], HEADER_HEIGHT))
        self.font: pygame.font.Font = pygame.font.Font(
            FONT_PATH, FONT_SIZE)

    def _current_score_n_lvl(self, current_level: int, score: int) -> None:
        self.image.fill("black")
        self.image.blit(
            self.font.render(
                f"Score: {score}", True, (0, 0, 255)),
            dest=(10, 30)
        )
        self.image.blit(
            self.font.render(
                "Packy by vsudak and brogaar", True, (255, 0, 0)
            ),
            dest=(int((WINDOW_SIZE[0] / 2) - FONT_SIZE * 7), 30)
        )
        self.image.blit(
            self.font.render(
                f"Level: {current_level}", True, (0, 255, 0)
            ),
            dest=(int((WINDOW_SIZE[0]) - FONT_SIZE * 6), 30)
        )

    def show_me(self,
                screen: pygame.Surface,
                current_lvl: int,
                score: int
                ) -> None:
        self._current_score_n_lvl(current_lvl, score)
        screen.blit(self.image, dest=(0, 0))


class Footer():
    def __init__(self, config: GameConfig) -> None:
        self.config: GameConfig = config
        self.width: int = config.width
        self.image: pygame.Surface = pygame.Surface(
            (WINDOW_SIZE[0], HEADER_HEIGHT))
        self.font: pygame.font.Font = pygame.font.Font(
            FONT_PATH, FONT_SIZE)

    # what if here we will take a time to display as an argument
    def _current_lives_n_timer(self, time: int, lives: int) -> None:
        self.image.blit(
            self.font.render(f"Lives left: {lives}", True, (255, 0, 0)
                             ),
            dest=(10, 30)
        )
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

    def show_me(self,
                screen: pygame.Surface, time: int, pacman: Pacman) -> None:
        self.image.fill("black")
        self._current_lives_n_timer(time, pacman.lives)
        screen.blit(self.image, (0, (WINDOW_SIZE[1] + HEADER_HEIGHT)))


class Game(Module):
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.levels: list[Level] = []
        self.current_lvl_id: int = 0
        self._prepare_levels()
        self.current_lvl: Level | None = None if not self.levels \
            else self.levels[self.current_lvl_id]
        self.pacman: Pacman = Pacman(self.current_lvl.map, config)
        header = Header(self.config)
        self.header: Header = header
        footer = Footer(self.config)
        self.footer: Footer = footer
        # needed???
        self.done = False
        self.paused = False
    # from bastiaan`s branch, just not to loose
        # self.gumsCollected: int = 0
        # self.creatures: list[Creature] = []
        # self.maps: list[Map] = []
        # self.maze_gen: MazeGenerator = maze_gen
        # # self.timer: Timer = Timer(config.level_max_time)
        # self.player: Player = Player(config.lives)
        # self._prepare_maps()
        # self.pacman: Pacman = Pacman(self.maps[0], config)
        # self.creatures.append(self.pacman)
        # self._awake_ghosts()
        # header = Header(self.config, 1000)
        # self.header: Header = header
        # footer = Footer(self.config, self.config.lives)
        # self.footer: Footer = footer
        # self.done = False
        # self.running = False
        # self.paused = False
        # self.gums: list[Gum] = []
        # self._gen_gums()
        # # if we are done with a lvl - then we poping it away
        # self.levels: list[Level] = []
        # self.points: int = 0

    # should return 0 , 1 , 2
    # or GameState that will store
    # track the win_loose condition, we can return gs with extra
    def process(self,
                events: list[pygame.event.Event],
                game_state: GameState,
                screen: pygame.Surface
                ) -> GameState:
        if game_state.previous == 2:
            self.current_lvl.timer.start_timer()
        # nothing yet sets this to True
        if self.done:
            # open the page to enter the name of the player
            # so it will add this score to the file
            game_state.gs_update(6, self.pacman.points)
            return game_state
        if self.paused:
            self.current_lvl.timer.resume()
            self.paused = False

        # check if the level is done and if we should switch the next one
        # level switch works
        # check if there is a time
        # check if the pacman is still alive

        for event in events:
            if event.type == pygame.KEYDOWN:  # or event.type == pygame.KEYUP
                # this can make our packy to crash
                ch: str = event.unicode
                if ch in "wasd" and len(ch) == 1:
                    self.pacman.update_direction(ch.upper())
                elif (event.key == pygame.K_SPACE or
                        event.key == pygame.K_q or
                        event.key == pygame.K_ESCAPE):
                    self.current_lvl.timer.pause()
                    self.paused = True
                    game_state.gs_update(5, self.pacman.points)
                    return game_state
            if event.type == pygame.QUIT:
                game_state.quit()
                return game_state
        map_image = self.current_lvl.map.map_image.copy()
        # if we finished current level
        if self.current_lvl.process(map_image, self.pacman) is True:
            self.current_lvl_id += 1
            if self.current_lvl_id == len(self.config.level):
                # here we finally won
                game_state.gs_update(6, self.pacman.points, True)
                return game_state
            self.start_current_lvl()
            return game_state
        if self.current_lvl.timer.isBurned():
            game_state.gs_update(6, self.pacman.points, False)
            return game_state
        self._display(map_image, screen)
        return game_state

    # def lvl_process(self)

    def _display(self,
                 map_image: pygame.Surface, screen: pygame.Surface) -> None:
        scaled_map = pygame.transform.scale(
            map_image, WINDOW_SIZE)
        self.header.show_me(screen, (self.current_lvl_id + 1),
                            self.pacman.points)
        time = (self.config.level_max_time -
                self.current_lvl.timer.time_since_start())
        # print("time since start", self.current_lvl.timer.time_since_start(), "\n",
        #       "start time", self.current_lvl.timer.start_time)
        self.footer.show_me(screen, time, self.pacman)
        screen.blit(scaled_map, dest=(0, HEADER_HEIGHT))

    def _prepare_levels(self) -> list[Level]:
        """"
        First lvl seed comes form the subject, rest random.
        """
        for i in range(len(self.config.level)):
            seed = self.config.seed if i == 0 else random.randrange(2**31)
            self.levels.append(Level(
                int(self.config.level[i]),
                self.config.level[i],
                seed,
                config=self.config
            ))
        print(f"Game: {len(self.config.level)} levels prepared")

    def start_current_lvl(self):
        print("lvl_id", self.current_lvl_id)
        print("amount of lvls", len(self.levels))
        self.current_lvl = self.levels[self.current_lvl_id]
        self.current_lvl.timer.start_time = pygame.time.get_ticks()
        self.pacman.go_to_next_level(self.current_lvl.map)

    def _init_creatures() -> None:
        """init PacMan, Ghosts"""
        ...

    # def render_creatures(self, map: pygame.Surface) -> None:
    #     for creature in self.creatures:
    #         creature.check((self.pacman.cell_x, self.pacman.cell_y))
    #         creature.spawn(map)
    #     self.pacman.check()
    #     self.pacman.spawn(map)

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
