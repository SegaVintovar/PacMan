
from typing import Any
from maze_gen.mazegenerator import MazeGenerator
from .cell import Cell
from .assets.cells import *
import pygame

class Map:
    def __init__(self, config: dict[str, Any]) -> None:
        # error handling now or do try init Map
        self.pacgum: int = int(config["pacgum"])
        self.width: int = int(config["width"])
        self.height: int = int(config["height"])
        self.seed: int = int(config["seed"])

        self._grid: list[list[int]] = []
        self.map: list[list[Cell]] = self._create_map()
        self.map_image: pygame.Surface = self._build_image()

    def _create_map(self) -> list[list[Cell]]:
        maze_gen: MazeGenerator = MazeGenerator(
            size=(self.width, self.height),
            seed=self.seed
        )
        self._grid = maze_gen.maze
        iMap = []
        for y, row in enumerate(self._grid):
            tmp = []
            for x ,c in enumerate(row):
                tmp.append(Cell(
                bool(c & 1),            # North
                bool((c >> 1) & 1),     # East
                bool((c >> 2) & 1),     # South
                bool((c >> 3) & 1),     # West
                ((x * 32), (y * 32)),   # position
                c                       # value
                ))
            iMap.append(tmp)
        return iMap

    def _build_image(self) -> pygame.Surface:
        tiles = []
        for i in range(16):
            try:
                image = pygame.image.load(f"src/assets/cells/tile_{i}.png").convert()
            except Exception as e:
                raise e
            tiles.append(image)
        screen = pygame.Surface(size=((self.width * 32), (self.height * 32)))
        for row in self.map:
            for c in row:
                screen.blit(tiles[c.value], c.position)
        return screen