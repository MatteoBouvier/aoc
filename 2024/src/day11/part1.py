from collections.abc import Generator
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


def change_all_stones(stones: list[int]) -> Generator[int]:
    for stone in stones:
        yield from change_stone(stone)


def main() -> int:
    data: list[int] = list(map(int, next(sys.stdin).strip().split(" ")))

    for i in range(25):
        print(i)
        data = list(change_all_stones(data))

    return len(data)


if __name__ == "__main__":
    print(main())
