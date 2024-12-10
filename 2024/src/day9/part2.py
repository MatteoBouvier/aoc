from collections.abc import Generator
from dataclasses import dataclass
import sys
from typing import override


@dataclass
class Block:
    len: int
    ID: int = -1


@dataclass(repr=False)
class Memory:
    blocks: list[Block]

    @override
    def __repr__(self) -> str:
        return "".join("." if ID is None else str(ID) for ID in self.iter())

    def iter(self) -> Generator[int | None, None, None]:
        for block in self.blocks:
            for _ in range(block.len):
                yield block.ID if block.ID > -1 else None

    @property
    def empty(self) -> Generator[tuple[int, Block], None, None]:
        for idx, block in enumerate(self.blocks):
            if block.ID == -1:
                yield idx, block


def parse(data: str) -> Memory:
    blocks: list[Block] = []

    is_empty = False

    for ID, length in enumerate(map(int, data)):
        blocks.append(Block(length, -1 if is_empty else ID // 2))

        is_empty = not is_empty

    return Memory(blocks)


def compact_one(data: Memory, idx_file: int, file: Block) -> None:
    for idx_empty, empty in data.empty:
        if idx_empty >= idx_file:
            return

        if empty.len == file.len:
            data.blocks[idx_empty] = file
            data.blocks[idx_file] = Block(file.len)
            break

        if empty.len > file.len:
            data.blocks.insert(idx_empty, file)
            empty.len -= file.len
            data.blocks[idx_file + 1] = Block(file.len)
            break


def compact(data: Memory) -> Memory:
    moved_files: set[int] = set()

    while True:
        for idx, block in enumerate(reversed(data.blocks)):
            if block.ID != -1 and block.ID not in moved_files:
                compact_one(data, len(data.blocks) - idx - 1, block)
                moved_files.add(block.ID)
                break

        else:
            break

    return data


def checksum(data: Memory) -> int:
    return sum(idx * ID for idx, ID in enumerate(data.iter()) if ID is not None)


def main() -> int:
    data = parse(next(sys.stdin).strip())

    compacted_data = compact(data)
    return checksum(compacted_data)


if __name__ == "__main__":
    print(main())
