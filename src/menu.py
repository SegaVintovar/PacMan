from .constants import WINDOW_SIZE, PINK
import pygame
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
        start = ("Start", 1)
        # cntinue = "Continue"
        score_board = ("ScoreBoard", 3)
        instructions = ("Instructions", 4)
        quit = ("Exit", 0)
        buttons = [start, score_board, instructions, quit]
        for i, b in enumerate(buttons):
            position = (start_position[0], (start_position[1] + i * step))
            self.buttons.append(Button(b[0], size, position, b[1]))

    def _render_menu(self) -> None:
        selected = self.seleceted_button % len(self.buttons)
        base = self.background.copy()
        for i, btn in enumerate(self.buttons):
            btn.update_button_image(selected=(i == selected))
            img = btn.image.copy()
            if i == selected:
                frame = img.get_rect()
                pygame.draw.rect(img, PINK, frame, width=4)
            base.blit(img, btn.rect)
        self.image = base

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
                        game_state.gs_update(b.go_to_module)
                        return game_state
            # keyboard events handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.seleceted_button -= 1
                elif event.key == pygame.K_s:
                    self.seleceted_button += 1
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    game_state.quit()
                    return game_state
                    # return (0, None)
                if event.key == pygame.K_RETURN:
                    print("return")
                    seleceted_button = self.buttons[
                        self.seleceted_button % len(self.buttons)
                    ]
                    game_state.gs_update(seleceted_button.go_to_module)
                    return game_state
            if event.type == pygame.QUIT:
                exit()
        self._render_menu()
        screen.blit(self.image, dest=(0, 0))
        return game_state
