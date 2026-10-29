from . import Game
from .constants import FONT_SIZE, WINDOW_SIZE
import pygame
from typing import Any
from typing import Callable

class Menu():
    class Button():
        def __init__(self, text: str, size: tuple[int, int], position: tuple[int, int]) -> None:
            self.text = text
            self.image: pygame.Surface = pygame.Surface(size)
            self.rect: pygame.Rect = pygame.rect.Rect(position, size)
            # self.action = action
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
        self.seleceted_button:int = 0
        self._render_menu()

    def _create_buttons(self) -> None:
        size: tuple[int, int] = (int(WINDOW_SIZE[0] * 0.4), int(WINDOW_SIZE[1] * 0.1))
        start_position = size
        step = int(WINDOW_SIZE[1] * 0.2)
        start = ("Start", 0)
        quit = ("Exit", exit)
        buttons = [start, quit]
        for i, b in enumerate(buttons):
            position = (start_position[0], (start_position[1] + i * step))
            self.buttons.append(Menu.Button(b[0], size, position))

    def _render_menu(self) -> None:
        selected = self.buttons[self.seleceted_button % len(self.buttons)]
        print(selected.text, len(self.buttons))
        for btn in self.buttons:
            if btn == selected:
                
                img = btn.image.copy()
                img.set_colorkey((255, 0, 0))
                print("btn selected", type(img))
            else:
                img = btn.image
            
            self.image.blit(img, btn.rect)

    def process(self, ents: list[pygame.event.Event], screen: pygame.Surface) -> bool:
        for event in ents:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    # rotate selected button up
                    self.seleceted_button += 1
                    ...
                if event.key == pygame.K_s:
                    # rotate selected button down
                    self.seleceted_button -= 1
                    ...
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return 0
                if event.key == pygame.K_RETURN:
                    if self.buttons[
                        self.seleceted_button % len(self.buttons)
                        ] == "Start":
                        return 1
            if event.type == pygame.QUIT:
                exit()
        # show the menu
        self._render_menu()
        screen.blit(self.image, dest=(0, 0))
        return 2

        

    def open_menu(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (0, 0))
