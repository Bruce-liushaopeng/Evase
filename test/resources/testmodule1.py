import testmodule2 as tm2


class Test:
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def perform_comp(self, x: int, y: int) -> int:
        return tm2.add(x, y) + tm2.sub(x, y)


def main():
    t1 = Test("name1")
    print(t1.get_name())
    print(t1.perform_comp(1, 2))


if __name__ == '__main__':
    main()
