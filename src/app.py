import pygame
from .config import GameConfig
from .constants import WINDOW_SIZE, HEADER_HEIGHT
from .game import Game
from .menu import Menu
import json
from .scoreboard import ScoreBoard
from .gradient import make_gradient
# from typing import Any
from .game_state import GameState
from .module import Module
from .instructions import Instructions
from .pause import Pause
from .win_loose import Win, Loose


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
        self.background = make_gradient()
        # info = pygame.display.Info()
        # screen = pygame.display.set_mode(
        #     (info.current_w, info.current_h),
        #     pygame.FULLSCREEN)
        self.screen: pygame.Surface = screen
        clock = pygame.time.Clock()
        self.clock: pygame.time.Clock = clock
        # init game state with the menu at the start
        self.app_state = GameState(2, True, "")
        # then initializing all modules of the app
        self.game: Game = Game(config=self.config)
        self.menu: Menu = Menu(self.background.copy())
        self.scoreboard: ScoreBoard = ScoreBoard(self.background.copy())
        self.intructions: Instructions = Instructions(
            self.background.copy(),
            config=config)
        self.pause = Pause(self.background.copy())
        self.win = Win(self.background.copy())
        self.loose = Loose(self.background.copy())
        # do i need this list? dict feels better
        self.modules: list[Module]
        self.dict_modules: dict[int, Module] = {
            1: self.game,
            2: self.menu,
            3: self.scoreboard,
            4: self.intructions,
            5: self.pause,
            6: self.win,
            7: self.loose,
            0: None
        }
        self.state: Module = self.dict_modules[self.app_state.next_module]

    # if  state returns some value we are checking it and making some decisions
    # if 1 then  self.state = self.game
    # if 2 then self.state = self.menu
    # if 3 then self.scoreboard
    # if 4 then instructions
    # if 5 then self.pause
    # if 6 then self.win
    # if 7 then self.loose
    # if 0 then exit()
    # for the module process we need:
    #       1. events
    #       2. gamestate
    #       3. main_screen
    def process(self, evns: list[pygame.event.Event]) -> bool:
        gs = self.state.process(evns, self.app_state, self.screen)
        next_module = gs.next_module
        if next_module == 0:
            return False
        self.state = self.dict_modules[next_module]
        return True

    # def _open_scoreboard_file(self) -> dict:
    #     """
    #     Open, read and save it to the self.scoreboard
    #     """
    #     with open(self.scoreboard_file, "r") as file:
    #         self.scores = json.load(file.read())
    #     with open(self.scoreboard_file, "w") as file:
    #         self.scoreboard = json.load(file.read())

    def _save_results(self) -> None:
        with open(self.scoreboard_file, "w+") as file:
            file.write(json.dumps(str(self.scores)))
            print("File scores.json was updated")
