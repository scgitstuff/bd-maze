from window import Window
from line import Line
from point import Point
from cell import Cell
import random
import time

# just while building to see all the walls
GAP = 0


class Maze:
    def __init__(
        self,
        origin: Point,
        rows: int,
        cols: int,
        cellWidth: int,
        cellHeight: int,
        win: Window | None = None,
    ):
        self.origin = origin
        self.rows = rows
        self.cols = cols
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.win = win

        self.cells: list[list[Cell]] = []

    def __str__(self) -> str:
        return (
            f"window: {self.win.root.title if self.win else "None"}\n"
            f"origin: {self.origin}\n"
            f"rows: {self.rows}\n"
            f"cols: {self.cols}\n"
            f"cellWidth: {self.cellWidth}\n"
            f"cellHeight: {self.cellHeight}\n"
        )

    def solve(self):
        if self._solve(0, 0):
            self._fixLines()
        self._resetVisited()

    # hack to extend the line for start/end cells
    # the spec draws moves from the center of cell
    # otherwise cells would need to know direction
    def _fixLines(self):
        if self.win == None:
            return

        color = "red"
        start = self.cells[0][0]
        end = self.cells[self.rows - 1][self.cols - 1]

        line = Line(Point(start.topLeft.x, start.center.y), start.center)
        line.draw(self.win.canvas, color)

        line = Line(Point(end.bottomRight.x, end.center.y), end.center)
        line.draw(self.win.canvas, color)

    def _solve(self, r: int, c: int) -> bool:

        self._animate()
        self.cells[r][c].visited = True

        if r == self.rows - 1 and c == self.cols - 1:
            return True

        directions = self._getValidDirections(r, c)
        for direction in directions:
            s, dr, dc = direction
            if self._validateMove(self.cells[r][c], direction):
                self.cells[r][c].drawMove(self.cells[dr][dc])
                if self._solve(dr, dc):
                    return True
                self.cells[r][c].drawMove(self.cells[dr][dc], True)

        return False

    def _validateMove(self, cell: Cell, direction: tuple[str, int, int]) -> bool:
        s, r, c = direction

        match s:
            case "North":
                return (
                    cell.walls.top == False and self.cells[r][c].walls.bottom == False
                )
            case "South":
                return (
                    cell.walls.bottom == False and self.cells[r][c].walls.top == False
                )
            case "West":
                return (
                    cell.walls.left == False and self.cells[r][c].walls.right == False
                )
            case "East":
                return (
                    cell.walls.right == False and self.cells[r][c].walls.left == False
                )

        return False

    # spec has this private and called by constructor, I'm not doing that
    # I want it separate so I can recreate cells if dimensions change
    def createCells(self):
        if self.win == None:
            return

        self.cells: list[list[Cell]] = []

        for r in range(self.rows):
            y = self.origin.y + self.cellHeight * r
            self.cells.append([])

            for c in range(self.cols):
                x = self.origin.x + self.cellWidth * c
                start = Point(x + GAP, y + GAP)
                end = Point(self.cellWidth + x, self.cellHeight + y)
                self.cells[r].append(Cell(self.win, start, end))

                self._drawCell(r, c)

        self._openMaze()

    def _drawCell(self, row: int, col: int, fillColor: str = "black"):
        if not self.win:
            return
        self.cells[row][col].draw(fillColor)
        self._animate()

    def _animate(self):
        if not self.win:
            return
        self.win.redraw()
        time.sleep(0.05)

    def _openMaze(self):
        self.cells[0][0].walls.left = False
        self._drawCell(0, 0)

        self.cells[self.rows - 1][self.cols - 1].walls.right = False
        self._drawCell(self.rows - 1, self.cols - 1)

    def breakWalls(self):
        # random.seed(0)

        self._breakWalls(0, 0)
        self._resetVisited()

    def _breakWalls(self, r: int, c: int):
        self.cells[r][c].visited = True

        while True:
            directions = self._getValidDirections(r, c)
            if len(directions) < 1:
                self._drawCell(r, c)
                return

            index = random.randrange(len(directions))
            s, dr, dc = directions[index]
            self._breakWall(self.cells[r][c], directions[index])
            self._breakWalls(dr, dc)

    def _getValidDirections(self, r: int, c: int) -> list[tuple[str, int, int]]:
        directions = []

        if r - 1 >= 0 and not self.cells[r - 1][c].visited:
            directions.append(("North", r - 1, c))
        if r + 1 < self.rows and not self.cells[r + 1][c].visited:
            directions.append(("South", r + 1, c))
        if c - 1 >= 0 and not self.cells[r][c - 1].visited:
            directions.append(("West", r, c - 1))
        if c + 1 < self.cols and not self.cells[r][c + 1].visited:
            directions.append(("East", r, c + 1))

        return directions

    def _breakWall(self, cell: Cell, direction: tuple[str, int, int]):
        s, r, c = direction

        match s:
            case "North":
                cell.walls.top = False
                self.cells[r][c].walls.bottom = False
            case "South":
                cell.walls.bottom = False
                self.cells[r][c].walls.top = False
            case "West":
                cell.walls.left = False
                self.cells[r][c].walls.right = False
            case "East":
                cell.walls.right = False
                self.cells[r][c].walls.left = False

    def _resetVisited(self):
        for r in range(len(self.cells)):
            for c in range(len(self.cells[r])):
                self.cells[r][c].visited = False


def main():

    win = Window(500, 500)
    win.root.title("Maze test")

    maze = Maze(Point(100, 100), 5, 5, 60, 50, win)
    maze.createCells()
    maze.breakWalls()
    maze.solve()

    print()
    print(maze)
    print(maze.cells)

    win.wait()


if __name__ == "__main__":
    main()
