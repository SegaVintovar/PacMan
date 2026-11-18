from .gum import Gum
from .map import Map
import pygame
from .timer import Timer
from .config import GameConfig
from .pacman import Pacman
from .constants import GHOSTS
from .ghost import Ghost
import random
from .pathfinder import Pathfinder


class Level():
    def __init__(self,
                 id: int,
                 name: str,
                 seed: int,
                 config: GameConfig,
                 ) -> None:
        self.id = id
        self.config = config
        self.name = name
        self.seed = seed
        self.map: Map = Map(self.config, self.seed)
        self.creatures: list[Ghost] = []
        self.gums: list[Gum] = []
        self._gen_gums()
        timer = Timer(config.level_max_time)
        self.timer: Timer = timer
        self._awake_ghosts()
        self.pathfinder: Pathfinder = Pathfinder(self.map)

    def isDone(self) -> bool:
        if not self.gums:
            return True
        return False

    def process(self, screen: pygame.Surface, pacman: Pacman) -> bool:
        if self.isDone():
            return True
        self.show_gums(screen, pacman)
        self._render_creatures(screen, pacman)
        screen.blit(pacman.sprite, pacman.rect)
        return False

    def _gen_gums(self) -> None:
        # first place super gums in corner cells
        # then fulfill rest of the grid
        amount = self.config.pacgum
        corner_cells = (
            self.map.map[0][0],
            self.map.map[self.config.height - 1][0],
            self.map.map[0][self.config.width - 1],
            self.map.map[self.config.height - 1][self.config.width - 1]
        )
        for c in corner_cells:
            px, py = c.position
            self.gums.append(
                Gum(
                    (px, py),
                    "super"
                )
            )
            amount -= 1

        free_cells = []
        for row in self.map.map:
            for cell in row:
                if cell.value != 15 and cell not in corner_cells:
                    free_cells.append(cell)
        # we do not place more then we can
        amount = min(amount, len(free_cells))
        # random gen, thanks to Claude
        rng = random.Random(self.seed)
        for cell in rng.sample(free_cells, amount):
            self.gums.append(Gum(cell.position, ""))

    def show_gums(self, screen: pygame.Surface, pacman: Pacman) -> None:
        to_remove = []
        for g in self.gums:
            if pacman.rect.center == g.rect.center:
                pacman.points += (
                    self.config.points_per_pacgum
                    if not g.type else
                    self.config.points_per_super_pacgum
                    )
                if g.type == "super":
                    print("run you b*tches")
                    for ghost in self.creatures:
                        ghost.pussy_mod = True
                to_remove.append(g)
            else:
                screen.blit(g.image, dest=g.rect)
        for g in to_remove:
            self.gums.remove(g)

    def _render_creatures(self,
                          screen: pygame.Surface,
                          pacman: Pacman
                          ) -> None:
        for ghost in self.creatures:
            if ghost._at_destination():
                # regen the path
                self.pathfinder.build_path(ghost, pacman)
                ...
            # make ghost follow the path
            ghost.check(pacman)
            ghost.spawn(screen)
        pacman.check()
        pacman.spawn(screen)

    def _awake_ghosts(self) -> None:
        for name in GHOSTS:
            ghost = Ghost(
                name=name,
                map=self.map,
                config=self.config
            )
            self.creatures.append(ghost)
