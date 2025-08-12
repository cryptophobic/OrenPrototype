from app.core.vectors import CustomVec2f, CustomVec2i


def test():
    a = CustomVec2f(1.0, 0.0)
    b = CustomVec2i(3, 4)

    i: list[int] = [b.x, b.y]
    f: float = b.y

    print(a.normalized())