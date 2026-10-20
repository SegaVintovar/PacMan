from maze_gen.mazegenerator import MazeGenerator


class Cell():
    """Represents a single cell in the maze grid.

    Each cell has four walls (north, east, south, west) that can be either
    closed (True) or open (False), a position in the grid, and several state
    flags used during generation and pathfinding. Cells can also carry
    special markers like ' S' for start, ' E' for exit, or '42' for the
    decorative pattern.

    Attributes:
        n: Boolean state of the north wall. True means wall is closed.
        e: Boolean state of the east wall. True means wall is closed.
        s: Boolean state of the south wall. True means wall is closed.
        w: Boolean state of the west wall. True means wall is closed.
        position: Tuple (x, y) with the cell's coordinates in the grid.
        special: String marker shown in the cell's center during rendering.
        visited: True if generation algorithm has processed this cell.
        path: True if this cell is part of the shortest path.
        seed: Reserved flag for seed-related marking (currently unused).
    """
    def __init__(
            self,
            n: bool, e: bool, s: bool, w: bool, position: tuple[int, int],
            special: str = "", visited: bool | None = None
            ) -> None:
        """Initialize a cell with walls, position, and state.

        Args:
            n: Initial state of the north wall (True = closed).
            e: Initial state of the east wall (True = closed).
            s: Initial state of the south wall (True = closed).
            w: Initial state of the west wall (True = closed).
            position: Tuple of (x, y) coordinates for this cell.
            special: String marker to display in the cell's center.
            visited: Initial visited state for the generation algorithm.
        """
        self.n = n
        self.e = e
        self.s = s
        self.w = w
        self.special = special
        self.seed: bool = False
        self.position = position
        self.visited = visited
        self.path: bool = False
        self.parent: Cell | None = None
        self.dead: bool = False

    def wall(
            self,
            wall: bool,
            # side: str,
            is_path: bool = False,
            is_42: bool = False
            ) -> str:
        """
        Return the colored 2-char string for one wall or corridor segment.

        Yellow square when is_42, black '██' when the wall is closed, blue
        square when the cell is on the path and the wall is open, white
        corridor '  ' otherwise.
        """

        blue_square = "\033[34m██\033[0m"
        white_corridor = "\033[47m  \033[0m"
        yellow_square = "\033[33m██\033[0m"
        black_corridor = "  "
        if is_42:
            return yellow_square

        if not wall:
            if is_path:
                return blue_square
            if is_42:
                return yellow_square
            return black_corridor
        return "██"

    def representation(
            self, show_path: bool = False, neigh_path: dict | None = None,
            neigh_42: dict | None = None) -> list:
        """Return the 3x3 string matrix representing the cell for printing.

        The cell is rendered as a 3-row by 3-column grid of strings. Corners
        are always walls ('██'), edges show walls or open gaps based on the
        cell's wall state, and the center shows the special marker, the path
        indicator '··', or empty space depending on state.

        Returns:
            A list of 3 lists, each containing 3 strings. The outer list
            represents rows (top, middle, bottom), the inner lists represent
            columns (left, center, right) within each row.
        """
        if neigh_path is None:
            neigh_path = {"N": False, "E": False, "S": False, "W": False}

        if neigh_42 is None:
            neigh_42 = {"N": False, "E": False, "S": False, "W": False}

        blue_square = "\033[34m██\033[0m"
        white_corridor = "\033[47m  \033[0m"

        if "S" in self.special:
            center = "\033[92;47m██\033[0m"
        elif "E" in self.special:
            center = "\033[91;47m██\033[0m"
        elif show_path and self.path and "\033[" not in self.special:
            center = blue_square
        elif self.special == "  " or self.special == " P":
            center = white_corridor
        else:
            center = self.special
        center = "  "
        w_char = "██"

        return [
            [
                w_char,
                self.wall(self.n),
                w_char
            ],
            [
                self.wall(self.w),
                center,
                self.wall(self.e)
            ],
            [
                w_char,
                self.wall(self.s),
                w_char
            ]
        ]

    def open_wall(self, wall: str | None) -> None:
        """
        Set a specific wall to the open state.
        """
        if wall == "N":
            self.n = False
        if wall == "E":
            self.e = False
        if wall == "S":
            self.s = False
        if wall == "W":
            self.w = False

    def count_open_walls(self) -> int:
        i = 0
        if self.n is False:
            i += 1
        if self.e is False:
            i += 1
        if self.s is False:
            i += 1
        if self.w is False:
            i += 1
        return i


class Map():
    def __init__(self, input: list[list[int]]) -> None:
        self.input = input
        self.grid: list[list[Cell]]
        self.create_map(self.input)

    def create_map(input: list[list[int]]) -> None:
        ...

def test():
    maze = MazeGenerator(exit_cell=(14, 14), seed=1)
    for row in maze.maze:
        print([bin(cell) for cell in row])
    for row in maze.maze:
        print(row)
    my_maze: list[list[Cell]] = []
    y = 0

    for row in maze.maze:
        line = []
        x = 0
        for c in row:
            line.append(Cell(
                bool(c & 1),            # North
                bool((c >> 1) & 1),     # East
                bool((c >> 2) & 1),     # South
                bool((c >> 3) & 1),     # West
                (x, y)                  # position
                ))
            x += 1
        my_maze.append(line)
        y += 1

    color: str = "\033[0m"

    for y, row in enumerate(my_maze):
        i = 0
        while i < 3:

            for x, cell in enumerate(row):

                rep = cell.representation()

                k = 0
                while k < 3:
                    part = rep[i][k]
                    print(part, end="")
                    # paint only black walls dont touch color blocks
                    # if part == "██" and "\033[" not in part:
                    #     print(color + part + "\033[0m", end="")
                    # else:
                    #     print(part, end="")
                    k += 1
            print()
            i += 1


if __name__ == "__main__":
    test()

# West, South, East, North

# 0 = 0000
# 1 = 0001
# • 2 = 0010
# • 3 = 0011
# • 4 = 0100
# • 5 = 0101
# • 6 = 0110
# • 7 = 0111
# • 8 = 1000
# • 9 = 1001
# • 10 = 1010
# • 11 = 1011
# • 12 = 1100
# • 13 = 1101
# • 14 = 1110
# • 15 = 1111
# 13 / 2 = 6 1/2 (1)
# 6 / 2 = 3  0/2 (0)
# 3 / 2 = 1  1/2 (1)
# 1 / 2 = 0  1/2 (1)

# n = 13

# north = n & 1          # LSB
# east = (n >> 1) & 1
# south = (n >> 2) & 1
# west = (n >> 3) & 1   # MSB
# print("north", north, "east", east, "south", south, "west", west)

# W N W W W W W W W
# W C E W C E
# W S W