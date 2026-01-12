from tkinter import Tk, BOTH, Canvas, ttk
from line import Line


class Window:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.root = Tk()
        self.root.title("Maze")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        # self.root.resizable(True, True)

        self.canvas = Canvas(
            self.root,
            width=self.width,
            height=self.height,
            background="white",
        )
        self.canvas.pack()

        self.isRunning = False

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait(self):
        self.isRunning = True
        while self.isRunning:
            self.redraw()

    def close(self):
        self.isRunning = False

    def drawLine(self, line: Line, fillColor: str):
        line.draw(self.canvas, fillColor)


def main():
    win = Window(500, 500)
    print(win)
    win.wait()


if __name__ == "__main__":
    main()
