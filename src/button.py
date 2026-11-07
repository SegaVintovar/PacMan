import pygame
from .constants import FONT_PATH, FONT_SIZE, PINK, CYAN


class Button():
    def __init__(self,
                 text: str,
                 size: tuple[int, int],
                 position: tuple[int, int]
                 ) -> None:
        self.text = text
        self.image: pygame.Surface = pygame.Surface(
            size, pygame.SRCALPHA)
        self.rect: pygame.Rect = pygame.rect.Rect(position, size)
        self.font: pygame.font.Font = pygame.font.Font(
            FONT_PATH, FONT_SIZE)
        self.font_color: pygame.color.Color = PINK
        self.image.blit(
            self.font.render(self.text, True, self.font_color),
            dest=(FONT_SIZE * 2, FONT_SIZE // 2)
            )

    def update_button_image(self, selected: bool) -> None:
        font_color = self.font_color if not selected else CYAN
        self.image.blit(
            self.font.render(self.text, True, font_color),
            dest=(FONT_SIZE * 2, FONT_SIZE // 2)
            )
