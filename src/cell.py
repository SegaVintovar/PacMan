import pygame

TILE = 64
WINDOW_SIZE = (1400, 1080)

class Cell():
    """Represents a single cell in the maze grid.

    Each cell has four walls (north, east, south, west) that can be either
    closed (True) or open (False), a position in the grid.

    Attributes:
        n: Boolean state of the north wall. True means wall is closed.
        e: Boolean state of the east wall. True means wall is closed.
        s: Boolean state of the south wall. True means wall is closed.
        w: Boolean state of the west wall. True means wall is closed.
        position: Tuple (x, y) with the cell's coordinates in the grid.
        special: String marker shown in the cell's center during rendering.
    """
    def __init__(
            self,
            n: bool, e: bool, s: bool, w: bool, position: tuple[int, int],
            value: int, special: str = ""
            ) -> None:
        self.n = n
        self.e = e
        self.s = s
        self.w = w
        self.special = special
        self.position = position
        self.value = value
        self.surface: pygame.Surface | None = None
        self.set_surface()
        self.render_walls()

    def set_surface(self) -> None:
        self.surface = pygame.display.set_mode((TILE, TILE))

    def render_walls(self) -> None:
        # cell_base = pygame.Surface(size=(TILE, TILE))
        if self.value == 15:
            self.surface.fill()
        walls = []
        # cell_base.set_alpha()
        if self.n:
            walls.append(pygame.Rect((0, 0), (TILE, 4)))
        if self.e:
            walls.append(pygame.Rect((TILE - 4, 0), (TILE, TILE)))
        if self.s:
            walls.append(pygame.Rect((0, TILE - 4), (TILE, TILE)))
        if self.w:
            walls.append(pygame.Rect((0, 0), (4, TILE)))
        for w in walls:
            pygame.draw.rect(self.surface, (255, 255, 255), w)

# pygame.Rect.collidelist()


if __name__ == "__main__":
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode(
        (WINDOW_SIZE[0], WINDOW_SIZE[1]))
    # pygame.display.set_caption("Hello Pygame for pac-man")

    cell = Cell(0, 1, 0, 1, (0, 0), 6)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(cell.surface, dest=(0, 0))
        pygame.display.update()

    pygame.quit()
