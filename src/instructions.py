from .config import GameConfig
import pygame
from .constants import WINDOW_SIZE, HEADER_HEIGHT, FONT_PATH, FONT_SIZE
from typing import Any
from .gradient import make_gradient


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

    def __init__(self, config: GameConfig) -> None:
        self.background: pygame.Surface = make_gradient(
            (WINDOW_SIZE[0], WINDOW_SIZE[1] + HEADER_HEIGHT * 2))
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE - 25)
        # self.text = self.font.render(self.rules, True, "white")
        # self.image_with_txt = pygame.Surface(
        #     self.font.size(self.rules), masks=pygame.SRCALPHA)
        # self.image_with_txt.blit(self.text, dest=(0, 0))
        # self.background.blit(
        #     self.image_with_txt,
        #     dest=(WINDOW_SIZE[0] * 0.3, WINDOW_SIZE[1] * 0.2)
        #     )
        self.config = config
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

    def process(self,
                events: list[pygame.event.Event], screen: pygame.Surface
                ) -> tuple[int, Any]:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return (2, None)
            if event.type == pygame.QUIT:
                return (0, None)
        self._show_me(screen=screen)
        return (4, None)

    def _show_me(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, dest=(0, 0))