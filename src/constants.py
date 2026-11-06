WINDOW_SIZE = (1400, 1200)

TILE = 64  # cell size

SPRIE_SIZE = 44

HEADER_HEIGHT = int(WINDOW_SIZE[1] * 0.1)

KEY_DIRECTIONS: dict[str, tuple[int, int]] = {
    'W' or 'up': (0, -1),
    'D' or 'right': (1, 0),
    'S' or 'down': (0, 1),
    'A' or 'left': (-1, 0)
}

GHOSTS: dict[str, tuple[str, tuple[str, str]]] = {
    "Clyde": ("orange", ('right', 'top')),
    "Inky": ("cyan", ('left', 'bottom')),
    "Blinky": ("red", ('left', 'top')),
    "Pinky": ("pink", ('right', 'bottom'))
}

SPEED: int = 3

FONT_SIZE = int(WINDOW_SIZE[0] * WINDOW_SIZE[1] / 18000)
FONT_SIZE = 50
# colors for the menu
PINK = (255, 80, 180)
CYAN = (0, 230, 255)
WHITE = (235, 235, 235)
BLACK = (0, 0, 0)

FONT_PATH = "src/assets/fonts/Bungee-Regular.ttf"

MAX_SCORES = 10

WALL_COLOR = "darkorchid1"
