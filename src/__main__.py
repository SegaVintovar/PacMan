
import pygame
import sys
import json
from typing import Any
from .config import GameConfig


def __main__() -> None:
    try:
        if not len(sys.argv) == 1:
            raise EOFError("Only one argument is required")
        elif not sys.argv[1] == "config.json":
            raise NameError("'config.json' is expected")
        
        pygame.init()

        screen: Any = pygame.display.set_mode((1280, 1480))
        pygame.display.set_caption("Hello Pygame for pac-man")
        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()
    except (EOFError, NameError) as err:
        print(f"couldn't run Pac-Man: {err}")


if __name__ == "__main__":
    __main__()
