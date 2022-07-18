from collections import defaultdict
from itertools import chain
from skspatial.objects import Plane, Points
from typing import Dict, List, Set, Tuple


class Person:
    def __init__(self, lines: List[str]):
        self.name = lines[0].split(":")[1].strip()
        self.id = lines[1].split(":")[1].strip()
        self.home_planet = lines[2].split(":")[1].strip()
        self.blood_sample = [line.strip()[1:-1] for line in lines[5:11]]

    def has_pico(self) -> bool:
        transpose = ("".join(s) for s in zip(*self.blood_sample))
        return any(
            "pico" in r or "ocip" in r for r in chain(self.blood_sample, transpose)
        )


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


def puzzle1(persons: List[Person]) -> Set[str]:
    return {p.id for p in persons if p.has_pico()}


def puzzle2(persons: List[Person]) -> Set[str]:
    galaxy = read_galaxy("galaxy_map.txt")
    plane = Plane.best_fit(Points(list(galaxy.values())))
    outliers = {k for k, v in galaxy.items() if plane.distance_point(v) > 2}
    return {p.id for p in persons if p.home_planet in outliers}


def puzzle3(persons: List[Person]) -> Set[str]:
    visited = defaultdict(list)
    with open("security_log.txt", "r") as f:
        for line in f:
            if line.startswith("Place:"):
                place = line.split(":")[1].strip()
            elif line.startswith("in"):
                for person in line.split(":")[1].strip().split(","):
                    visited[person.strip()].append((time, place))
            elif not line.startswith("out") and ":" in line:
                time = tuple(map(int, line.split(":")))

    seq = ["Junkyard", "Pod Racing Track", "Pod Racing Track", "Palace", "Factory"]

    def match(places: List[Tuple[int, str]]) -> bool:
        return len(places) == len(seq) and all(i[1] == j for i, j in zip(places, seq))

    return {p.id for p in persons if match(sorted(visited[p.name]))}


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
