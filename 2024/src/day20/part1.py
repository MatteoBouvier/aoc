from __future__ import annotations
from dataclasses import dataclass, field
import sys
from queue import LifoQueue
from typing import override
from collections import Counter


OFFSETS: list[tuple[int, int]] = [
    (0, 1),  # right
    (0, -1),  # left
    (1, 0),  # down
    (-1, 0),  # up
]


@dataclass
class Map:
    tiles: list[list[str]]
    start: tuple[int, int]
    end: tuple[int, int]


@dataclass
class Step:
    x: int
    y: int
    previous: Step | None = field(default=None, compare=False)
    next: Step | None = field(default=None, compare=False)

    def __add__(self, offset: tuple[int, int]) -> Step:
        return Step(self.x + offset[0], self.y + offset[1], self)

    @override
    def __hash__(self) -> int:
        return hash((self.x, self.y))


def get_map(file: str) -> Map:
    map: list[list[str]] = []
    start = (0, 0)
    end = (0, 0)

    with open(file) as data:
        for x, line in enumerate(data):
            line = line.strip()
            idx_start = line.find("S")
            if idx_start > -1:
                start = (x, idx_start)

            idx_end = line.find("E")
            if idx_end > -1:
                end = (x, idx_end)

            map.append(list(line.replace("S", ".").replace("E", ".")))

    return Map(map, start, end)


def print_map(map: Map, step: Step | None = None) -> None:
    map_ = [[c for c in line] for line in map.tiles]

    if step is not None:
        while step is not None:
            map_[step.x][step.y] = "O"
            step = step.previous

    map_[map.start[0]][map.start[1]] = "S"
    map_[map.end[0]][map.end[1]] = "E"

    print("\n".join("".join(line) for line in map_))


def get_path(map: Map) -> Step | None:
    to_visit: LifoQueue[Step] = LifoQueue()
    visited: set[Step] = set()

    to_visit.put(Step(*map.start))
    visited.add(Step(*map.start))

    path: Step | None = None

    while not to_visit.empty():
        step = to_visit.get()

        if (step.x, step.y) == map.end:
            path = step
            break

        for offset in OFFSETS:
            new_step = step + offset

            if map.tiles[new_step.x][new_step.y] != "#" and new_step not in visited:
                to_visit.put(new_step)
                visited.add(new_step)

    return path


def get_cheats(map: Map, path: Step) -> list[int]:
    cheats: list[int] = []

    end, start = path, path
    while True:
        if start.previous is None:
            break

        start_prev = start.previous
        start_prev.next = start
        start = start_prev

    def count_save(start: Step, end: Step | None) -> int:
        count = 0
        while end != start and end is not None:
            end = end.previous
            count += 1

        return count - 2

    end_ref = end
    while start != end_ref and start is not None:
        while end != start and end is not None:
            for offset in OFFSETS:
                if map.tiles[end.x + offset[0]][end.y + offset[1]] == "#" and (
                    end.x + offset[0] * 2,
                    end.y + offset[1] * 2,
                ) == (start.x, start.y):
                    cheats.append(count_save(start, end))

            end = end.previous

        start = start.next
        end = end_ref

    return cheats


def main(file: str) -> None:
    map = get_map(file)

    path = get_path(map)
    if path is None:
        raise RuntimeError

    counts = Counter(get_cheats(map, path))
    print(sum(count for saved, count in counts.items() if saved >= 100))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "input.txt")
