from src import Game, GameConfig
import pygame
import sys
import json
from pydantic import ValidationError


def validate_config(setting: int) -> GameConfig:
    if setting == 1:
        if not len(sys.argv) == 2:
            # print(sys.argv)
            raise EOFError("Only one argument is required")
        elif not sys.argv[1].endswith(".json"):
            raise TypeError("'.json' file format is expected")
        # here we should try to load config from argument of the pac-man.py,
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
            raise ValidationError("Could not validate the config")
        else:
            return our_config
    else:
        with open("storage/config.json", mode="r") as file:
            cfg = json.loads(file.read())
        return GameConfig(**cfg)


def main():
    try:
        our_config: GameConfig = validate_config(1)
    except Exception as e:
        print(f"Could start the PacMan with given config {sys.argv[1]}")
        print(f"The error was: {str(e)}")
        print("\n\nStarting the Game with default config\n\n")
        our_config = validate_config()

    print("config validated")
    mygame = Game(our_config)
    # screen = mygame.screen
    running = True
    while running:
        mygame.process(pygame.event.get())
        mygame.clock.tick(60)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
