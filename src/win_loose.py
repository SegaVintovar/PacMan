from .module import Module
from .gradient import make_gradient
from pygame import Surface
from pygame.event import Event
from .game_state import GameState
from .button import Button


def process_txt_input():
    ...
    


# enter your name to add the score with a name to the scoreslist
# how to pass score from here to the 
class WinLoose(Module):
    def __init__(self, bg: Surface) -> None:
        self.background = bg
        self.player_name: str = "Player"
        self.score: int = 0
        self.buttons: Button = []

    # here we need to handle keyboard input
    # start with "" or player name
    # then track all the stuff that came it
    def process(self,
                events: list[Event],
                gs: GameState) -> GameState:
        ...

    def _save_score(self) -> None:
        ...


class Loose(Module):
    def __init__(self, bg: Surface) -> None:
        self.background = bg
        self.looser_name: str = "Player"
        self.score: int = 0

    def process(
            self, events: list[Event], gs: GameState, screen: Surface
            ) -> GameState:
        ...