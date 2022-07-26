from collections import defaultdict
from itertools import tee
from queue import PriorityQueue
from typing import Dict, List, Tuple
import networkx as nx


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


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
        bunkers = [
            [int(bunker.strip()) for bunker in lines[i + j].strip().split(",")]
            for j in (1, 2)
        ]
        cols = len(bunkers[0])
        dp = [[0] * cols for _ in (0, 1)]
        dp[0][0] = bunkers[0][0]
        dp[1][0] = bunkers[1][0]
        for j in range(1, cols):
            dp[0][j] = max(bunkers[0][j] + dp[1][j - 1], dp[0][j - 1])
            dp[1][j] = max(bunkers[1][j] + dp[0][j - 1], dp[1][j - 1])
        res = max(dp[0][-1], dp[1][-1])
        if mx < res:
            mx = res
            planet = lines[i].strip()
    return f"{planet}{mx}"


class Graph:
    def __init__(self):
        self._adj: Dict[str, Dict[str, int]] = defaultdict(dict)
        self._indices: Dict[Tuple[int, int], int] = {}
        self._removed = []
        self.cost = 0

    def add_edge(self, u: str, v: str, w: int, i: int):
        self._adj[u][v] = self._adj[v][u] = w
        self._indices[(u, v)] = self._indices[(v, u)] = i

    def remove_edge(self, u: str, v: str):
        self._removed.append((u, v, self._adj[u][v]))
        self.cost += self._adj[u][v]
        self._adj[u].pop(v)
        self._adj[v].pop(u)
        return self.cost

    def restore_edge(self):
        u, v, w = self._removed.pop()
        self._adj[u][v] = self._adj[v][u] = w
        self.cost -= w
        return self.cost

    def answer(self):
        return [self._indices[(u, v)] for u, v, _ in self._removed]

    def dijikstra(self, src: str, tgt: str):
        dist = {src: 0}
        pred = {src: None}

        pq = PriorityQueue()
        pq.put((0, src))

        while not pq.empty():
            d, u = pq.get()
            for v, w in self._adj[u].items():
                alt = d + w
                if v not in dist or dist[v] > alt:
                    dist[v] = alt
                    pred[v] = u
                    pq.put((alt, v))

        path = []
        if tgt in pred:
            while pred[tgt] is not None:
                path.append((pred[tgt], tgt))
                tgt = pred[tgt]
        return path


def puzzle3():
    graph = Graph()
    with open("machine_room.txt", "r") as f:
        for line in f:
            i, link, n = map(str.strip, line.split(":"))
            u, v = map(str.strip, link.split("-"))
            graph.add_edge(u, v, int(n), int(i))

    def dfs(ans_mn: List):
        path = graph.dijikstra("A", "Z")
        for u, v in path:
            graph.remove_edge(u, v)
            dfs(ans_mn)
            graph.restore_edge()
            if ans_mn[1] <= graph.cost:
                break
        if len(path) == 0 and ans_mn[1] > graph.cost:
            ans_mn[1] = graph.cost
            ans_mn[0] = graph.answer()

    ans_mn = [[], float("inf")]
    dfs(ans_mn)
    return "-".join(map(str, sorted(ans_mn[0])))


if __name__ == "__main__":
    print(f"p1: {puzzle1()}")
    print(f"p2: {puzzle2()}")
    print(f"p3: {puzzle3()}")
