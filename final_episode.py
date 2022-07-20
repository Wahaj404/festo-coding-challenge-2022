from collections import defaultdict
from typing import Dict, List


def isCyclic(graph: Dict[str, List[str]]):
    vis = set()
    path = set()

    def helper(u: str):
        vis.add(u)
        path.add(u)
        ret = any((v not in vis and helper(v)) or v in path for v in graph[u])
        path.discard(u)
        return ret

    return any(helper(u) for u in graph)


def puzzle1():
    with open("scrap_scan.txt", "r") as f:
        clearable = []
        for line in f:
            line = line.strip()
            if line == "":
                if not isCyclic(graph):
                    clearable.append(int(num))
            elif line.startswith("Passage"):
                _, num = line.split()
                graph = {"-": []}
            else:
                u, vs = line.split(":")
                graph[u] = [v.strip() for v in vs.split(",")]
    return "-".join(map(str, sorted(clearable)))


if __name__ == "__main__":
    print(f"p1: {puzzle1()}")
