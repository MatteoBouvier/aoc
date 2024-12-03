import re
from operator import mul


MUL = re.compile(r"mul\(\d+,\d+\)")


def main() -> int:
    total: int = 0

    with open("input.txt", "r") as memory:
        for match in MUL.finditer("".join(memory.readlines()).replace("\n", "")):
            total += mul(*map(int, match.group(0)[4:-1].split(",")))

    return total


if __name__ == "__main__":
    print(main())
