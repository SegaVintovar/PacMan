# from .pacman import Pacman
# from .ghost import Ghost
from .creature import Creature
from .map import Map
from .cell import Cell
from collections import deque
from .constants import TILE
from pydantic_extra_types.coordinate import Coordinate


# from claude
# class Pathfinder:
#     """Finds the shortest path between two cells using BFS."""

#     def __init__(self, map: Map) -> None:
#         self.map: Map = map

#     def _open_neighbours(self, x: int, y: int) -> list[tuple[int, int]]:
#         """Return grid positions reachable from (x, y) in one step."""
#         cell = self.map.get_cel_by_coords(x, y)
#         # In Cell, True means "wall", so a side is open when it is False
#         sides = [
#             (not cell.n, (0, -1)),
#             (not cell.e, (1, 0)),
#             (not cell.s, (0, 1)),
#             (not cell.w, (-1, 0)),
#         ]
#         result: list[tuple[int, int]] = []
#         for is_open, (dx, dy) in sides:
#             nx, ny = x + dx, y + dy
#             if is_open and not self.map.off_grid(nx, ny):
#                 result.append((nx, ny))
#         return result

#     def build_path(self, ghost: Creature, pacman: Creature) -> None:
#         """Store in ghost.path the cells to walk, next cell first."""
#         start = (ghost.cell_x, ghost.cell_y)
#         target = (pacman.cell_x, pacman.cell_y)

#         # came_from doubles as the "visited" set
#         came_from: dict[tuple[int, int], tuple[int, int] | None] = {
#             start: None}
#         queue: deque[tuple[int, int]] = deque([start])
#         while queue and target not in came_from:
#             current = queue.popleft()
#             for nxt in self._open_neighbours(*current):
#                 if nxt not in came_from:
#                     came_from[nxt] = current
#                     queue.append(nxt)

#         if target not in came_from:
#             ghost.path = []  # unreachable: stand still
#             return

#         # walk back from target to start, then reverse
#         positions: list[tuple[int, int]] = []
#         step: tuple[int, int] | None = target
#         while step is not None:
#             positions.append(step)
#             step = came_from[step]
#         positions.reverse()

#         # drop positions[0] (the ghost's own cell), convert to Cells
#         cells: list[Cell] = []
#         for x, y in positions[1:]:
#             cells.append(self.map.get_cel_by_coords(x, y))
#         ghost.path = cells


# my pathfinder - i am tired and it is not there
class Pathfinder():
    def __init__(self, map: Map) -> None:
        self.map: Map = map

    def get_neighbours(self, cell: Cell
                       ) -> list[tuple[tuple[int, int], Cell]]:
        """
        Returns a list of neighbours where we can go.
        """
        def wall_opened(direction: tuple[int, int], cell: Cell) -> bool:
            if self.map.off_grid(*direction):
                return False
            if direction[0] and direction[0] > 0:
                return not cell.e
            if direction[0] and direction[0] < 0:
                return not cell.w
            if direction[1] and direction[1] > 0:
                return not cell.s
            if direction[1] and direction[1] < 0:
                return not cell.n
            return False

        directions = [
            (1, 0), (0, 1), (-1, 0), (0, -1)
        ]
        pos = (cell.position[0] // TILE, cell.position[1] // TILE)
        result = []
        for d in directions:
            # if not off grid
            if (pos[0] + d[0] < 0) or (pos[1] + d[1] < 0) or \
                (pos[0] + d[0] >= len(self.map.map[0])) or \
                    (pos[1] + d[1] >= len(self.map.map)):
                continue
            #
            if wall_opened(d, cell):
                new_pos = (pos[0] + d[0],
                           pos[1] + d[1])
                result.append((d, self.map.map[new_pos[1]][new_pos[0]]))
        return result

    # def build_path(self, ghost: Creature,
    #                pacman: Creature, retreat: bool = False) -> None:
    #     def get_neighbours(
    #             cell: Cell, map: list[list[Cell]]
    #             ) -> list[tuple[tuple[int, int], Cell]]:

    def build_path(
            self, start_cell: Cell | None, target_cell: Cell | None
            ) -> list[Cell]:
        if not start_cell or not target_cell:
            return []
        queue = deque([start_cell])
        came_from = {start_cell: None}
        visited = set()
        while queue and target_cell not in came_from:  # without " and target_cell not in came_from" it gives different behavior
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
        
        # while queue:  # without " and target_cell not in came_from" it gives different behavior
        #     current_c = queue.popleft()
        #     if current_c not in visited:
        #         visited.add(current_c)
        #         neighbours = get_neighbours(current_c, self.map.map)
        #         for n in neighbours:
        #             if n[1] not in visited:
        #                 came_from[n[1]] = current_c
        #                 if n[1] == target_cell:
        #                     break
        #                 queue.append(n[1])
        if target_cell not in came_from:
            path = []
            return path
        path = []
        step: Cell | None = target_cell
        while step is not None:
            path.append(step)
            step = came_from[step]
        path.reverse()
        return path

    def retreat(self, ghost: Creature) -> None:
        start_x, start_y = ghost.start
        start_cell = self.map.get_cel_by_coords(ghost.cell_x, ghost.cell_y)
        target_cell = self.map.get_cel_by_coords(start_x, start_y)
        self.ghost.path = self.build_path(start_cell, target_cell)

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


    # def run_away(self, ghost: Creature, pacman: Creature) -> Cell:
    #     def one(v: int) -> int:
    #         if v == 0:
    #             return 0
    #         elif v > 0:
    #             return 1
    #         else:
    #             return -1
    #     opposite_dir = {
    #         (1, 0): (-1, 0),
    #         (0, 1): (0, -1),
    #         (-1, 0): (1, 0),
    #         (0, -1): (0, 1),
    #         (0, 0): (0, 0)
    #     }
    #     # 1. in with dir pacman is
    #     # 2. choose opposite direction
    #     # nb = self.get_neighbours(ghost_cell)

    #     ghost_cell: Coordinate = ghost.position
    #     pacman_cell: Coordinate = pacman.position 
    #     pac_coord = (pacman_cell[0]//TILE,
    #                  pacman_cell[1]//TILE)
    #     ghost_coord = (ghost_cell[0]//TILE,
    #                    ghost_cell[1]//TILE)
    #     d_x = one(pac_coord[0] - ghost_coord[0])
    #     d_y = one(pac_coord[1] - ghost_coord[1])
    #     if abs(d_x) == abs(d_y) and d_x != 0 and d_y != 0:
    #         d_x = 0
    #     pac_dir = (d_x, d_y)
    #     run_there = opposite_dir[pac_dir]
    #     res_c = (ghost_coord[0] + run_there[0],
    #              ghost_coord[1] + run_there[1])
    #     if not self.map.off_grid(*res_c):
    #         ghost.path = [self.map.map[res_c[1]][res_c[0]]]
    #         # return self.map.map[res_c[1]][res_c[0]]
    #     else:
    #         ghost.path = [ghost_cell]

    # from claude
    def run_away(self, ghost: Creature, pacman: Creature) -> None:
        """Set ghost.path to one step in the direction away from pacman."""
        def sign(v: int) -> int:
            """Return -1, 0 or 1 depending on the sign of v."""
            if v == 0:
                return 0
            return 1 if v > 0 else -1

        # creatures track their grid cell in cell_x / cell_y
        d_x = sign(pacman.cell_x - ghost.cell_x)
        d_y = sign(pacman.cell_y - ghost.cell_y)
        # diagonal: keep only one axis so we move in a single direction
        if d_x != 0 and d_y != 0:
            d_x = 0
        # go the opposite way from pacman
        target_x = ghost.cell_x - d_x
        target_y = ghost.cell_y - d_y
        if self.map.off_grid(target_x, target_y):
            ghost.path = []
            return
        ghost.path = [self.map.map[target_y][target_x]]
