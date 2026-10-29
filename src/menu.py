from . import Game
from .constants import FONT_SIZE, WINDOW_SIZE
import pygame
from typing import Any
from typing import Callable

class Menu():
    class Button():
        def __init__(self, text: str, size: tuple[int, int], position: tuple[int, int], action: Callable) -> None:
            self.text = text
            self.image: pygame.Surface = pygame.Surface(size)
            self.rect: pygame.Rect = pygame.rect.Rect(position, size)
            self.action = action
            self.highlighted: bool = True
            self.font: pygame.font.Font = pygame.font.SysFont("Arial", FONT_SIZE)

            self.image.blit(
                self.font.render(self.text, True, (0, 255, 0)),
                dest=(FONT_SIZE, FONT_SIZE)
                )

        def execute(self, *arg: Any) -> None:
            self.action(arg)


    def __init__(self, game: Game):
        self.image: pygame.Surface = pygame.Surface(WINDOW_SIZE)
        self.buttons: list[Menu.Button] = []
        self.game = game
        self._create_buttons()
        self._render_menu()

    def _create_buttons(self) -> None:
        size: tuple[int, int] = (int(WINDOW_SIZE[0] * 0.4), int(WINDOW_SIZE[1] * 0.1))
        start_position = size
        step = int(WINDOW_SIZE[1] * 0.2)
        start = ("Start", self.game.state)
        quit = ("Exit", exit)
        buttons = [start, quit]
        for i, b in enumerate(buttons):
            position = (start_position[0], (start_position[1] + i * step))
            self.buttons.append(Menu.Button(b[0], size, position, b[1]))

    def _render_menu(self) -> None:
        for btn in self.buttons:
            self.image.blit(btn.image, btn.rect)

    def open_menu(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (0, 0))
