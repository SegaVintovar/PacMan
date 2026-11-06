import pygame
from .constants import WINDOW_SIZE, HEADER_HEIGHT


def _lerp_color(a: tuple[int, int, int], b: tuple[int, int, int],
                t: float) -> tuple[int, int, int]:
    """Blend colour a into colour b. t=0 gives a, t=1 gives b."""
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )


def make_gradient(
        size: tuple[int, int] | None = None, extra: bool = False) -> pygame.Surface:
    """Sunset gradient: dark purple at the top, pink at the bottom."""
    if not size:
        size = (WINDOW_SIZE[0], WINDOW_SIZE[1] + HEADER_HEIGHT * 2)
    surface = pygame.Surface(size)
    top = (25, 5, 60)
    bottom = (255, 90, 140)
    for y in range(size[1]):
        color = _lerp_color(top, bottom, y / size[1])
        pygame.draw.line(surface, color, (0, y), (size[0], y))
    if extra:
        logo_path = "src/assets/menu/FT_PacMan.png"
        logo = pygame.image.load(logo_path).convert_alpha()
        surface.blit(
            pygame.transform.scale(logo,
                                   (WINDOW_SIZE[0] * 0.4,
                                    WINDOW_SIZE[1] * 0.4)),
            (WINDOW_SIZE[0] * 0.3, WINDOW_SIZE[1] * 0.02)
            )
    return surface
