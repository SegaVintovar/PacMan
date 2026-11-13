from src.app import App
import pygame
import sys
from src.config import GameConfig

default_config = {
    "highscore_filename": "scores.json",
    "level": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "lives": "3",
    "pacgum": "10",
    "points_per_pacgum": "10",
    "points_per_super_pacgum": "50",
    "points_per_ghost": "200",
    "width": "12",
    "height": "12",
    "seed": "42",
    "level_max_time": "60"
}


def main():
    try:
        if len(sys.argv) != 2:
            raise Exception(
                "The game has to be launched as: \
                    $python pac-man.py config.json" +
                "\n Probably the argument is missing")
        if not sys.argv[1].endswith(".json"):
            raise Exception("The config file has to be .json format")
        config = GameConfig(sys.argv[1])
    except Exception as e:
        print("Could not validate given config file", str(e))
        print("Launching the game with default config")
        config = default_config
    # here we also need try,
    # so image load or bad config,
    # or maze gen fail
    # not gonna give traceback
    mygame = App(config)
    running: bool = True
    while running:
        running = mygame.process(pygame.event.get())
        mygame.clock.tick(60)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
