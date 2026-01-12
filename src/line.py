from point import Point
from tkinter import Canvas


class Line:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b

    def draw(self, canvas: Canvas, fillColor: str = "black"):
        canvas.create_line(
            *self.a.asTuple(),
            *self.b.asTuple(),
            fill=fillColor,
            width=2,
        )

    def __str__(self) -> str:
        return f"a:{self.a} b:{self.b}"


def main():
    from window import Window

    win = Window(500, 500)
    win.root.title("Line test")
    line = Line(Point(100, 100), Point(300, 300))
    line.draw(win.canvas, "blue")
    line = Line(Point(200, 100), Point(100, 300))
    line.draw(win.canvas)

    print()
    print(line)

    win.wait()


if __name__ == "__main__":
    main()
