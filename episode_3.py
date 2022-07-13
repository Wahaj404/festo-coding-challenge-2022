from itertools import chain
from copy import deepcopy


class Person:
    def __init__(self, lines: list[str]):
        self.name = lines[0].split(":")[1].strip()
        self.id = lines[1].split(":")[1].strip()
        self.home_planet = lines[2].split(":")[1].strip()
        self.blood = [list(line.strip()[1:-1]) for line in lines[5:11]]

    def _bendy_path(self, s: str, i: int, j: int) -> list[set[tuple[int, int]]]:
        path = []

        def helper(s: str, i: int, j: int):
            if s == "":
                yield set(path)
            elif (
                0 <= i < len(self.blood)
                and 0 <= j < len(self.blood[i])
                and self.blood[i][j] == s[0]
            ):
                s = s[1:]
                path.append((i, j))
                for x, y in ((i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)):
                    yield from helper(s, x, y)
                path.pop()

        return list(helper(s, i, j))

    def has_pico(self, seqs: list[str]) -> bool:
        paths = {
            seq: [
                path
                for i in range(len(self.blood))
                for j in range(len(self.blood[i]))
                for path in self._bendy_path(seq, i, j)
            ]
            for seq in seqs
        }

        def non_intersecting(running_set: set[tuple[int, int]], i: int = 0) -> bool:
            if i == len(seqs):
                return True
            for path in paths[seqs[i]]:
                if len(running_set & path) == 0:
                    running_set |= path
                    if non_intersecting(running_set, i + 1):
                        return True
                    running_set -= path
            return False

        return non_intersecting(set())


def read_persons(fname: str) -> list[Person]:
    with open(fname, "r") as f:
        lines = f.readlines()
    return [Person(lines[i : i + 14]) for i in range(0, len(lines), 14)]


def puzzle1(persons: list[Person]) -> set[str]:
    seqs = ["pic", "opi", "cop", "ico"]
    return sorted({p.id for p in persons if p.has_pico(seqs)})


if __name__ == "__main__":
    persons = read_persons("population.txt")
    p1 = puzzle1(persons)
    print(f"p1: {sum(map(int, p1))}")
