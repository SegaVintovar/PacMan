
from typing import Any


class Map:
    def __init__(self, config: dict[str, Any]) -> None:
        self.pacgum: int = int(config["pacgum"])
        self.width: int = int(config["width"])
        self.height: int = int(config["height"])
        self.seed: int = int(config["seed"])
