from .config import GameConfig
from .pacman import Pacman
import pygame
from .constants import WINDOW_SIZE, HEADER_HEIGHT, FONT_SIZE, FONT_PATH, ASSETS_DIR, CYAN
from .level import Level
from .game_state import GameState
import random
from .module import Module
from .pathfinder import Pathfinder


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
    def _current_lives_n_timer(self, time: int, lives: int, invincible: bool) -> None:
        self.image.blit(
            self.font.render(f"Lives left: {lives}", True, (255, 0, 0)
                             ),
            dest=(10, 30)
        )
        if time < 0:
            return
        self.image.blit(
            self.font.render(
                f"Time left: {time}",
                True, (255, 0, 0)
                ),
            dest=(int(WINDOW_SIZE[0]) - 300, 30)
        )
        if invincible:
            self.image.blit(
                self.font.render(
                    "Invincible",
                    True, CYAN
                ),
                dest=((WINDOW_SIZE[0]//2 - FONT_SIZE * 5), 30)
            )

    def show_me(self,
                screen: pygame.Surface, time: int, pacman: Pacman) -> None:
        self.image.fill("black")
        self._current_lives_n_timer(time, pacman.lives, pacman.invincible)
        screen.blit(self.image, (0, (WINDOW_SIZE[1] + HEADER_HEIGHT)))


class Game(Module):
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.levels: list[Level] = []
        self.current_lvl_id: int = 0
        self._prepare_levels()
        self.current_lvl: Level = self.levels[self.current_lvl_id]
        self.pacman: Pacman = Pacman(self.current_lvl.map, config)
        header = Header(self.config)
        self.header: Header = header
        footer = Footer(self.config)
        self.footer: Footer = footer
        # needed???
        # self.done = False
        self.paused: bool = False
        self.wasted: bool = False
        original = pygame.image.load(
            ASSETS_DIR / "WASTED_hires.png")
        orig_w, orig_h = original.get_size()
        new_w = int(WINDOW_SIZE[0] * 0.85)
        new_h = int(orig_h * new_w / orig_w)
        self.wasted_surface: pygame.Surface = pygame.transform.smoothscale(
            original, (new_w, new_h))
        self.wasted_pos: tuple[int, int] = (
            (WINDOW_SIZE[0] - new_w) // 2,
            (WINDOW_SIZE[1] - new_h) // 2,
            )
        original = pygame.image.load(
            ASSETS_DIR / "mission_passed.png")
        orig_w, orig_h = original.get_size()
        new_w = int(WINDOW_SIZE[0] * 0.85)
        new_h = int(orig_h * new_w / orig_w)
        self.mission_passed: pygame.Surface = pygame.transform.smoothscale(
            original, (new_w, new_h))
        self.mis_pas_pos: tuple[int, int] = (
            (WINDOW_SIZE[0] - new_w) // 2,
            (WINDOW_SIZE[1] - new_h) // 2,
            )

    def process(self,
                events: list[pygame.event.Event],
                game_state: GameState,
                screen: pygame.Surface
                ) -> GameState:
        if game_state.previous == 2:
            self.current_lvl.timer.start_timer()

        if self.paused:
            self.current_lvl.timer.resume()
            for ghost in self.current_lvl.creatures:
                ghost.pussy_timer.resume()
            self.paused = False

        # check if the pacman is still alive

        for event in events:
            if event.type == pygame.KEYDOWN:  # or event.type == pygame.KEYUP
                # this can make our packy to crash
                ch: str = event.unicode
                if (ch in "wasd" and len(ch) == 1
                   or ch in "WASD" and len(ch) == 1):
                    self.pacman.update_direction(ch.upper())
                elif ch == "1":
                    self.pacman.lives += 1
                elif ch == "2":
                    self.pacman.invincible = not self.pacman.invincible
                    for ghost in self.current_lvl.creatures:
                        ghost.path = []
                elif ch == "3":
                    self.current_lvl_id += 1
                    if self.current_lvl_id >= len(self.levels):
                        game_state.gs_update(6, self.pacman.points, True)
                        return game_state
                    self.current_lvl = self.levels[self.current_lvl_id]
                    self.start_current_lvl()
                elif (event.key == pygame.K_SPACE or
                        event.key == pygame.K_q or
                        event.key == pygame.K_ESCAPE):
                    self.current_lvl.timer.pause()
                    for ghost in self.current_lvl.creatures:
                        ghost.pussy_timer.pause()
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
            screen.blit(self.mission_passed,
                        dest=self.mis_pas_pos)
            pygame.display.update()
            pygame.time.delay(2000)
            if self.current_lvl_id == len(self.config.level):
                # here we finally won
                game_state.gs_update(6, self.pacman.points, True)
                return game_state
            self.start_current_lvl()
            return game_state
        if self.current_lvl.timer.isBurned() or\
           not self.packie_still_alive():
            # wasted
            screen.blit(
                self.wasted_surface,
                dest=self.wasted_pos)
            pygame.display.update()
            pygame.time.delay(2000)
            game_state.gs_update(6, self.pacman.points, False)
            game_state.wasted = True
            return game_state
        self._display(map_image, screen)
        return game_state

    def _display(self,
                 map_image: pygame.Surface, screen: pygame.Surface) -> None:
        scaled_map = pygame.transform.scale(
            map_image, WINDOW_SIZE)
        self.header.show_me(screen, (self.current_lvl_id + 1),
                            self.pacman.points)
        time = (self.config.level_max_time -
                self.current_lvl.timer.time_since_start())
        self.footer.show_me(screen, time, self.pacman)
        screen.blit(scaled_map, dest=(0, HEADER_HEIGHT))

    def _prepare_levels(self) -> None:
        """"
        First lvl seed comes form the subject, rest random.
        """
        for i in range(len(self.config.level)):
            seed = self.config.seed if i == 0 else random.randrange(2**31)
            self.levels.append(Level(
                int(self.config.level[i]),
                self.config.level[i],
                seed,
                self.config
            ))
        print(f"Game: {len(self.config.level)} levels prepared")

    def start_current_lvl(self) -> None:
        print("lvl_id", self.current_lvl_id)
        print("amount of lvls", len(self.levels))
        self.current_lvl = self.levels[self.current_lvl_id]
        self.current_lvl.timer.start_time = pygame.time.get_ticks()
        self.pacman.map = self.current_lvl.map
        self.pacman.go_to_next_level(self.current_lvl.map)

    def packie_still_alive(self) -> bool:
        if self.pacman.lives > 0:
            return True
        return False
