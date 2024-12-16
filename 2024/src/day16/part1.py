from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, cast, override
from queue import Queue

MOVES: dict[Literal["N", "S", "E", "W"], tuple[int, int]] = {
    "E": (0, 1),
    "W": (0, -1),
    "S": (1, 0),
    "N": (-1, 0),
}

INVERSE: dict[Literal["N", "S", "E", "W"], Literal["N", "S", "E", "W"]] = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E",
}


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, other: object) -> Position:
        if not isinstance(other, tuple):
            raise RuntimeError

        other = cast(tuple[int, int], other)
        return Position(self.x + other[0], self.y + other[1])

    @override
    def __hash__(self) -> int:
        return hash((self.x, self.y))


@dataclass(eq=False, frozen=True)
class Step:
    pos: Position
    dir: Literal["N", "S", "E", "W"]
    cost: int
    positions: list[Position] = field(default_factory=list, repr=False)

    @override
    def __eq__(self, value: object, /) -> bool:
        return (
            isinstance(value, Step) and self.pos == value.pos and self.dir == value.dir
        )

    @override
    def __hash__(self) -> int:
        return hash(self.pos) + hash(self.dir)

    def new(
        self, new_pos: Position, dir: Literal["N", "S", "E", "W"], cost: int
    ) -> Step:
        positions = [pos for pos in self.positions]
        positions.append(self.pos)

        return Step(new_pos, dir, cost, positions)


DIR_REPR = {"N": "^", "S": "v", "E": ">", "W": "<"}


def print_map(
    map: list[list[str]],
    visited: dict[tuple[Position, Literal["N", "S", "E", "W"]], Step],
    last_step: Step,
    limit_x: tuple[int, int] = (0, 10_000),
    limit_y: tuple[int, int] = (0, 10_000),
) -> None:
    to_print = [[cell if cell != "." else " " for cell in line] for line in map]

    for step in visited.values():
        to_print[step.pos.x][step.pos.y] = DIR_REPR[step.dir]

    to_print[last_step.pos.x][last_step.pos.y] = (
        "\033[31m" + DIR_REPR[last_step.dir] + "\033[39m"
    )

    print(
        "\n".join(
            [
                "".join(
                    [e for y, e in enumerate(line) if limit_y[0] <= y <= limit_y[1]]
                )
                for x, line in enumerate(to_print)
                if limit_x[0] <= x <= limit_x[1]
            ]
        )
    )


def print_map_one(map: list[list[str]], step: Step) -> None:
    to_print = [[cell if cell != "." else " " for cell in line] for line in map]

    for pos in step.positions:
        to_print[pos.x][pos.y] = "."

    to_print[step.pos.x][step.pos.y] = "\033[31m" + DIR_REPR[step.dir] + "\033[39m"

    print("   " + "".join([f"{i:<5}" for i in range(0, len(map[0]), 5)]))
    print(
        "\n".join(
            [
                "".join([f"{idx:>3}" if idx % 5 == 0 else "   "] + line)
                for idx, line in enumerate(to_print)
            ]
        )
    )


def main() -> None:
    map: list[list[str]] = []
    start = (0, 0)
    end = (0, 0)

    with open("input.txt") as file:
        for x, line in enumerate(file):
            line = line.strip()
            idx_start = line.find("S")
            if idx_start > -1:
                start = (x, idx_start)

            idx_end = line.find("E")
            if idx_end > -1:
                end = (x, idx_end)

            map.append(list(line.replace("S", ".").replace("E", ".")))

    to_visit: Queue[Step] = Queue()
    visited: dict[tuple[Position, Literal["N", "S", "E", "W"]], Step] = {}

    start = Position(*start)
    end = Position(*end)

    root = Step(start, "E", 0)
    to_visit.put(root)
    visited[(start, "E")] = root

    paths: list[Step] = []

    while not to_visit.empty():
        step = to_visit.get()
        if step.pos == end:
            paths.append(step)
            continue

        for dir, offset in MOVES.items():
            new_pos = step.pos + offset
            if dir != INVERSE[step.dir] and map[new_pos.x][new_pos.y] != "#":
                new_step = step.new(
                    new_pos, dir, step.cost + (1 if dir == step.dir else 1001)
                )

                if (new_pos, dir) in visited:
                    if visited[(new_pos, dir)].cost < new_step.cost:
                        continue

                if new_pos != end:
                    visited[(new_pos, dir)] = new_step

                to_visit.put(new_step)

    min_cost = min(path.cost for path in paths)

    best_tiles: set[Position] = set()
    for path in paths:
        if path.cost == min_cost:
            print(path)
            best_tiles = best_tiles.union(path.positions)
            print_map_one(map, path)

    print("part1", min_cost)
    print("part2", len(best_tiles) + 1)


if __name__ == "__main__":
    main()
