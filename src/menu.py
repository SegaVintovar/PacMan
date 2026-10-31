from . import Game
from .constants import FONT_SIZE, FONT_PATH, WINDOW_SIZE, PINK, CYAN, \
    HEADER_HEIGHT
import pygame


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
        def __init__(self,
                     text: str,
                     size: tuple[int, int],
                     position: tuple[int, int]
                     ) -> None:
            self.text = text
            self.image: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA)
            self.rect: pygame.Rect = pygame.rect.Rect(position, size)
            # self.action = action
            # self.highlighted: bool = True
            self.font: pygame.font.Font = pygame.font.Font(
                FONT_PATH, FONT_SIZE)
            # self.font: pygame.font.Font = pygame.font.SysFont(
            # "Arial", FONT_SIZE)
            self.font_color: pygame.color.Color = PINK
            self.image.blit(
                self.font.render(self.text, True, self.font_color),
                dest=(FONT_SIZE * 3, FONT_SIZE // 2)
                )

        def update_button_image(self, selected: bool) -> None:
            font_color = self.font_color if not selected else CYAN
            self.image.blit(
                self.font.render(self.text, True, font_color),
                dest=(FONT_SIZE * 3, FONT_SIZE // 2)
                )
            # if selected:
            #     pygame.draw.rect(self.image, PINK, self.rect, width=4)
        # def execute(self, *arg: Any) -> None:
        #     self.action(arg)

    def __init__(self, game: Game):
        # image is a background
        self.background = self._make_gradient(
            (WINDOW_SIZE[0], WINDOW_SIZE[1] + HEADER_HEIGHT * 2))
        self.image: pygame.Surface = self.background.copy()
        self.buttons: list[Menu.Button] = []
        self.game = game # no need?
        self._create_buttons()
        self.seleceted_button: int = 0
        self._render_menu()

    def _create_buttons(self) -> None:
        size: tuple[int, int] = (
            int(WINDOW_SIZE[0] * 0.4), int(WINDOW_SIZE[1] * 0.1)
            )
        start_position = (size[0] * 0.7, int(WINDOW_SIZE[1] * 0.4))
        # start_position[1] = WINDOW_SIZE[1] * 0.2
        step = int(WINDOW_SIZE[1] * 0.2)
        start = ("Start", 0)
        quit = ("Exit", exit)
        buttons = [start, quit]
        for i, b in enumerate(buttons):
            position = (start_position[0], (start_position[1] + i * step))
            self.buttons.append(Menu.Button(b[0], size, position))

    def _render_menu(self) -> None:
        selected = self.seleceted_button % len(self.buttons)
        base = self.background.copy()
        # print(selected, len(self.buttons))
        for i, btn in enumerate(self.buttons):
            btn.update_button_image(selected=(i == selected))
            # btn.rect.inflate(8, 8)
            img = btn.image.copy()
            if i == selected:
                frame = img.get_rect()
                # frame = frame.inflate(8, 8)
                pygame.draw.rect(img, PINK, frame, width=4)
            base.blit(img, btn.rect)
        self.image = base

    def _make_gradient(self, size: tuple[int, int]) -> pygame.Surface:
        """Sunset gradient: dark purple at the top, pink at the bottom."""
        surface = pygame.Surface(size)
        top = (25, 5, 60)
        bottom = (255, 90, 140)
        for y in range(size[1]):
            color = lerp_color(top, bottom, y / size[1])
            pygame.draw.line(surface, color, (0, y), (size[0], y))
        logo_path = "src/assets/menu/FT_PacMan.png"
        logo = pygame.image.load(logo_path).convert_alpha()
        surface.blit(
            pygame.transform.scale(logo,
                                   (WINDOW_SIZE[0] * 0.4,
                                    WINDOW_SIZE[1] * 0.4)),
            (WINDOW_SIZE[0] * 0.3, WINDOW_SIZE[1] * 0.02)
            )
        return surface

    def process(
            self, ents: list[pygame.event.Event], screen: pygame.Surface
            ) -> bool:
        for event in ents:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # mouse = pygame.Rect((x, y), (5, 5))
                for b in self.buttons:
                    print(b.text, )
                    if b.rect.collidepoint(x, y):
                        print("Mouse button", b.text, x, y)
                        if b.text == "Exit":
                            return 0
                        if b.text == "Start":
                            if self.game.paused:
                                self.game.footer.timer.resume()
                                self.game.timer
                            # print("")
                            return 1

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
                        if self.game.paused:
                            self.game.footer.timer.resume()
                            self.game.timer
                        print("start")
                        return 1
                    else:
                        return 0
            if event.type == pygame.QUIT:
                exit()
        self._render_menu()
        screen.blit(self.image, dest=(0, 0))
        return 2

    # def open_menu(self, screen: pygame.Surface) -> None:
    #     screen.blit(self.image, (0, 0))
