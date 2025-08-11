from app.core.vectors_v2 import CustomVec2


def test():
    a = CustomVec2[int](1, 2)

    b = CustomVec2[float](3, 4) + a

    print(a, b)