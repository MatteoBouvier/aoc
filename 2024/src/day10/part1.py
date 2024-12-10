from __future__ import annotations

import sys
import queue


def find_trailheads(map: list[list[int]]) -> list[tuple[int, int]]:
    max_x, max_y = len(map), len(map[0])
    trailheads: list[tuple[int, int]] = []

    for x in range(0, max_x):
        for y in range(0, max_y):
            if map[x][y] == 0:
                trailheads.append((x, y))

    return trailheads


def compute_score(trailhead: tuple[int, int], map: list[list[int]]) -> int:
    to_visit: queue.Queue[tuple[int, int]] = queue.Queue()
    visited: set[tuple[int, int]] = set()

    to_visit.put(trailhead)
    visited.add(trailhead)

    max_x, max_y = len(map), len(map[0])

    def in_bounds(x: int, y: int) -> bool:
        return max_x > x >= 0 and max_y > y >= 0

    score = 0

    while not to_visit.empty():
        x, y = to_visit.get()
        value = map[x][y]

        if value == 9:
            score += 1
            continue

        for offset in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            new_x, new_y = x + offset[0], y + offset[1]
            if (
                in_bounds(new_x, new_y)
                and (new_x, new_y) not in visited
                and map[new_x][new_y] == value + 1
            ):
                visited.add((new_x, new_y))
                to_visit.put((new_x, new_y))

    return score


def main() -> int:
    map: list[list[int]] = []

    for line in sys.stdin:
        map.append([int(i) for i in line.strip()])

    trailheads = find_trailheads(map)
    return sum(compute_score(trailhead, map) for trailhead in trailheads)


if __name__ == "__main__":
    print(main())
