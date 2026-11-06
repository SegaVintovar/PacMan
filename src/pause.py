from .module import Module
from .gradient import make_gradient
from .game_state import GameState
from pygame import Surface
from .button import Button


class Pause(Module):
    def __init__(self, bg: Surface) -> None:
        self.background = bg
        self.buttons: list[Button] = []

    def process(self, gs: GameState) -> GameState:
        ...

    def _create_buttons() -> None:
        buttons = {}
