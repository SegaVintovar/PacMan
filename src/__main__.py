
import pygame
import sys
import json
from typing import Any
from .config import GameConfig


def __main__() -> None:
    try:
        if not len(sys.argv) == 2:
            raise EOFError("Only one argument is required")
        elif not sys.argv[1] == "config.json":
            raise NameError("'config.json' is expected")
        
        pygame.init()

        screen = pygame.display.set_mode()
        x, y = screen.get_size()

        width = int(x * 0.8)
        height = int(y * 0.9)
        print(f"display information;\nx: {width}, y: {height}")
        screen = pygame.display.set_mode((width, height))
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
