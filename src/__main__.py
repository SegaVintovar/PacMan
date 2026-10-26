import pygame
import sys
import json
from .config import GameConfig
from pydantic_extra_types.coordinate import Coordinate
from pydantic import ValidationError
from .game import Game
from . import MazeGenerator

TILE = 64


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
        raise
    else:
        return our_config


def load_the_game(our_config: GameConfig) -> Game:
    """
    made to init the game
    """
    new_game = Game(our_config, MazeGenerator)
    return new_game


def __main__() -> None:
    # try:
    our_config: GameConfig = validate_config()
    print("config validated")

    # screen is being loading during Game init
    # pygame init also happens during Game init
    # screen: pygame.Surface = pygame.display.set_mode(
    #     (WINDOW_SIZE[0], WINDOW_SIZE[1]))
    # goes into the game
    # pygame.display.set_caption("Hello Pygame for pac-man")
    # one map per level???
    mygame = Game(our_config, MazeGenerator)
    print("mygame has done init")
    screen = mygame.screen
    mygame.display_one_map()

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    mygame.pacman.update_direction('W')
                elif event.key == pygame.K_a:
                    mygame.pacman.update_direction('A')
                elif event.key == pygame.K_s:
                    mygame.pacman.update_direction('S')
                elif event.key == pygame.K_d:
                    mygame.pacman.update_direction('D')
            if event.type == pygame.QUIT:
                running = False
        map_i = mygame.maps[0].map_image
        screen = mygame.screen
        scaled_map = pygame.transform.scale(map_i,
                                            (our_config.width * TILE,
                                             our_config.height * TILE))
        screen.blit(scaled_map, dest=(0, 0))
        mygame.render_creatures()
        pygame.display.flip()
        mygame.clock.tick(60)
        pygame.display.update()
    pygame.quit()
    # except Exception as err:
    #     print(f"couldn't run Pac-Man: {err}")
    # finally:
    #     print("Exited PacMan successfully")
    #     sys.exit()


if __name__ == "__main__":
    __main__()
