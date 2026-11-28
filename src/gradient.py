import pygame
from .constants import WINDOW_SIZE, HEADER_HEIGHT
from .paths import ASSETS_DIR


def _lerp_color(a: tuple[int, int, int], b: tuple[int, int, int],
                t: float) -> tuple[int, int, int]:
    """Blend colour a into colour b. t=0 gives a, t=1 gives b."""
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )


def _add_palms(surface: pygame.Surface, size: tuple[int, int]) -> None:
    palms = []
    palm_left = (ASSETS_DIR / "palms" / "palm1.png",
                 (-30, size[1] * 0.3))
    palm_mid = (ASSETS_DIR / "palms" / "palm2.png",
                (size[0] * 0.65, size[1] * 0.35))
    palm_right = (ASSETS_DIR / "palms" / "palm3.png",
                  (size[0] * 0.65, size[1] * 0.35))
    palms = [palm_left, palm_mid, palm_right]
    # try:
    for p in palms:
        surface.blit(pygame.image.load(p[0]),
                     dest=(p[1]))


def make_gradient(
        size: tuple[int, int], extra: bool = False, palms: bool = False
        ) -> pygame.Surface:
    """Sunset gradient: dark purple at the top, pink at the bottom."""
    surface = pygame.Surface(size)
    top = (25, 5, 60)
    bottom = (255, 90, 140)
    for y in range(size[1]):
        color = _lerp_color(top, bottom, y / size[1])
        pygame.draw.line(surface, color, (0, y), (size[0], y))
    if extra:
        logo_path = ASSETS_DIR / "menu" / "FT_PacMan.png"
        try:
            logo = pygame.image.load(logo_path).convert_alpha()
        except (FileNotFoundError, PermissionError) as e:
            raise e
        surface.blit(
            pygame.transform.scale(
                logo,
                (size[0] * 0.4, size[1] * 0.4)
                ),
            (size[0] * 0.3, size[1] * 0.02)
        )
    if palms:
        _add_palms(surface, size)
    return surface
