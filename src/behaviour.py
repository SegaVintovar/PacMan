
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
    # firstly you pick the lowest total cost followed by the lowest heuristic
    def a_star(map,
               dest: tuple[int, int],
               at: tuple[int, int]) -> list[tuple[int, int]]:
        routes: list[str] = ["up", "right", "down", "left"]
        current: tuple[int, int] = at
        popped: list[tuple[tuple[int, int], int, int]] = []
        destx, desty = dest
        costs: list[tuple[tuple[int, int], int, int]] = []
        # NEW: g of every cell seen so far, and who each cell came from
        g_score: dict[tuple[int, int], int] = {at: 0}
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        # NEW: the start counts as visited
        popped.append((at, 0, abs(at[0] - destx) + abs(at[1] - desty)))
        while True:
            x, y = current
            print(f"current position: x: {x}, y: {y}")
            if x == destx and y == desty:
                print("good boy, you are A* <3")
                # NEW: walk came_from backwards, then flip it
                path: list[tuple[int, int]] = [current]
                while path[-1] in came_from:
                    path.append(came_from[path[-1]])
                path.reverse()
                return path
            for route in routes:
                opt: tuple[int, int] = GHOST_DIRECTIONS[route]
                atx, aty = current
                optx, opty = opt
                if map.off_grid(atx + optx, aty + opty):
                    continue
                if map.is_walled(atx, aty, route):
                    continue
                new: tuple[int, int] = (atx + optx, aty + opty)
                if new in [p[0] for p in popped]:
                    continue
                newx, newy = new
                _heuristic: int = abs(newx - destx) + abs(newy - desty)
                # CHANGED: steps of the cell we came from, plus one
                _steps: int = g_score[current] + 1
                # NEW: already known with an equal or cheaper route
                if new in g_score and g_score[new] <= _steps:
                    continue
                # NEW: remember the better route, drop the older entry
                g_score[new] = _steps
                came_from[new] = current
                costs = [c for c in costs if c[0] != new]
                costs.append((new, _steps, _heuristic))
            # NEW: nothing left to explore means there is no path
            if not costs:
                print("no path")
                return []
            lowest = min(costs, key=lambda c: (c[1] + c[2], c[2]))
            current = lowest[0]
            costs.remove(lowest)
            print(lowest)
            popped.append((lowest[0], lowest[1], lowest[2]))
