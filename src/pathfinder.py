from .creature import Creature
from .map import Map
from .cell import Cell
from collections import deque


# my pathfinder - i am tired and it is not there
class Pathfinder():
    def __init__(self, map: Map) -> None:
        self.map: Map = map

    def get_neighbours(self, cell: Cell
                       ) -> list[tuple[tuple[int, int], Cell]]:
        """Return the neighbours of a cell that we can walk to.

        Every item is ((dx, dy), neighbour_cell). A neighbour is reachable
        when it is inside the grid and there is no wall on that side
        (in Cell, True means "wall").
        """
        x, y = cell.grid_coord
        # (dx, dy, is there a wall on this side of the cell?)
        sides = [
            (1, 0, cell.e),
            (0, 1, cell.s),
            (-1, 0, cell.w),
            (0, -1, cell.n),
        ]
        result: list[tuple[tuple[int, int], Cell]] = []
        for dx, dy, has_wall in sides:
            nx, ny = x + dx, y + dy
            if has_wall or self.map.off_grid(nx, ny):
                continue
            result.append(((dx, dy), self.map.map[ny][nx]))
        return result

    def build_path(
            self, start_cell: Cell | None, target_cell: Cell | None
            ) -> list[Cell]:
        if not start_cell or not target_cell:
            return []
        queue = deque([start_cell])
        came_from: dict[Cell, Cell | None] = {start_cell: None}
        visited = set()
        while queue and target_cell not in came_from:
            current_c = queue.popleft()
            if current_c not in visited:
                visited.add(current_c)
                neighbours = self.get_neighbours(current_c)
                for n in neighbours:
                    if n[1] not in visited:
                        came_from[n[1]] = current_c
                        if n[1] == target_cell:
                            break
                        queue.append(n[1])

        if target_cell not in came_from:
            path: list[Cell] = []
            return path
        path = []
        step: Cell | None = target_cell
        while step is not None:
            path.append(step)
            step = came_from[step]
        path.reverse()
        return path[1:]

    def retreat(self, ghost: Creature) -> None:
        start_x, start_y = ghost.start
        start_cell = self.map.get_cel_by_coords(ghost.cell_x, ghost.cell_y)
        target_cell = self.map.get_cel_by_coords(start_x, start_y)
        ghost.path = self.build_path(start_cell, target_cell)

    # used to be build
    def follow_pacman(
            self,
            ghost: Creature, pacman: Creature
            ) -> None:
        # now we need to start getting neighbours in general dir
        start_cell: Cell | None = None
        target_cell: Cell | None = None
        for row in self.map.map:
            for c in row:
                if ghost.rect.collidepoint(c.rect.center):
                    start_cell = c
                if pacman.rect.collidepoint(c.rect.center):
                    target_cell = c
        ghost.path = self.build_path(start_cell, target_cell)

    def run_away(self, ghost: Creature, pacman: Creature) -> None:
        """Take one step to the open neighbour furthest from pacman."""
        here = self.map.get_cel_by_coords(ghost.cell_x, ghost.cell_y)
        options = self.get_neighbours(here)
        if not options:
            ghost.path = []
            return

        def distance_to_pacman(option: tuple[tuple[int, int], Cell]) -> int:
            """Manhattan distance between the option and pacman."""
            col, row = option[1].grid_coord
            return abs(col - pacman.cell_x) + abs(row - pacman.cell_y)

        best = max(options, key=distance_to_pacman)
        ghost.path = [best[1]]
