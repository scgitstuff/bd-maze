class Point:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"(x:{self.x}, y:{self.y})"

    def asTuple(self) -> tuple[int, int]:
        return (self.x, self.y)


def main():
    p = Point(45, 60)
    print()
    print(p)
    print(p.asTuple())


if __name__ == "__main__":
    main()
