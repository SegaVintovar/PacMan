from .module import Module
from .gradient import make_gradient
from .game_state import GameState
from pygame import Surface
from .button import Button
from .constants import WINDOW_SIZE
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
        self.buttons: list[Button] = []

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
                            gs.running = False
                            gs.next_module = 0
                        elif b.text == "Continue":
                            gs.next_module = 1
                        elif b.text == "Save the score":
                            gs.next_module = 6
                        elif b.text == "Back to menu":
                            gs.next_module = 2
                        return gs
                        # keyboard events handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.seleceted_button -= 1
                if event.key == pygame.K_s:
                    self.seleceted_button += 1
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    gs.next_module = 0
                    gs.running = False
                    return gs
                if event.key == pygame.K_RETURN:
                    print("return")
                    if self.buttons[
                        self.seleceted_button % len(self.buttons)
                    ].text == "Start":
                        # if self.game.paused:
                        #     self.game.footer.timer.resume()
                            # self.game.timer
                        gs.next_module = 1
                        return gs
                    elif self.buttons[
                        self.seleceted_button % len(self.buttons)
                    ].text == "ScoreBoard":
                        gs.next_module = 3
                        return gs
                    elif self.buttons[
                        self.seleceted_button % len(self.buttons)
                    ].text == "Instructions":
                        gs.next_module = 4
                        return gs
                    else:
                        gs.next_module = 0
                        gs.running = False
                        return gs
            if event.type == pygame.QUIT:
                exit()
        self._show_pause_menu(screen)
        return gs

    def _create_buttons(self) -> None:
        size: tuple[int, int] = (
            int(WINDOW_SIZE[0] * 0.4), int(WINDOW_SIZE[1] * 0.05)
            )
        buttons = ["Continue", "Save the score", "Back to menu", "Exit"]
        start_position = (size[0] * 0.7, int(WINDOW_SIZE[1] * 0.4))
        step = int(WINDOW_SIZE[1] * 0.1)
        for i, b in enumerate(buttons):
            self.buttons.append(
                Button(
                    b,
                    size,
                    (start_position[0], start_position[1] + i * step))
            )

    def _show_pause_menu(self, screen: pygame.Surface) -> None:
