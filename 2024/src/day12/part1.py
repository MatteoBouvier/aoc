import queue as q
from dataclasses import dataclass


@dataclass
class Region:
    kind: str
    plots: list[tuple[int, int]]
    to_visit: q.Queue[tuple[int, int]] = q.Queue()

    @property
    def area(self) -> int:
        return len(self.plots)

    @property
    def perimeter(self) -> int:
        perimeter = 0

        for x, y in self.plots:
            for offset in (x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y):
                if offset not in self.plots:
                    perimeter += 1

        return perimeter

    @property
    def sides(self) -> int:
        sides = 0

        for x, y in self.plots:
            for neighboors in (
                [
                    (x, y - 1) in self.plots,
                    (x - 1, y - 1) in self.plots,
                    (x - 1, y) in self.plots,
                ],
                [
                    (x, y + 1) in self.plots,
                    (x + 1, y + 1) in self.plots,
                    (x + 1, y) in self.plots,
                ],
            ):
                if neighboors in ([False, False, False], [False, True, False]):
                    sides += 2

                elif neighboors in ([False, True, True], [True, True, False]):
                    sides += 1

        return sides


def main():
    with open("input.txt", "r") as file:
        map: list[list[str]] = [[c for c in line.strip()] for line in file.readlines()]
    max_x, max_y = len(map) - 1, len(map[0]) - 1

    regions: list[Region] = []

    to_visit: q.Queue[tuple[int, int]] = q.Queue()
    visited: set[tuple[int, int]] = set()

    current_region = Region(map[0][0], [(0, 0)])
    current_region.to_visit.put((0, 1))
    current_region.to_visit.put((1, 0))

    to_visit.put((0, 1))
    to_visit.put((1, 0))
    visited.add((0, 0))

    def in_bounds(x: int, y: int) -> bool:
        return max_x >= x >= 0 and max_y >= y >= 0

    while not to_visit.empty():
        while not current_region.to_visit.empty():
            x, y = current_region.to_visit.get()
            if (x, y) in visited:
                continue

            if map[x][y] == current_region.kind:
                current_region.plots.append((x, y))
                visited.add((x, y))

                for offset in (0, 1), (0, -1), (1, 0), (-1, 0):
                    new_x, new_y = x + offset[0], y + offset[1]
                    if (new_x, new_y) not in visited and in_bounds(new_x, new_y):
                        current_region.to_visit.put((new_x, new_y))

            else:
                to_visit.put((x, y))

        regions.append(current_region)

        x, y = to_visit.get()
        while (x, y) in visited:
            if to_visit.empty():
                break
            x, y = to_visit.get()

        current_region = Region(map[x][y], [(x, y)])
        visited.add((x, y))

        for offset in (0, 1), (0, -1), (1, 0), (-1, 0):
            new_x, new_y = x + offset[0], y + offset[1]
            if (new_x, new_y) not in visited and in_bounds(new_x, new_y):
                current_region.to_visit.put((new_x, new_y))

    print("part1:", sum(region.area * region.perimeter for region in regions))
    print("part2:", sum(region.area * region.sides for region in regions))


if __name__ == "__main__":
    main()
