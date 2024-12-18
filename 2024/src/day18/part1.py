from __future__ import annotations
from dataclasses import dataclass, field
import sys
from queue import Queue
from typing import override


MAP_SIZE = 71

OFFSETS: list[tuple[int, int]] = [
    (0, 1),  # down
    (0, -1),  # up
    (1, 0),  # right
    (-1, 0),  # left
]


@dataclass
class Step:
    x: int
    y: int
    previous: Step | None = field(default=None, compare=False)
    len: int = field(default=0, compare=False)

    def __add__(self, offset: tuple[int, int]) -> Step:
        return Step(self.x + offset[0], self.y + offset[1], self, self.len + 1)

    @override
    def __hash__(self) -> int:
        return hash((self.x, self.y))


def get_map(falling_bytes: list[tuple[int, int]]) -> list[list[str]]:
    lines = [["." for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]

    for byte in falling_bytes:
        lines[byte[1]][byte[0]] = "#"

    return lines


def print_map(map: list[list[str]], step: Step | None = None) -> None:
    if step is not None:
        map = [[c for c in line] for line in map]

        while step is not None:
            map[step.y][step.x] = "O"
            step = step.previous

    print("\n".join("".join(line) for line in map))


def in_bounds(step: Step) -> bool:
    return 0 <= step.x < MAP_SIZE and 0 <= step.y < MAP_SIZE


def shortest_path(
    map: list[list[str]], start: tuple[int, int], goal: tuple[int, int]
) -> int | None:
    to_visit: Queue[Step] = Queue()
    visited: set[Step] = set()

    to_visit.put(Step(*start))
    visited.add(Step(*start))

    paths: list[Step] = []

    while not to_visit.empty():
        step = to_visit.get()

        if (step.x, step.y) == goal:
            paths.append(step)
            continue

        for offset in OFFSETS:
            new_step = step + offset

            if (
                in_bounds(new_step)
                and map[new_step.y][new_step.x] != "#"
                and new_step not in visited
            ):
                to_visit.put(new_step)

                if (new_step.x, new_step.y) != goal:
                    visited.add(new_step)

    if not len(paths):
        return None

    return min(path.len for path in paths)


def binary_search(
    falling_bytes: list[tuple[int, int]], low: int, high: int
) -> tuple[int, int]:
    mid = -1

    while low <= high:
        mid = low + (high - low) // 2

        map = get_map(falling_bytes[: mid + 1])

        if shortest_path(map, (0, 0), (MAP_SIZE - 1, MAP_SIZE - 1)) is None:
            high = mid - 1

        else:
            low = mid + 1

    if mid < 0:
        raise RuntimeError

    return falling_bytes[mid]


def main(file: str) -> None:
    falling_bytes: list[tuple[int, int]] = []
    with open(file) as data:
        for line in data:
            coords = line.strip().split(",")
            falling_bytes.append((int(coords[0]), int(coords[1])))

    map = get_map(falling_bytes[:1024])
    print("part 1:", shortest_path(map, (0, 0), (MAP_SIZE - 1, MAP_SIZE - 1)))

    blocked_path = binary_search(falling_bytes, 1024, len(falling_bytes) - 1)
    print("part 2:", blocked_path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "input.txt")
