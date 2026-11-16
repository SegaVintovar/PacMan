
from .cell import Cell
from .creature import Creature
from .constants import GHOST_DIRECTIONS
from .map import Map


class Behaviour:
    @staticmethod
    def chase(grid: list[list[Cell]],
              pacman: Creature, ghost: Creature) -> str:
        ...

    @staticmethod
    def block(grid: list[list[Cell]],
              pacman: Creature, ghost: Creature) -> str:
        ...

    @staticmethod
    def rand(grid: list[list[Cell]],
             pacman: Creature, ghost: Creature) -> str:
        ...

    def coward_flee(grid: list[list[Cell]],
                    pacman: Creature, ghost: Creature) -> str:
        ...

    def _assemble_path() -> list[Cell]:
        ...

    @staticmethod
    # each step is added by 1 when one of the remaining distances gets cut
    # rather an increase in x or y would cause an extra increase of steps.
    def a_star(map: Map,
               dest: tuple[int, int],
               at: tuple[int, int]) -> None:
        routes: list[str] = ["up", "right", "down", "left"]
        steps: int = 0
        # cellCost: list[tuple[int, int]] = []
        while steps < 3:
            costs: list[int] = []
            for route in routes:
                opt: tuple[int, int] = GHOST_DIRECTIONS[route]
                destx, desty = dest
                atx, aty = at
                optx, opty = opt
                if map.off_grid(atx + optx, aty + opty):
                    continue
                if map.is_walled(atx, aty, route):
                    continue
                h: int = abs(atx - destx) + abs(aty - desty)
                c: int = h + steps
                costs.append(c)
                if atx == destx and aty == desty:
                    break
            print(f"\tthe cheapest: {costs}")
            steps += 1
