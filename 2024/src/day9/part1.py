import sys
import itertools as it
from typing import cast


def repr_memory(data: list[int | None]) -> None:
    print("".join("." if element is None else str(element) for element in data))


def parse(data: str) -> list[int | None]:
    parsed_data: list[int | None] = []

    is_empty = False
    position = 0

    for ID, length in enumerate(map(int, data)):
        if is_empty:
            parsed_data.extend([None for _ in range(length)])

        else:
            parsed_data.extend([ID // 2 for _ in range(length)])

        position += length
        is_empty = not is_empty

    return parsed_data


def next_empty(data: list[int | None], last_pointer: int = 0) -> int:
    data = data[last_pointer:]
    return next(i for i, e in enumerate(data, start=last_pointer) if e is None)


def next_file_block(data: list[int | None], last_pointer: int = sys.maxsize) -> int:
    length = len(data) if last_pointer == sys.maxsize else last_pointer

    return (
        length
        - next(i for i, e in enumerate(reversed(data[:last_pointer])) if e is not None)
        - 1
    )


def compact(data: list[int | None]) -> list[int | None]:
    empty_pointer = next_empty(data)
    file_block_pointer = next_file_block(data)

    while empty_pointer < file_block_pointer:
        data[empty_pointer], data[file_block_pointer] = (
            data[file_block_pointer],
            data[empty_pointer],
        )

        empty_pointer = next_empty(data, empty_pointer)
        file_block_pointer = next_file_block(data, file_block_pointer)

    return data


def checksum(data: list[int | None]) -> int:
    return sum(
        [
            idx * cast(int, ID)
            for idx, ID in enumerate(it.takewhile(lambda e: e is not None, data))
        ]
    )


def main() -> int:
    data = parse(next(sys.stdin).strip())

    compacted_data = compact(data)
    return checksum(compacted_data)


if __name__ == "__main__":
    print(main())
