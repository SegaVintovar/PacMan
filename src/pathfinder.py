# from .pacman import Pacman
# from .ghost import Ghost
from .creature import Creature
from .map import Map
from .cell import Cell
from collections import deque
from .constants import TILE


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

    def build_path(self, ghost: Creature,
                   pacman: Creature, retreat: bool = False) -> None:
        def get_neighbours(
                cell: Cell, map: list[list[Cell]]
                ) -> list[tuple[tuple[int, int], Cell]]:

            def wall_opened(direction: tuple[int, int], cell: Cell) -> bool:
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
                    (pos[0] + d[0] >= len(map[0])) or \
                        (pos[1] + d[1] >= len(map)):
                    continue
                #
                if wall_opened(d, cell):
                    new_pos = (pos[0] + d[0],
                               pos[1] + d[1])
                    result.append((d, map[new_pos[1]][new_pos[0]]))
            return result

        # now we need to start getting neighbours in general dir
        if retreat:
            start_x, start_y = ghost.start
            start_cell = self.map.get_cel_by_coords(ghost.cell_x, ghost.cell_y)
            target_cell = self.map.get_cel_by_coords(start_x, start_y)
        else:
            for row in self.map.map:
                for c in row:
                    if ghost.rect.colliderect(c.rect):
                        start_cell = c
                    if pacman.rect.colliderect(c.rect):
                        target_cell = c
        queue = deque([start_cell])
        came_from = {start_cell: None}
        visited = set()
        if ghost.name == "Pinky" or ghost.name == "Blinky" or retreat:
            while queue and target_cell not in came_from:  # without " and target_cell not in came_from" it gives different behavior
                current_c = queue.popleft()
                if current_c not in visited:
                    visited.add(current_c)
                    neighbours = get_neighbours(current_c, self.map.map)
                    for n in neighbours:
                        if n[1] not in visited:
                            came_from[n[1]] = current_c
                            if n[1] == target_cell:
                                break
                            queue.append(n[1])
        else:
            while queue:  # without " and target_cell not in came_from" it gives different behavior
                current_c = queue.popleft()
                if current_c not in visited:
                    visited.add(current_c)
                    neighbours = get_neighbours(current_c, self.map.map)
                    for n in neighbours:
                        if n[1] not in visited:
                            came_from[n[1]] = current_c
                            if n[1] == target_cell:
                                break
                            queue.append(n[1])
        if target_cell not in came_from:
            ghost.path = []
            return
        path = []
        step: Cell | None = target_cell
        while step is not None:
            path.append(step)
            step = came_from[step]
        path.reverse()
        ghost.path = path[1:]

    def run_away(self, ghost: Creature, pacman: Creature) -> None:
        opposite_dir = {
            (1, 0): (-1, 0),
            (0, 1): (0, -1),
            (-1, 0): (1, 0),
            (0, -1): (0, 1)
        }
        # 1. in with dir pacman is
        # 2. choose opposite direction
