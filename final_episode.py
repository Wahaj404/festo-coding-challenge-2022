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


def puzzle2():
    with open("bunker_gold.txt", "r") as f:
        lines = f.readlines()
    mx = float("-inf")
    for i in range(0, len(lines), 4):
        pname = lines[i]
        bunkers = [
            [int(bunker.strip()) for bunker in lines[i + j].strip().split(",")]
            for j in (1, 2)
        ]
        cols = len(bunkers[0])
        dp = [[0] * cols for _ in (0, 1)]
        dp[0][0] = bunkers[0][0]
        dp[1][0] = bunkers[1][0]
        for i in range(1, cols):
            dp[0][i] = max(bunkers[0][i] + dp[1][i - 1], dp[0][i - 1])
            dp[1][i] = max(bunkers[1][i] + dp[0][i - 1], dp[1][i - 1])
        res = max(dp[0][-1], dp[1][-1])
        if mx < res:
            mx = res
            planet = pname.strip()
    return f"{planet}{mx}"


if __name__ == "__main__":
    print(f"p1: {puzzle1()}")
    print(f"p2: {puzzle2()}")
