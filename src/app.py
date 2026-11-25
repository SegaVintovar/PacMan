import pygame
import os
from .config import GameConfig
from .constants import (WINDOW_SIZE,
                        HEADER_HEIGHT,
                        GHOSTS, GHOST_DIRECTIONS, ASSETS_DIR)
from .game import Game
from .menu import Menu
from .scoreboard import ScoreBoard
from .gradient import make_gradient
from .game_state import GameState
from .module import Module
from .instructions import Instructions
from .pause import Pause
from .spriteBank import SpriteBank, SpriteLoadingError
from .win_loose import WinLoose
from typing import Any
from pathlib import Path


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
        pygame.mixer.init()
        screen = pygame.display.set_mode(
            (WINDOW_SIZE[0], WINDOW_SIZE[1] + HEADER_HEIGHT * 2))
        self.spriteErrors: list[SpriteLoadingError | NameError] = []
        self.screen: pygame.Surface = screen
        self.background = make_gradient()
        self.menu_background = make_gradient(extra=True)
        _sprites: Path = ASSETS_DIR / "sprites"
        _files: list[str] = [f for f in os.listdir(_sprites)]
        name: str = ""
        _key: str = ""
        for _f in _files:
            try:
                if not _f.islower() and '_' not in _f and ' ' in _f:
                    raise SpriteLoadingError(
                        "Sprite name is not snake_case", Path(_f))
                _surf: pygame.Surface = pygame.image.load(
                    f"{_sprites}/{_f}").convert_alpha()
                if not _surf:
                    raise SpriteLoadingError(
                        f"Sprite '{_f}' not found", Path(_f))
                pieces: str = os.path.splitext(_f)
                if not pieces[-1] == ".png":
                    raise SpriteLoadingError(
                        "Sprites should be a .png file", Path(_f))
                comp: list[str] = _f.split('_')
                if "pacman" in comp:
                    _key = "".join(
                        [c for c in comp
                         if 'W' in c or 'A' in c or 'S' in c or 'D' in c])
                    if _key in ("W", "A", "S", "D"):
                        name = os.path.splitext(f"{_key}-{comp[-1]}")[0]
                        SpriteBank.store(comp[0], name, _surf)
                    elif _key in "death":
                        _death: str = "".join(
                            [c for c in comp if c == "death"])
                        name = os.path.splitext(f"{_death}-{comp[-1]}")[0]
                        SpriteBank.store(comp[0], name, _surf)
                    else:
                        raise NameError("Pacman name must have W | A | S | D")
                elif "ghost" in comp:
                    _direction: str = "".join(os.path.splitext(comp[-1])[0])
                    name = "".join(
                        [_name for _name in GHOSTS.keys()
                         if GHOSTS[_name][0] in comp])
                    if not len(list(GHOSTS.keys())) == 4:
                        raise SpriteLoadingError(
                            "Not all ghost names are present", Path(_f))
                    if comp[1] not in GHOSTS[name][0]:
                        raise SpriteLoadingError(
                            f"invalid color of '{comp[1]}'", Path(_f))
                    if name in GHOSTS.keys():
                        SpriteBank.store(comp[0], f"{name}-{_direction}",
                                         _surf)
                    elif (name not in GHOSTS.keys() and
                          _direction in GHOST_DIRECTIONS.keys()):
                        SpriteBank.store(comp[0], f"eyes-{_direction}", _surf)
                    else:
                        _key = os.path.splitext(f"frightened-{comp[-1]}")[0]
                        SpriteBank.store(comp[0], _key, _surf)
                elif "fruit" in comp:
                    fruit: str = "".join(os.path.splitext(comp[-1])[0])
                    SpriteBank.store(comp[0], fruit, _surf)
                else:
                    raise NameError(f"Wrong sprite name '{" ".join(comp)}'")
            except NameError as err:
                print("Something went wrong with loading the sprites: ", err)
            except SpriteLoadingError as err:
                print("failed loading in the sprites: ", err)
                self.spriteErrors.append(err)
        clock = pygame.time.Clock()
        self.clock: pygame.time.Clock = clock
        self.app_state = GameState(2, True)
        # then initializing all modules of the app
        self.game: Game = Game(config=self.config)
        self.menu: Menu = Menu(self.menu_background.copy())
        self.scoreboard: ScoreBoard = ScoreBoard(self.background.copy(),
                                                 config)
        self.intructions: Instructions = Instructions(
            self.background.copy(),
            config=config)
        self.pause = Pause(self.background.copy())
        self.win_loose = WinLoose(self.background.copy(), config)
        self.dict_modules: dict[int, Any[Module]] = {
            1: self.game,
            2: self.menu,
            3: self.scoreboard,
            4: self.intructions,
            5: self.pause,
            6: self.win_loose,
            0: None
        }
        self.state: Module = self.dict_modules[self.app_state.next_module]

    # if  state returns some value we are checking it and making some decisions
    # if 1 then self.game
    # if 2 then self.menu
    # if 3 then self.scoreboard
    # if 4 then self.instructions
    # if 5 then self.pause
    # if 6 then self.win_loose
    # if 0 then exit()
    # for the Module.process() we need:
    #       1. events
    #       2. gamestate
    #       3. main_screen
    def process(self, evns: list[pygame.event.Event]) -> bool:
        gs: GameState = self.state.process(evns, self.app_state, self.screen)

        if gs.reload:
            self.game = Game(config=self.config)
            self.dict_modules[1] = self.game
            self.app_state = GameState(2, True)
            print("Game reloaded")
            gs = self.app_state
        next_module = gs.next_module
        if next_module == 0:
            return False
        self.state = self.dict_modules[next_module]
        return True
