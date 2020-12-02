import functools
from typing import List, Callable, Union
from math import inf

from collections import defaultdict

from .math import Point

def backtrack(vertices, current):
    total_path = [current]
    while current in vertices:
        current = vertices[current]
        total_path.append(current)
    
    return list(reversed(total_path))

grid_neighbors = [
    Point.from_tuple((0,  1)),
    Point.from_tuple((-1,  0)),
    Point.from_tuple(( 0, -1)),
    Point.from_tuple(( 1,  0)),
]



def find_path(
    start: Point,
    goal: Point,
    nodes: List[Point],
    h: Callable[[Point], Union[int, float]]
):
    openset = set([start])

    vertices = dict()

    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    f_score = defaultdict(lambda: inf)
    f_score[start] = h(start)

    while openset:
        current = min({s: v for s, v in f_score.items() if s in openset}, key=f_score.get)

        if current == goal:
            return backtrack(vertices, current)
        
        openset.remove(current)

        for delta in grid_neighbors:
            neighbor = current + delta
            if neighbor in nodes:
                new_g_score = g_score[current] + 1
                if new_g_score < g_score[neighbor]:
                    # This path to neighbor is better than any previous one. Record it!
                    vertices[neighbor] = current
                    g_score[neighbor] = new_g_score
                    f_score[neighbor] = g_score[neighbor] + h(neighbor)
                    openset.add(neighbor)
    
    raise RuntimeError("No path")