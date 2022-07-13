from collections import defaultdict
from queue import Queue


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


def read_galaxy(fname: str) -> dict[str, list[int]]:
    with open(fname, "r") as f:
        return {
            line[0].strip(): list(int(x) for x in line[1].strip()[1:-1].split(","))
            for line in map(lambda line: line.split(":"), f)
        }


def dist(c1: tuple[float, float, float], c2: tuple[float, float, float]) -> float:
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5


def puzzle1(persons: list[Person]) -> set[str]:
    seqs = ["pic", "opi", "cop", "ico"]
    return sorted({p.id for p in persons if p.has_pico(seqs)})


def puzzle2(persons: list[Person]) -> set[str]:
    signal_ranging = {"Venis": 2, "Cetung": 4, "Phoensa": 9}
    galaxy = read_galaxy("galaxy_map.txt")
    graph = defaultdict(list)
    for p1, c1 in galaxy.items():
        for p2, c2 in galaxy.items():
            if dist(c1, c2) < 50:
                graph[p1].append(p2)
    running_set = set(galaxy.keys())
    for planet, delay in signal_ranging.items():
        q = Queue()
        q.put(planet)
        distances = {}
        distances[planet] = 0
        while not q.empty():
            u = q.get()
            for v in graph[u]:
                if v not in distances:
                    distances[v] = distances[u] + 1
                    q.put(v)
        running_set &= {p for p, d in distances.items() if d == delay}
    return {p.id for p in persons if p.home_planet in running_set}


if __name__ == "__main__":
    persons = read_persons("population.txt")
    p1 = puzzle1(persons)
    print(f"p1: {sum(map(int, p1))}")
    p2 = puzzle2(persons)
    print(f"p2: {sum(map(int, p2))}")
