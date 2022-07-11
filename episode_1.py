class Person:
    def __init__(self, lines: list[str]):
        self.name = lines[0].split(":")[1].strip()
        self.id = lines[1].split(":")[1].strip()
        self.home_planet = lines[2].split(":")[1].strip()
        self.blood_sample = [line.strip()[1:-1] for line in lines[5:11]]

    def has_pico(self) -> bool:
        transpose = ["".join(s) for s in zip(*self.blood_sample)]
        return any("pico" in r or "ocip" in r for r in self.blood_sample) or any(
            "pico" in r or "ocip" in r for r in transpose
        )


def read_persons(fname: str) -> list[Person]:
    with open(fname, "r") as f:
        lines = f.readlines()
    return [Person(lines[i : i + 14]) for i in range(0, len(lines), 14)]


def puzzle1(persons: list[Person]) -> set[str]:
    return {p.id for p in persons if p.has_pico()}


if __name__ == "__main__":
    persons = read_persons("population.txt")
    p1 = puzzle1(persons)
    print(f"p1: {sum(map(int, p1))}")
