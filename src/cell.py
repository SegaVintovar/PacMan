import pygame

global TILE

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
        visited: True if generation algorithm has processed this cell.
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
        self.surface: pygame.Surface = self.render()

    def render(self) -> pygame.Surface:
        cell_base = pygame.Surface(size=(TILE, TILE))
        cell_base.set_alpha()
        if self.n:
            cell_base.blit(pygame.Rect((0, 0), (TILE, 4)))
        if self.e:
            cell_base.blit(pygame.Rect((TILE - 4, 0), (TILE, TILE)))
        if self.s:
            cell_base.blit(pygame.Rect((0, TILE - 4), (TILE, TILE)))
        if self.w:
            cell_base.blit(pygame.Rect((0, 0), (4, TILE)))
        return cell_base
            