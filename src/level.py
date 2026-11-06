from .gum import Gum
from .map import Map
import pygame
from .timer import Timer
from .config import GameConfig
from .creature import Creature
from .pacman import Pacman
from .constants import GHOSTS
from typing import Any
from .game_state import GameState


# we need some class for state returns
class Level():
    def __init__(self,
                 id: int,
                 name: str,
                 seed: int,
                 config: GameConfig
                 ) -> None:
        self.id = id
        self.config = config
        self.name = name
        self.seed = seed
        self.map: Map = Map(self.config, self.seed)
        self.creatures: list[Creature] = []
        self.gums: list[Gum] = []
        timer = Timer(config.level_max_time)
        self.timer: Timer = timer
        self.pacman: Pacman = Pacman(self.map, self.config)
        self.creatures: Creature = []

    def _prepare_level(self) -> None:
        # spawn creatures
        self.creatures.append(self.pacman)
        ...

    def process(self,
                events: list[pygame.event.Event],
                game_state: GameState,
                ) -> None:
        ...

    def _gen_gums(self) -> None:
        # place super gums in corner cells
        # then fulfill rest of the 
        amount = self.config.pacgum
        corner_cells = (
            self.map[0][0],
            self.map[0][self.config.height - 1],
            self.map[self.config.width - 1][0],
            self.map[self.config.width - 1][self.config.height - 1]
        )
        for row in self.maps[0].map:
            for c in row:
                if c.value not in (15, 1):
                    px, py = c.position
                    self.gums.append(
                            Gum(
                                (px, py),
                                t="super" if c in corner_cells else ""
                            )
                    )
                    amount -= 1

    def show_gums(self, screen: pygame.Surface) -> None:
        for g in self.gums:
            if self.pacman.rect.center == g.rect.center:
                self.header.score += (self.config.points_per_pacgum
                                      if not g.type else
                                      self.config.points_per_super_pacgum)
                self.gums.remove(g)
            else:
                screen.blit(g.image, dest=g.rect)

    def render_creatures(self, map: pygame.Surface) -> None:
        self.pacman.check()
        for creature in self.creatures:
            creature.spawn(map)
        # self.pacman.spawn(map)

    def _awake_ghosts(self) -> None:
        for name in GHOSTS:
            d: dict[str, Any] = GHOSTS[name]
