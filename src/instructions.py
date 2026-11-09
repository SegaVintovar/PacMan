from .config import GameConfig
import pygame
from .constants import WINDOW_SIZE, FONT_PATH, FONT_SIZE
from typing import Any
from .gradient import make_gradient
from .game_state import GameState
from .button import Button


class Instructions():
    rules = ["The game consists of multiple levels (at least 10).",
             "• Each level has a time limit (e.g., 90 seconds).\n",
             "• If the time limit is reached, you can decide what happens ",
             "(e.g., restart the level, end the game, etc.).\n",
             "• If the player completes a level, they move to the next level.",
             "• The player keeps their score and",
             "remaining lives between levels.\n",
             "• The game ends when all levels are completed or ",
             "when the player loses all lives.\n",
             "• During the game, the player can pause and resume the game.\n",
             "• When the game ends (win or lose),",
             "the final score is displayed, and the player can ",
             "enter their name to save the highscore.\n",
             "• After the game ends, the player is returned to the main menu."
             ]

    def __init__(self, bg: pygame.Surface, config: GameConfig) -> None:
        self.background = bg
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE - 25)
        self.config = config
        self.go_back: Button = Button(
            "Back to menu",
            ((WINDOW_SIZE[0] * 0.5), (WINDOW_SIZE[1] * 0.1)),
            ((WINDOW_SIZE[0] * 0.2), (WINDOW_SIZE[1] * 0.9)),
            2)
        self._prep_rules()

    def _prep_rules(self) -> None:
        start_pos = (WINDOW_SIZE[0] * 0.2, WINDOW_SIZE[1] * 0.2)
        step = (FONT_SIZE - 15) * 2 
        for i, rule in enumerate(self.rules):
            position = (start_pos[0], start_pos[1] + i * step)
            self.background.blit(
                self.font.render(rule, True, "white"),
                dest=(position)
            )
        self.background.blit(self.go_back.image, self.go_back.rect)

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
                    game_state.next_module = 2
                    # return (2, None)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if self.go_back.rect.collidepoint(x, y):
                    game_state.next_module = 2
                    # return (2, None)
            if event.type == pygame.QUIT:
                game_state.running = False
                game_state.next_module = 0
                return game_state
        self._show_me(screen=screen)
        # return (4, None)
        return game_state

    def _show_me(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, dest=(0, 0))