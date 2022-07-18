from collections import defaultdict
from itertools import tee
from queue import Queue
from typing import Dict, Iterator, List, Set, Tuple


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class Person:
    def __init__(self, lines: List[str]):
        self.name = lines[0].split(":")[1].strip()
        self.id = lines[1].split(":")[1].strip()
        self.home_planet = lines[2].split(":")[1].strip()
        self.blood = [line.strip()[1:-1] for line in lines[5:11]]

    def _bendy_path(self, s: str, i: int, j: int) -> Iterator[Set[Tuple[int, int]]]:
        path = []

        def helper(i: int, j: int, k: int = 0):
            if k == len(s):
                yield set(path)
            elif (
                0 <= i < len(self.blood)
                and 0 <= j < len(self.blood[i])
                and self.blood[i][j] == s[k]
            ):
                path.append((i, j))
                for i, j in ((i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)):
                    yield from helper(i, j, k + 1)
                path.pop()

        return helper(i, j)

    def has_pico(self, seqs: List[str]) -> bool:
        paths = {
            seq: [
                path
                for i in range(len(self.blood))
                for j in range(len(self.blood[i]))
                for path in self._bendy_path(seq, i, j)
            ]
            for seq in seqs
        }

        def no_overlap(chosen: Set[Tuple[int, int]], i: int = 0) -> bool:
            return i == len(seqs) or any(
                all(p not in chosen for p in path) and no_overlap(chosen | path, i + 1)
                for path in paths[seqs[i]]
            )

        return no_overlap(set())


def read_persons(fname: str) -> List[Person]:
    with open(fname, "r") as f:
        lines = f.readlines()
    return [Person(lines[i : i + 14]) for i in range(0, len(lines), 14)]


def read_galaxy(fname: str) -> Dict[str, List[int]]:
    with open(fname, "r") as f:
        return {
            line[0].strip(): list(int(x) for x in line[1].strip()[1:-1].split(","))
            for line in map(lambda line: line.split(":"), f)
        }


def dist(x: Tuple[float, float, float], y: Tuple[float, float, float]) -> float:
    return sum((a - b) ** 2 for a, b in zip(x, y)) ** 0.5


def puzzle1(persons: List[Person]) -> Set[str]:
    seqs = ["pic", "opi", "cop", "ico"]
    return {p.id for p in persons if p.has_pico(seqs)}


def puzzle2(persons: List[Person]) -> Set[str]:
    signal_ranging = {"Venis": 2, "Cetung": 4, "Phoensa": 9}
    galaxy = read_galaxy("galaxy_map.txt")
    graph = {
        u: [v for v, y in galaxy.items() if dist(x, y) < 50] for u, x in galaxy.items()
    }
    running_set = set(galaxy.keys())
    for planet, delay in signal_ranging.items():
        q = Queue()
        q.put(planet)
        distances = {planet: 0}
        while not q.empty():
            u = q.get()
            for v in graph[u]:
                if v not in distances:
                    distances[v] = distances[u] + 1
                    q.put(v)
        running_set &= {p for p, d in distances.items() if d == delay}
    return {p.id for p in persons if p.home_planet in running_set}


def puzzle3(persons: List[Person]) -> Set[str]:
    travel_times = {
        "Bio-Lab": 21,
        "Factory": 18,
        "Shopping Mall": 17,
        "Food Plant": 20,
        "Office Station": 20,
        "Gym": 7,
        "Starship Garage": 16,
        "Happy-Center": 27,
        "Palace": 37,
        "Junkyard": 16,
        "Pod Racing Track": 19,
        "Mining Outpost": 15,
        "placeholder": float("inf"),
    }

    absolute_time = lambda h, m: h * 60 + m

    visited = defaultdict(lambda: [["placeholder", float("inf"), None]])
    with open("security_log.txt", "r") as f:
        for line in f:
            if line.startswith("Place:"):
                place = line.split(":")[1].strip()
            elif line.startswith("in:"):
                for person in line.split(":")[1].strip().split(","):
                    visited[person.strip()].append([place, time])
            elif line.startswith("out:"):
                for person in line.split(":")[1].strip().split(","):
                    visited[person.strip()][-1].append(time)
            elif ":" in line:
                time = absolute_time(*map(int, line.split(":")))

    window = (absolute_time(11, 0), absolute_time(13, 0))
    crime_time = 20

    names = {
        person
        for person, log in visited.items()
        if any(
            max(enter + travel_times[src], window[0]) + crime_time
            <= min(window[1], leave - travel_times[dest])
            for (src, _, enter), (dest, leave, _) in pairwise(
                sorted(log, key=lambda x: x[1])
            )
        )
    }
    return {p.id for p in persons if p.name in names}


if __name__ == "__main__":
    persons = read_persons("population.txt")
    p1 = puzzle1(persons)
    print(f"p1: {sum(map(int, p1))}")
    p2 = puzzle2(persons)
    print(f"p2: {sum(map(int, p2))}")
    p3 = puzzle3(persons)
    print(f"p3: {sum(map(int, p3))}")
    culprit_id = (p1 & p2 & p3).pop()
    print(f"culprit name: {[p.name for p in persons if p.id == culprit_id][0]}")
