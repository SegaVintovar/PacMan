import pygame
from .config import GameConfig
from .constants import WINDOW_SIZE, HEADER_HEIGHT
from .game import Game
from .menu import Menu


class App():
    """
    Handles final output, by knowing current state
    delegates input.
    Two members Game and Menu.
    also own main screen(WINDOW)

    """
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        pygame.init()
        screen = pygame.display.set_mode(
            (WINDOW_SIZE[0], WINDOW_SIZE[1] + HEADER_HEIGHT * 2))
        self.screen: pygame.Surface = screen  # 1. window first
        clock = pygame.time.Clock()
        self.clock: pygame.time.Clock = clock
        self.game: Game = Game(config=self.config)
        self.menu: Menu = Menu(self.game)
        self.state: Game | Menu = self.menu

    # if  state returns some value we are checking it and making some desicions
    # if 1 then  self.state = self.game
    # if 2 then self.state = self.menu
    # if 0 then exit()
    def process(self, evns: list[pygame.event.Event]) -> bool:
        state = self.state.process(evns, self.screen)
        if state == 1:
            self.state = self.game
            self.game.process(evns, self.screen)
            # self.screen.blit(self.game.image, dest=(0, 0))
            return True
        if state == 2:
            self.state = self.menu
            self.screen.blit(self.menu.image, dest=(0, 0))
            return True
        if state == 0:
            return False
