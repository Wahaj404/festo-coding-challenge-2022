from collections import defaultdict
import numpy as np
from typing import Dict, List, Set


class Person:
    def __init__(self, lines: List[str]):
        self.name = lines[0].split(":")[1].strip()
        self.id = lines[1].split(":")[1].strip()
        self.home_planet = lines[2].split(":")[1].strip()
        self.blood_sample = [line.strip()[1:-1] for line in lines[5:11]]

    def _has_pico(self, i: int, j: int, s="picoico") -> bool:
        return s == "" or (
            0 <= i < len(self.blood_sample)
            and 0 <= j < len(self.blood_sample[i])
            and self.blood_sample[i][j] == s[0]
            and any(
                self._has_pico(x, y, s[1:])
                for x, y in ((i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1))
            )
        )

    def has_pico(self) -> bool:
        return any(
            self._has_pico(i, j)
            for i in range(len(self.blood_sample))
            for j in range(len(self.blood_sample[i]))
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


def read_trade_routes(fname: str) -> Set[str]:
    with open(fname, "r") as f:
        return {
            tuple(planet.strip() for planet in line.split(":")[0].split("-"))
            for line in f
            if "Ok" in line
        }


def lineseg_dist(p: np.ndarray, a: np.ndarray, b: np.ndarray) -> float:
    d = np.divide(b - a, np.linalg.norm(b - a))
    return np.hypot(
        np.maximum.reduce([np.dot(a - p, d), np.dot(p - b, d), 0]),
        np.linalg.norm(np.cross(p - a, d)),
    )


def puzzle1(persons: List[Person]) -> Set[str]:
    return {p.id for p in persons if p.has_pico()}


def puzzle2(persons: List[Person]) -> Set[str]:
    trade_routes = read_trade_routes("trade_routes.txt")
    galaxy = read_galaxy("galaxy_map.txt")
    close_planets = {
        planet
        for planet, coords in galaxy.items()
        if all(
            lineseg_dist(
                np.asarray(coords), np.asarray(galaxy[a]), np.asarray(galaxy[b])
            )
            <= 10
            for a, b, in trade_routes
        )
    }
    return {p.id for p in persons if p.home_planet in close_planets}


def puzzle3(persons: List[Person]) -> Set[str]:
    visited = defaultdict(list)
    with open("security_log.txt", "r") as f:
        for line in f:
            if line.startswith("Place:"):
                place = line.split(":")[1].strip()
            elif line.startswith("in"):
                for person in line.split(":")[1].strip().split(","):
                    visited[person.strip()].append(time)
            elif line.startswith("out") and ":" in line:
                for person in line.split(":")[1].strip().split(","):
                    visited[person.strip()].append(time)
            elif ":" in line:
                time = tuple(map(int, line.split(":")))

    absolute_time = lambda h, m: h * 60 + m

    diffs = {
        person: [
            absolute_time(*b) - absolute_time(*a)
            for a, b in zip(times[0::2], times[1::2])
        ]
        for person, times in visited.items()
    }

    def sums_to(nums: List[int], target: int, i: int = 0):
        if i == len(nums) or target <= 0:
            return target == 0
        return sums_to(nums, target - nums[i], i + 1) or sums_to(nums, target, i + 1)

    return {p.id for p in persons if sums_to(diffs[p.name], 79)}


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
