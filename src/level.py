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
        self.pussy_time: int = 8
        pussy_timer: Timer = Timer(self.pussy_time)
        self.pussy_timer: Timer = pussy_timer
        self.map: Map = Map(self.config, self.seed)
        self.creatures: list[Ghost] = []
        self.gums: list[Gum] = []
        self._gen_gums()
        timer = Timer(config.level_max_time)
        self.timer: Timer = timer
        self._awake_ghosts()
        self.pathfinder: Pathfinder = Pathfinder(self.map)

    def isDone(self, pacman: Pacman) -> bool:
        if not self.gums:
            return True
        return False

    def process(self, screen: pygame.Surface, pacman: Pacman) -> bool:
        if self.isDone(pacman):
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
                    for ghost in self.creatures:
                        ghost.fear_paccie()
                    self.pussy_timer.start_timer()
                self.gums.remove(g)
            else:
                screen.blit(g.image, dest=g.rect)
        for g in to_remove:
            self.gums.remove(g)

    def _render_creatures(self,
                          screen: pygame.Surface,
                          pacman: Pacman
                          ) -> None:
        for ghost in self.creatures:
            # ghost is scared or it is chasing
            if ghost._at_destination():
                if not ghost.eaten:
                    self.pathfinder.build_path(ghost, pacman)
                else:
                    self.pathfinder.build_path(ghost, pacman, True)
                ...
            # make ghost follow the path
            if ghost.check(pacman, _finder=self.pathfinder):
                ghost.disrespect_paccie()
                self._reset_ghosts()
            ghost.spawn(screen)
            if (self.pussy_timer.time_since_start() == self.pussy_time
               and ghost.being_coward):
                ghost.disrespect_paccie()
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

    def _reset_ghosts(self) -> None:
        for g in self.creatures:
            g.disrespect_paccie()
            g.measure_spawn()
            self.path = []
            g._destination = g._cell_center(None)
