import itertools as it
from collections import defaultdict
from collections.abc import Generator


def get_antennas(line: str) -> Generator[tuple[str, int]]:
    for y, c in enumerate(line):
        if c != ".":
            yield (c, y)


def main(file_name: str) -> int:
    antennas: dict[str, list[tuple[int, int]]] = defaultdict(list)
    max_x, max_y = 0, 0

    with open(file_name, "r") as data:
        for x, line in enumerate(data.readlines()):
            line = line.strip()
            max_y = len(line) - 1

            for antenna, y in get_antennas(line):
                antennas[antenna].append((x, y))

            max_x = x

    def in_bounds_x(x: int) -> bool:
        return max_x >= x >= 0

    def in_bounds_y(y: int) -> bool:
        return max_y >= y >= 0

    antinodes: set[tuple[int, int]] = set()
    for antenna, coords in antennas.items():
        for coord_a, coord_b in it.combinations(coords, 2):
            delta_x = coord_b[0] - coord_a[0]
            delta_y = coord_b[1] - coord_a[1]

            x = coord_a[0]
            y = coord_a[1]

            while in_bounds_x(x) and in_bounds_y(y):
                antinodes.add((x, y))

                x += delta_x
                y += delta_y

            x = coord_a[0] - delta_x
            y = coord_a[1] - delta_y

            while in_bounds_x(x) and in_bounds_y(y):
                antinodes.add((x, y))

                x -= delta_x
                y -= delta_y

    return len(antinodes)


if __name__ == "__main__":
    print(main("input.txt"))
