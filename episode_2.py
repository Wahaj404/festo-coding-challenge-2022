import numpy as np


class Person:
    def __init__(self, lines: list[str]):
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


def read_trade_routes(fname: str) -> set[str]:
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


def puzzle1(persons: list[Person]) -> set[str]:
    return {p.id for p in persons if p.has_pico()}


def puzzle2(persons: list[Person]) -> set[str]:
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


if __name__ == "__main__":
    persons = read_persons("population.txt")
    p1 = puzzle1(persons)
    print(f"p1: {sum(map(int, p1))}")
    p2 = puzzle2(persons)
    print(f"p2: {sum(map(int, p2))}")
