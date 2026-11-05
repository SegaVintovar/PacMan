WINDOW_SIZE = (1400, 1200)

TILE = 64  # cell size

SPRIE_SIZE = 44

HEADER_HEIGHT = int(WINDOW_SIZE[1] * 0.1)

KEY_DIRECTIONS: dict[str, tuple[int, int]] = {
    'W': (0, -1),
    'D': (1, 0),
    'S': (0, 1),
    'A': (-1, 0)
}

GHOSTS: dict[str, tuple[str, tuple[int, int]]] = {
    "Clyde": ("orange", (WINDOW_SIZE[0] - TILE // 2, TILE // 2)),
    "Inky": ("cyan", (TILE // 2, WINDOW_SIZE[1] - TILE // 2)),
    "Blinky": ("red", (TILE // 2, TILE // 2)),
    "Pinky": ("pink", (WINDOW_SIZE[0] - TILE // 2, WINDOW_SIZE[1] - TILE // 2))
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
