import pygame
import sys
import json
from .config import GameConfig
from pydantic import ValidationError
from .game import Game
from . import MazeGenerator


def validate_config(argv: list[str]) -> GameConfig:
    if not len(argv) == 2:
        # print(sys.argv)
        raise EOFError("Only one argument is required")
    elif not sys.argv[1].endswith(".json"):
        raise TypeError("'.json' file format is expected")
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
    except ValidationError as e:
        raise e
    else:
        return our_config


def __main__() -> None:
    try:
        our_config: GameConfig = validate_config(sys.argv)
    except Exception as e:
        print(f"Could not validate given configuration file: {str(e)}")
        print("Recovering the start up with default config")
        try:
            with open("storage/config.json", mode="r") as file:
                cfg = json.loads(file.read())
            our_config = GameConfig(**cfg)
        except Exception as e:
            print(f"Could not open and validate default config: {str(e)}")
            sys.exit(1)
    print("config validated")

    mygame = Game(our_config, MazeGenerator)
    running: bool = True
    while running:        
        running = mygame.process(pygame.event.get())
        mygame.clock.tick(60)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    __main__()
