
from .cell import Cell
from .config import GameConfig
from .assets.cells import *
from . import MazeGenerator
import pygame

TILE = 64


class Map:
    def __init__(self, config: GameConfig) -> None:
        # error handling now or do try init Map
        self.config = config
        self.pacgum: int = int(self.config.pacgum)
        self.width: int = int(self.config.width)
        self.height: int = int(self.config.height)
        self.seed: int = int(self.config.seed)

        self._grid: list[list[int]] = []
        self.map: list[list[Cell]] = self._create_map()
        self.map_image: pygame.Surface = self._build_rect_image()
        self.tiles: list[pygame.Surface] = []

    def _create_map(self) -> list[list[Cell]]:
        maze_gen: MazeGenerator = MazeGenerator(
            size=(self.width, self.height),
            seed=self.seed
        )
        self._grid = maze_gen.maze
        iMap = []
        for y, row in enumerate(self._grid):
            tmp = []
            for x, c in enumerate(row):
                tmp.append(Cell(
                 bool(c & 1),            	 # North
                 bool((c >> 1) & 1),      	 # East
                 bool((c >> 2) & 1),     	 # South
                 bool((c >> 3) & 1),     	 # West
                 ((x * TILE), (y * TILE)),   # position
                 c                       	 # value
                ))
            iMap.append(tmp)
        return iMap

    def _build_rect_image(self) -> pygame.Surface:
        screen = pygame.Surface(size=(
            (self.width * TILE), (self.height * TILE)))
        for row in self.map:
            for c in row:
                screen.blit(c.surface, dest=c.position)
        return screen

    # can be used to build an image with .png pictures
    def _build_image(self) -> pygame.Surface:
        tiles = []
        for i in range(16):
            try:
                image = pygame.image.load(
                    f"src/assets/cells/tile_{i}.png").convert()
            except Exception as e:
                raise e
            tiles.append(image)
        screen = pygame.Surface(size=(
            (self.width * TILE), (self.height * TILE)))
        for row in self.map:
            for c in row:
                screen.blit(tiles[c.value], c.position)
        return screen

    def get_cel_by_coords(self, x: int, y: int) -> Cell | None:
        return self.map[y][x] or None
