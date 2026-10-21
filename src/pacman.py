
from typing import Any


class Pacman:
    def __init__(self, config: dict[str, Any]) -> None:
        self.x: int = int(config["width"] / 2)
        self.y: int = int(config["height"] / 2)
        self.lives: int = int(config["lives"])
        self.points: int = 0
        self.lastDirection: str = '0'

    def move(keyEvent: Any) -> None:
        ...
