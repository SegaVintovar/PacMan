from .paths import ASSETS_DIR

WINDOW_SIZE = (1400, 1200)

NEW_SIZE = (1400, 1200)
DEST = (0, 0)


SPEED: int = 3
SPEEDS: dict[str, float] = {
    "pacman": 2.6,
    "ghost": 2.9,
    "ghost_coward": 1.5,
    "ghost_eaten": 5.5
}

FPS = 60
TILE = 64  # cell size

SPRIE_SIZE = 44

HEADER_HEIGHT = int(WINDOW_SIZE[1] * 0.1)

KEY_DIRECTIONS: dict[str, tuple[int, int]] = {
    'W': (0, -1),
    'D': (1, 0),
    'S': (0, 1),
    'A': (-1, 0)
}

GHOST_DIRECTIONS: dict[str, tuple[int, int]] = {
    'up': (0, -1),
    'right': (1, 0),
    'down': (0, 1),
    'left': (-1, 0)
}

GHOSTS: dict[str, tuple[str, tuple[str, str], int]] = {
    "Clyde": ("orange", ('right', 'top'), 2),
    "Inky": ("cyan", ('left', 'bottom'), 2),
    "Blinky": ("red", ('left', 'top'), 3),
    "Pinky": ("pink", ('right', 'bottom'), 1)
}

GHOST_COWARD_TIME: int = 8

# FONT_SIZE = int(WINDOW_SIZE[0] * WINDOW_SIZE[1] / 18000)
FONT_SIZE = 30
# colors for the menu
PINK = (255, 80, 180)
CYAN = (0, 230, 255)
WHITE = (235, 235, 235)
BLACK = (0, 0, 0)
SPEED

FONT_PATH = ASSETS_DIR / "fonts" / "Bungee-Regular.ttf"

MAX_SCORES = 10

WALL_COLOR = "darkorchid1"
