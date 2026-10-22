import pygame
import sys
import json
from typing import Any
from .config import GameConfig
from .map import Map


TILE_SIZE = 64
WINDOW_SIZE = (1400, 1080)


class Gum():
    def __init__(self) -> None:
        self.position


class Game():
    """
    takes a Surface of the main screen and blits
    1) Map once per lvl
    2) gums 
    """
    def __init__() -> None:
        ...


def __main__() -> None:
    try:
        # validation
        if not len(sys.argv) == 2:
            # print(sys.argv)
            raise EOFError("Only one argument is required")
        elif not sys.argv[1] == "config.json":
            raise NameError("'config.json' is expected")

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
        # game.init(cfg)
        
        screen: pygame.Surface = pygame.display.set_mode(
            (WINDOW_SIZE[0], WINDOW_SIZE[1]))
        # goes into the game
        pygame.display.set_caption("Hello Pygame for pac-man")
        # one map per level???
        ourMap = Map(config=our_config)

        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # game.run(screen)
            scaled_map = pygame.transform.scale(ourMap.map_image, WINDOW_SIZE)
            screen.blit(scaled_map, dest=(0, 0))
            pygame.display.update()
        pygame.quit()
    except (EOFError, NameError) as err:
        print(f"couldn't run Pac-Man: {err}")


if __name__ == "__main__":
    __main__()
