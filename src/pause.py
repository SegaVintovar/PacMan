from .module import Module
from .gradient import make_gradient
from .game_state import GameState
from pygame import Surface
from .button import Button
from .constants import WINDOW_SIZE, HEADER_HEIGHT, PINK
import pygame


class Pause(Module):
    """
    4 buttons:
    - continue
    - save the result
    - back to menu
    - exit
    """
    def __init__(self, bg: Surface) -> None:
        self.background = bg
        self.selected_button: int = 0
        self.image: Surface
        self.buttons: list[Button] = []
        self._create_buttons()

    def process(self,
                events: list[pygame.event.Event],
                gs: GameState,
                screen: pygame.Surface) -> GameState:
        for event in events:
            # mouse handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for b in self.buttons:
                    if b.rect.collidepoint(x, y):
                        print("Mouse button", b.text, x, y)
                        if b.text == "Exit":
                            gs.gs_update(0)
                        elif b.text == "Continue":
                            gs.gs_update(1)
                        elif b.text == "Save the score":
                            gs.gs_update(6)
                        elif b.text == "Back to menu":
                            gs.gs_update(2)
                        return gs
                        # keyboard events handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.selected_button -= 1
                if event.key == pygame.K_s:
                    self.selected_button += 1
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    gs.next_module = 0
                    gs.running = False
                    return gs
                if event.key == pygame.K_RETURN:
                    print("return")
                    selected_button = self.buttons[
                        self.selected_button % len(self.buttons)
                    ]
                    gs.gs_update(selected_button.go_to_module)
                    return gs
            if event.type == pygame.QUIT:
                exit()
        self._show_pause_menu(screen)
        return gs

    def _create_buttons(self) -> None:
        size: tuple[int, int] = (
            int(WINDOW_SIZE[0] * 0.4), int(WINDOW_SIZE[1] * 0.05)
            )
        buttons = [
            ("Continue", 1),
            ("Save the score", 6),
            ("Back to menu", 2),
            ("Exit", 0)
            ]
        start_position = (size[0] * 0.7, int(WINDOW_SIZE[1] * 0.4))
        step = int(WINDOW_SIZE[1] * 0.1)
        for i, b in enumerate(buttons):
            self.buttons.append(
                Button(
                    b[0],
                    size,
                    (start_position[0], start_position[1] + i * step),
                    b[1]
                    )
            )

    def _render_menu(self) -> None:
        selected = self.selected_button % len(self.buttons)
        base = self.background.copy()
        for i, btn in enumerate(self.buttons):
            btn.update_button_image(selected=(i == selected))
            img = btn.image.copy()
            if i == selected:
                frame = img.get_rect()
                pygame.draw.rect(img, PINK, frame, width=4)
            base.blit(img, btn.rect)
        self.image = base

    def _show_pause_menu(self, screen: pygame.Surface) -> None:
        self._render_menu()
        screen.blit(self.image, dest=(0, 0))
        for b in self.buttons:
            screen.blit(b.image, dest=b.rect)
