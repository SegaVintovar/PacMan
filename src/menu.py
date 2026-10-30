from . import Game
from .constants import FONT_SIZE, FONT_PATH, WINDOW_SIZE, PINK, CYAN
import pygame
from typing import Any
from typing import Callable


def lerp_color(a: tuple[int, int, int], b: tuple[int, int, int],
               t: float) -> tuple[int, int, int]:
    """Blend colour a into colour b. t=0 gives a, t=1 gives b."""
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )

class Menu():
    class Button():
        def __init__(self, text: str, size: tuple[int, int], position: tuple[int, int]) -> None:
            self.text = text
            self.image: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA)
            self.rect: pygame.Rect = pygame.rect.Rect(position, size)
            # self.action = action
            # self.highlighted: bool = True
            self.font: pygame.font.Font = pygame.font.Font(FONT_PATH, FONT_SIZE)
            # self.font: pygame.font.Font = pygame.font.SysFont("Arial", FONT_SIZE)
            self.font_color: pygame.color.Color = CYAN
            self.image.blit(
                self.font.render(self.text, True, self.font_color),
                dest=(0, 0)
                )

        def update_button_image(self, selected: bool) -> None:
            font_color = self.font_color if not selected else PINK
            self.image.blit(
                self.font.render(self.text, True, font_color),
                dest=(0, 0)
                )

        # def execute(self, *arg: Any) -> None:
        #     self.action(arg)


    def __init__(self, game: Game):
        # image is a background
        self.image: pygame.Surface = self._make_gradient((WINDOW_SIZE[0], WINDOW_SIZE[1] + 200))
        self.buttons: list[Menu.Button] = []
        self.game = game
        # self.background: pygame.Surface = 
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
        selected = self.seleceted_button % len(self.buttons)
        print(selected, len(self.buttons))
        for i, btn in enumerate(self.buttons):
            btn.update_button_image(selected=(i == selected))
            img = btn.image.copy()
            if i == selected:
                btn.rect = pygame.draw.rect(img, PINK, btn.rect, width=4)
                
                print("btn selected", type(img))
            
            self.image.blit(img, btn.rect)

    def _make_gradient(self, size: tuple[int, int]) -> pygame.Surface:
        """Sunset gradient: dark purple at the top, pink at the bottom."""
        surface = pygame.Surface(size)
        top = (25, 5, 60)
        bottom = (255, 90, 140)
        for y in range(size[1]):
            color = lerp_color(top, bottom, y / size[1])
            pygame.draw.line(surface, color, (0, y), (size[0], y))
        return surface

    def process(self, ents: list[pygame.event.Event], screen: pygame.Surface) -> bool:
        for event in ents:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    # rotate selected button up
                    self.seleceted_button += 1
                if event.key == pygame.K_s:
                    # rotate selected button down
                    self.seleceted_button -= 1
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return 0
                if event.key == pygame.K_RETURN:
                    print("return")
                    if self.buttons[
                        self.seleceted_button % len(self.buttons)
                        ].text == "Start":
                        print("start")
                        return 1
                    else:
                        return 0
            if event.type == pygame.QUIT:
                exit()
        self._render_menu()
        screen.blit(self.image, dest=(0, 0))
        return 2

        

    def open_menu(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (0, 0))
