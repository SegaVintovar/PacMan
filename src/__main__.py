import pygame
import sys
import json
from typing import Any
from .config import GameConfig
from .map import Map

class Game():
    def __init__() -> None:
        ...


def __main__() -> None:
    try:
        with open(sys.argv[1], mode="r") as file:
            cfg = json.loads(file.read())
        our_config = GameConfig(**cfg)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file {sys.argv[1]}")
    except PermissionError:
        raise PermissionError(f"Could not open the file {sys.argv[1]}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Broken JSON {str(e)}")


    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode(
        (our_config.width * 32, our_config.height * 32))
    pygame.display.set_caption("Hello Pygame for pac-man")
    # one map per level???
    ourMap = Map(config=cfg)

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(ourMap.map_image, dest=(0, 0))
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    __main__()
