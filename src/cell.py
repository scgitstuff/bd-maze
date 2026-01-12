from point import Point
from line import Line
from walls import Walls
from window import Window
from typing import Self


class Cell:
    def __init__(
        self,
        win: Window,
        topLeft: Point,
        bottomRight: Point,
        walls: Walls | None = None,
        visited: bool = False,
    ):
        self.win = win

        self.topLeft = topLeft
        self.topRight = Point(bottomRight.x, topLeft.y)
        self.bottomRight = bottomRight
        self.bottomLeft = Point(topLeft.x, bottomRight.y)

        self.center = Point(
            topLeft.x + (bottomRight.x - topLeft.x) // 2,
            topLeft.y + (bottomRight.y - topLeft.y) // 2,
        )

        if walls is None:
            walls = Walls()
        self.walls = walls

        self.visited = visited

    def __str__(self) -> str:
        return (
            f"window: {self.win.root.title}\n"
            f"center: {self.center}\n"
            f"topLeft: {self.topLeft}\n"
            f"topRight: {self.topRight}\n"
            f"bottomRight: {self.bottomRight}\n"
            f"bottomLeft: {self.bottomLeft}\n"
            f"walls: {self.walls}\n"
            f"visited: {self.visited}\n"
        )

    def __repr__(self):
        return f"Cell({self.topLeft}, {self.bottomRight})"

    # Turns out I didn't read the spec carefully, draw was supposed to take points as args
    # this makes no sense, because cells never move, always drawn in the same place
    # the points are set at construction, I'm not changing it
    def draw(self, fillColor: str = "black"):
        self._resetWalls()

        if self.walls.top:
            self.win.drawLine(Line(self.topLeft, self.topRight), fillColor)
        if self.walls.right:
            self.win.drawLine(Line(self.topRight, self.bottomRight), fillColor)
        if self.walls.bottom:
            self.win.drawLine(Line(self.bottomLeft, self.bottomRight), fillColor)
        if self.walls.left:
            self.win.drawLine(Line(self.topLeft, self.bottomLeft), fillColor)

    # lines do not disappear when breaking walls, reset them
    # I do hate this hack, it is what the lesson recommended
    def _resetWalls(self):
        self.win.drawLine(Line(self.topLeft, self.topRight), "white")
        self.win.drawLine(Line(self.topRight, self.bottomRight), "white")
        self.win.drawLine(Line(self.bottomLeft, self.bottomRight), "white")
        self.win.drawLine(Line(self.topLeft, self.bottomLeft), "white")

    def drawMove(self, destination: Self, undo=False):
        color = "gray" if undo else "red"
        line = Line(self.center, destination.center)
        line.draw(self.win.canvas, color)


def main():
    win = Window(500, 500)
    win.root.title("Cell test")
    cell1 = Cell(win, Point(100, 100), Point(200, 200))
    cell2 = Cell(win, Point(300, 300), Point(400, 400))

    cell1.draw()
    cell2.draw("green")
    cell1.drawMove(cell2)

    print()
    print(cell1)
    print(cell2)

    win.wait()


if __name__ == "__main__":
    main()
