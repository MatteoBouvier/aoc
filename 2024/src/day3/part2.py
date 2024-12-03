import re
from operator import mul


OP = re.compile(r"(mul\(\d+,\d+\))|(do\(\))|(don't\(\))")


def main() -> int:
    total: int = 0
    enabled: bool = True

    with open("input.txt", "r") as memory:
        for re_match in OP.finditer("".join(memory.readlines()).replace("\n", "")):
            match re_match.group(0).split("(")[0]:
                case "do":
                    enabled = True

                case "don't":
                    enabled = False

                case "mul":
                    if enabled:
                        total += mul(*map(int, re_match.group(0)[4:-1].split(",")))

                case _:
                    raise RuntimeError(re_match.group(0))

    return total


if __name__ == "__main__":
    print(main())
