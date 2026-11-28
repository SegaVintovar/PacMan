from src.app import App
import pygame
import sys
from src.config import GameConfig
from src.constants import FPS


def main() -> None:
    try:
        if len(sys.argv) != 2:
            raise Exception(
                "The game has to be launched as: \
                    $python pac-man.py config.json" +
                "\n Probably the argument is missing")
        if not sys.argv[1].endswith(".json"):
            raise Exception("The config file has to be .json format")
        config = GameConfig(sys.argv[1])
        print(f"{sys.argv[1]} is validated!")
    except Exception as e:
        print("Could not validate given config file", str(e))
        print("Launching the game with default config")
        config = GameConfig()
    try:
        mygame = App(config)
    except FileNotFoundError as e:
        print("Instantiation of the App failed due to missing file\n", str(e))
        sys.exit(1)
    except Exception as e:
        print("Could not init the App", repr(e))
        sys.exit(1)
    running: bool = True
    while running:
        running = mygame.process(pygame.event.get())
        mygame.clock.tick(FPS)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
