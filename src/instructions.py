from .config import GameConfig
import pygame
from .constants import WINDOW_SIZE, FONT_PATH, FONT_SIZE, CYAN
from typing import Any
# from .gradient import make_gradient
from .game_state import GameState
from .button import Button
from .module import Module


class Instructions(Module):
    rules = [
        " ----------- ",
        "Goal",
        "",
        "Eat every pacgum in the maze to clear the level.",
        "Clear all levels to win the game.",
        " ----------- ",
        "Controls:",
        "",
        "Move: Arrow keys or W / A / S / D",
        "Pause: ESC | Q | ",
        "Menus: Up / Down to navigate, Enter to select",
        "Name entry: type your name, Enter to confirm, Backspace to delete",
        " ----------- ",
        "Rules",
        "",
        "You move through corridors only. Walls block you.",
        "You start each level in the middle of the maze.",
        "If a ghost touches you, you lose a life and respawn in the middle.",
        "You lose the game when all lives are gone.",
        "Each level has a time limit of 90 seconds ⚙. 🔧 When time runs out,",
        "[the level restarts / the game ends].",
        "Your score and remaining lives carry over between levels.",
        " ----------- ",
        "Items and scoring",
        "",
        "Pacgum (small dot): +10 points ⚙",
        "Super-pacgum (big dot in each corner): +50 points ⚙ and the ghosts",
        "become edible for a short time",
        "Edible ghost: +200 points ⚙. An eaten ghost returns to its corner",
        "and respawns after a few seconds.",
        "Your score never decreases.",
        " ----------- ",
        "Ghosts",
        "",
        "4 ghosts start in the 4 corners of the maze.",
        "Normally they chase you.",
        "While edible, they run away from you.",
        " ----------- ",
        "Highscores",
        "After a win or a loss, enter your name (max 10 characters, letters,",
        "digits and spaces). The top 10 scores are shown in the main menu.",
        " ----------- ",
        "Cheat mode (for reviewers)",
        "🔧 Key bindings, for example: I = invincibility, N = skip level,",
        "F = freeze ghosts, L = extra life, and so on.",
    ]

    def __init__(self, bg: pygame.Surface, config: GameConfig) -> None:
        self.background = bg
        self.image: pygame.Surface = bg.copy()
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE - 5)
        self.config = config
        self.go_back: Button = Button(
            "Back to menu",
            ((WINDOW_SIZE[0] * 0.5), (WINDOW_SIZE[1] * 0.1)),
            ((WINDOW_SIZE[0] * 0.01), (WINDOW_SIZE[1] * 0.05)),
            2,
            CYAN)
        self.scroll_pos = 0
        self._prep_rules()

    def _prep_rules(self) -> None:
        start_pos = (WINDOW_SIZE[0] * 0.25, WINDOW_SIZE[1] * 0.05)
        step = (FONT_SIZE - 15) * 2
        self.image = pygame.Surface(
            WINDOW_SIZE, pygame.SRCALPHA).convert_alpha()
        for i, rule in enumerate(self.rules):
            position = (start_pos[0], start_pos[1] + i * step)
            self.image.blit(
                self.font.render(rule, True, "white"),
                dest=(position)
            )
        # self.image = self.background.copy()

    # need to change return type to GameState
    def process(self,
                events: list[pygame.event.Event],
                game_state: GameState,
                screen: pygame.Surface
                ) -> tuple[int, Any]:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or\
                      event.key == pygame.K_ESCAPE or\
                        event.key == pygame.K_RETURN:
                    game_state.gs_update(2)
                    return game_state
                if event.key == pygame.K_w or \
                        event.key == pygame.K_UP:
                    self.scroll_pos -= 10
                elif event.key == pygame.K_s or \
                        event.key == pygame.K_DOWN:
                    self.scroll_pos += 10
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if self.go_back.rect.collidepoint(x, y):
                    game_state.gs_update(2)
            if event.type == pygame.MOUSEWHEEL:
                self.scroll_pos += event.y * -10
                # if self.scroll_pos < 0:
                #     self.scroll_pos = 0
            if event.type == pygame.QUIT:
                game_state.quit()
                return game_state
        self._show_me(screen=screen)
        return game_state

    def _show_me(self, screen: pygame.Surface) -> None:
        # self._prep_rules()
        screen.blit(self.background, (0, 0))
        screen.blit(self.image, dest=(0, self.scroll_pos))
        screen.blit(self.go_back.image, (0, 0))
