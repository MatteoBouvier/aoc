import sys
from math import log10


def change_stone(stone: int) -> tuple[int, ...]:
    if stone == 0:
        return (1,)

    nb_digits = int(log10(stone)) + 1
    if nb_digits % 2 == 0 and nb_digits >= 2:
        stone_str = str(stone)
        return (int(stone_str[: nb_digits // 2]), int(stone_str[nb_digits // 2 :]))

    return (stone * 2024,)


def main() -> int:
    stone_counts: dict[int, int] = {}
    for stone in list(map(int, next(sys.stdin).strip().split(" "))):
        _ = stone_counts.setdefault(stone, 0)
        stone_counts[stone] += 1

    for _ in range(75):
        new_counts: dict[int, int] = {}
        for stone, count in stone_counts.items():
            for new_stone in change_stone(stone):
                _ = new_counts.setdefault(new_stone, 0)
                new_counts[new_stone] += count

        stone_counts = new_counts

    return sum(count for count in stone_counts.values())


if __name__ == "__main__":
    print(main())
