# from .pacman import Pacman
# from .ghost import Ghost
from .creature import Creature
from .map import Map
from .cell import Cell
from collections import deque


# from claude
class Pathfinder:
    """Finds the shortest path between two cells using BFS."""

    def __init__(self, map: Map) -> None:
        self.map: Map = map

    def _open_neighbours(self, x: int, y: int) -> list[tuple[int, int]]:
        """Return grid positions reachable from (x, y) in one step."""
        cell = self.map.get_cel_by_coords(x, y)
        # In Cell, True means "wall", so a side is open when it is False
        sides = [
            (not cell.n, (0, -1)),
            (not cell.e, (1, 0)),
            (not cell.s, (0, 1)),
            (not cell.w, (-1, 0)),
        ]
        result: list[tuple[int, int]] = []
        for is_open, (dx, dy) in sides:
            nx, ny = x + dx, y + dy
            if is_open and not self.map.off_grid(nx, ny):
                result.append((nx, ny))
        return result

    def build_path(self, ghost: Creature, pacman: Creature) -> None:
        """Store in ghost.path the cells to walk, next cell first."""
        start = (ghost.cell_x, ghost.cell_y)
        target = (pacman.cell_x, pacman.cell_y)

        # came_from doubles as the "visited" set
        came_from: dict[tuple[int, int], tuple[int, int] | None] = {
            start: None}
        queue: deque[tuple[int, int]] = deque([start])
        while queue and target not in came_from:
            current = queue.popleft()
            for nxt in self._open_neighbours(*current):
                if nxt not in came_from:
                    came_from[nxt] = current
                    queue.append(nxt)

        if target not in came_from:
            ghost.path = []  # unreachable: stand still
            return

        # walk back from target to start, then reverse
        positions: list[tuple[int, int]] = []
        step: tuple[int, int] | None = target
        while step is not None:
            positions.append(step)
            step = came_from[step]
        positions.reverse()

        # drop positions[0] (the ghost's own cell), convert to Cells
        cells: list[Cell] = []
        for x, y in positions[1:]:
            cells.append(self.map.get_cel_by_coords(x, y))
        ghost.path = cells



# my pathfinder - i am tired and it is not there
# class Pathfinder():
#     def __init__(self, map: Map) -> None:
#         self.map: Map = map

#     def build_path(self, ghost: Creature, pacman: Creature) -> None:
#         def get_neighbours(
#                 cell: Cell, map: list[list[Cell]]
#                 ) -> list[tuple[tuple[int, int], Cell]]:

#             def wall_opened(direction: tuple[int, int], cell: Cell) -> bool:
#                 if direction[0] and direction[0] > 0:
#                     return not cell.w
#                 if direction[0] and direction[0] < 0:
#                     return not cell.e
#                 if direction[1] and direction[1] > 0:
#                     return not cell.s
#                 if direction[1] and direction[1] < 0:
#                     return not cell.n
#                 return False

#             directions = [
#                 (1, 0), (0, 1), (-1, 0), (0, -1)
#             ]
#             pos = cell.position
#             result = []
#             for d in directions:
#                 # if not off grid
#                 if (pos[0] + d[0] < 0) or (pos[1] + d[1] < 0) or \
#                     (pos[0] + d[0] >= len(map[0])) or \
#                         (pos[1] + d[1] >= len(map)):
#                     continue
#                 #
#                 if wall_opened(d, cell):
#                     new_pos = (cell.position[0] + d[0],
#                                cell.position[1] + d[1])
#                     result.append((d, map[new_pos[1]][new_pos[0]]))
#             return result

#         # now we need to start getting neighbours in general dir
#         for row in self.map.map:
#             for c in row:
#                 # x = c.position[0]
#                 # y = c.position[1]
#                 if ghost.rect.colliderect(c.rect):
#                     start_cell = c
#                     print("found start cell")
#                 if pacman.rect.colliderect(c.rect):
#                     target_cell = c
#                     print("target cell: ", target_cell.position)
#         queue = deque([start_cell])
#         came_from = {}
#         visited = set()
#         while queue:
#             current_c = queue.popleft()
#             if current_c not in visited:
#                 visited.add(current_c)
#                 neighbours = get_neighbours(current_c, self.map.map)
#                 for n in neighbours:
#                     if n[1] not in visited:
#                         came_from[n[1]] = current_c
#                         if n[1] == target_cell:
#                             break
#                         queue.append(n[1])
#         path = [target_cell]
#         c = target_cell
#         while True:
#             print(c.grid_coord)
#             c = came_from[c]
#             path.append(c)
#             if c == start_cell:
#                 break

#         path.reverse()
#         ghost.path = path[1:]
