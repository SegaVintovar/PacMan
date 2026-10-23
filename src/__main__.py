import pygame
import sys
import json
from typing import Any
from .config import GameConfig
from .map import Map
from .pacman import Pacman
from pydantic_extra_types.coordinate import Coordinate
from pydantic import ValidationError
from .game import Game
from . import Maze


TILE_SIZE = 64
WINDOW_SIZE = (1400, 1080)


class Gum():
    def __init__(self, position: Coordinate) -> None:
        self.position = position
        self.sprite = pygame.Rect(self.position[0], self.position[1], 5, 5)


def validate_config() -> GameConfig:
    if not len(sys.argv) == 2:
        # print(sys.argv)
        raise EOFError("Only one argument is required")
    elif not sys.argv[1].endswith(".json"):
        raise TypeError("'.json' file format is expected")
    # here we should try to load config from argument list,
    # but in case it is not possible we should run the game with default one
    # this is according to the subject!
    # NOT DONE YET!!!!
    try:
        with open(sys.argv[1], mode="r") as file:
            cfg = json.loads(file.read())
        our_config = GameConfig(**cfg)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file {sys.argv[1]}")
    except PermissionError:
        raise PermissionError(f"Could not open the file {sys.argv[1]}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Broken JSON")
    except ValidationError:
        raise ValidationError("Config file is incorrect")
    else:
        return our_config


def load_the_game(our_config: GameConfig) -> Game:
    """
    made to init the game
    """
    new_game = Game(our_config, Maze)
    
    ...


def __main__() -> None:
    try:
        # validation
        our_config: GameConfig = validate_config()
        the_game = load_the_game(our_config=our_config)
        pygame.init()

        screen: pygame.Surface = pygame.display.set_mode(
            (WINDOW_SIZE[0], WINDOW_SIZE[1]))
        # goes into the game
        pygame.display.set_caption("Hello Pygame for pac-man")
        # one map per level???
        ourMap = Map(config=our_config)

        ourHero: Pacman = Pacman(ourMap, config=cfg)

        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # game.run(screen)
            scaled_map = pygame.transform.scale(ourMap.map_image, WINDOW_SIZE)
            screen.blit(scaled_map, dest=(0, 0))
            ourHero.spawn(screen)
            pygame.display.update()
        pygame.quit()
    except (EOFError, NameError) as err:
        print(f"couldn't run Pac-Man: {err}")
    finally:
        print("Exited PacMan successfully")
        sys.exit()


if __name__ == "__main__":
    __main__()
