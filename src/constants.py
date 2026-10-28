WINDOW_SIZE = (1200, 800)

TILE = 64  # cell size

SPRIE_SIZE = 44

HEADER_HEIGHT = 100

KEY_DIRECTIONS: dict[str, tuple[int, int]] = {
    'W': (0, -1),
    'D': (1, 0),
    'S': (0, 1),
    'A': (-1, 0)
}
