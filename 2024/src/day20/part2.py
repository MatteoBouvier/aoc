from __future__ import annotations
from collections.abc import Generator
from dataclasses import dataclass, field
import sys
from queue import LifoQueue
from typing import override, cast
from collections import defaultdict


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
    previous: Step | None = field(default=None, compare=False, repr=False)
    len: int = field(default=0, compare=False)

    def __add__(self, offset: tuple[int, int]) -> Step:
        return Step(self.x + offset[0], self.y + offset[1], self, self.len + 1)

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
        i = step.len
        while step is not None:
            map_[step.x][step.y] = str(i % 10)
            step = step.previous
            i -= 1

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


def get_cheats(path: Step) -> defaultdict[int, int]:
    cheats: defaultdict[int, int] = defaultdict(lambda: 0)
    steps: dict[tuple[int, int], int] = {}

    end = path
    while end is not None:
        steps[(end.x, end.y)] = end.len
        end = end.previous

    def neighbors(step: Step) -> Generator[tuple[tuple[int, int], int]]:
        for x_offset in range(-20, 20 + 1):
            for y_offset in range(-20, 20 + 1):
                path_len = abs(x_offset) + abs(y_offset)
                if path_len > 20:
                    continue

                x = step.x + x_offset
                y = step.y + y_offset

                yield (x, y), path_len

    end = path
    while end is not None:
        for coord, cheat_path_len in neighbors(end):
            path_len_at_cheat = steps.get(coord)
            if path_len_at_cheat is None:
                continue

            delta_len = end.len - path_len_at_cheat - cheat_path_len

            if delta_len >= 100:
                cheats[delta_len] += 1

        end = end.previous

    return cheats


def main(file: str) -> None:
    map = get_map(file)

    path = get_path(map)
    if path is None:
        raise RuntimeError

    counts = get_cheats(path)
    # print(sorted([(k, v) for k, v in counts.items()], key=lambda x: x[0]))
    print(sum(count for count in counts.values()))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "input.txt")
