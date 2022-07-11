class Person:
    name: str
    id: str
    access_key: int
    hour: int
    minute: int

    def __init__(self, line):
        parts = line.split(",")
        self.name = parts[0].strip()
        self.id = parts[1].strip()
        self.access_key = int(parts[2].strip())
        login_time = parts[3].strip().split(":")
        self.hour = int(login_time[0])
        self.minute = int(login_time[1])


def read_persons() -> list[Person]:
    with open("office_database.txt", "r") as f:
        return [Person(line) for line in f]


def puzzle1(persons: list[Person]) -> set[str]:
    return {p.id for p in persons if "814" in p.id}


def puzzle2(persons: list[Person]) -> set[str]:
    return {p.id for p in persons if p.access_key & 8 == 8}


if __name__ == "__main__":
    persons = read_persons()
    p1 = puzzle1(persons)
    print(f"p1: {sum(map(int, p1))}")
    p2 = puzzle2(persons)
    print(f"p2: {sum(map(int, p2))}")
