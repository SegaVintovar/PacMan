# from .game_state import GameState
from abc import ABC, abstractmethod
from pygame.event import Event
from pygame import Surface


class GameState():
    pass


class Module(ABC):
    def __init__(self) -> None:
        pass

    # what if i ll put all data into the GameState
    @abstractmethod
    def process(self,
                events: list[Event],
                game_state: GameState,
                screen: Surface
                ) -> GameState:
        pass
