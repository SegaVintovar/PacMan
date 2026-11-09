from . import Game
from .constants import FONT_SIZE, FONT_PATH, WINDOW_SIZE, PINK, CYAN, \
    HEADER_HEIGHT
import pygame
from typing import Any
# from .scoreboard import ScoreBoard
from .gradient import make_gradient
from .button import Button
from .game_state import GameState

class Menu():
    def __init__(self, bg: pygame.Surface):
        # image is a background
        # self.background = make_gradient(
        #     (WINDOW_SIZE[0], WINDOW_SIZE[1] + HEADER_HEIGHT * 2),
        #     True)
        self.background = bg
        self.image: pygame.Surface = self.background.copy()
        self.buttons: list[Button] = []
        # self.game = game
        self._create_buttons()
        self.seleceted_button: int = 0
        self._render_menu()

    def _create_buttons(self) -> None:
        size: tuple[int, int] = (
            int(WINDOW_SIZE[0] * 0.4), int(WINDOW_SIZE[1] * 0.05)
            )
        start_position = (size[0] * 0.7, int(WINDOW_SIZE[1] * 0.4))
        step = int(WINDOW_SIZE[1] * 0.1)
        start = "Start"
        # cntinue = "Continue"
        score_board = "ScoreBoard"
        instructions = "Instructions"
        quit = "Exit"
        buttons = [start, score_board, instructions, quit]
        for i, b in enumerate(buttons):
            position = (start_position[0], (start_position[1] + i * step))
            self.buttons.append(Button(b, size, position))

    def _render_menu(self) -> None:
        selected = self.seleceted_button % len(self.buttons)
        base = self.background.copy()
        # print(selected, len(self.buttons))
        for i, btn in enumerate(self.buttons):
            # if self.game.paused and btn.text == "Start":
            #     btn.text = "Continue"
            # if not self.game.paused and btn.text == "Continue":
            #     btn.text = "Start"
            btn.update_button_image(selected=(i == selected))
            # btn.rect.inflate(8, 8)
            img = btn.image.copy()
            if i == selected:
                frame = img.get_rect()
                # frame = frame.inflate(8, 8)
                # frame.move_ip(20, 0)
                pygame.draw.rect(img, PINK, frame, width=4)
            base.blit(img, btn.rect)
        self.image = base

    # def _make_gradient(self, size: tuple[int, int]) -> pygame.Surface:
    #     """Sunset gradient: dark purple at the top, pink at the bottom."""
    #     surface = pygame.Surface(size)
    #     top = (25, 5, 60)
    #     bottom = (255, 90, 140)
    #     for y in range(size[1]):
    #         color = lerp_color(top, bottom, y / size[1])
    #         pygame.draw.line(surface, color, (0, y), (size[0], y))
    #     logo_path = "src/assets/menu/FT_PacMan.png"
    #     logo = pygame.image.load(logo_path).convert_alpha()
    #     surface.blit(
    #         pygame.transform.scale(logo,
    #                                (WINDOW_SIZE[0] * 0.4,
    #                                 WINDOW_SIZE[1] * 0.4)),
    #         (WINDOW_SIZE[0] * 0.3, WINDOW_SIZE[1] * 0.02)
    #         )
    #     return surface

    # now i want every module.process() return GameState

    def process(
            self,
            ents: list[pygame.event.Event],
            game_state: GameState,
            screen: pygame.Surface
            ) -> GameState:
        for event in ents:
            # mouse events handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for b in self.buttons:
                    if b.rect.collidepoint(x, y):
                        print("Mouse button", b.text, x, y)
                        if b.text == "Exit":
                            game_state.running = False
                            game_state.next_module = 0
                        elif b.text == "Start":
                            game_state.next_module = 1
                        elif b.text == "ScoreBoard":
                            game_state.next_module = 3
                        elif b.text == "Instructions":
                            game_state.next_module = 4
                        return game_state
            # keyboard events handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.seleceted_button -= 1
                if event.key == pygame.K_s:
                    self.seleceted_button += 1
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    game_state.next_module = 0
                    game_state.running = False
                    return game_state
                    # return (0, None)
                if event.key == pygame.K_RETURN:
                    print("return")
                    if self.buttons[
                        self.seleceted_button % len(self.buttons)
                    ].text == "Start":
                        # if self.game.paused:
                        #     self.game.footer.timer.resume()
                            # self.game.timer
                        game_state.next_module = 1
                        return game_state
                    elif self.buttons[
                        self.seleceted_button % len(self.buttons)
                    ].text == "ScoreBoard":
                        game_state.next_module = 3
                        return game_state
                    elif self.buttons[
                        self.seleceted_button % len(self.buttons)
                    ].text == "Instructions":
                        game_state.next_module = 4
                        return game_state
                    else:
                        game_state.next_module = 0
                        game_state.running = False
                        return game_state
            if event.type == pygame.QUIT:
                exit()
        self._render_menu()
        screen.blit(self.image, dest=(0, 0))
        return game_state

    # def open_menu(self, screen: pygame.Surface) -> None:
    #     screen.blit(self.image, (0, 0))
