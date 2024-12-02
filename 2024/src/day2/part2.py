import itertools as it


def as_list_diff(line: str) -> list[int]:
    return list(map(int, line.split(" ")))


def is_valid(levels: list[int]) -> bool:
    differences = [b - a for a, b in it.pairwise(levels)]

    return all(3 >= diff >= 1 for diff in differences) or all(
        -1 >= diff >= -3 for diff in differences
    )


def main() -> int:
    counter = 0

    with open("input.txt", "r") as data:
        for line_nb, line in enumerate(data.readlines()):
            levels = as_list_diff(line)

            if is_valid(levels):
                print(f"({counter}/{line_nb}) +  ", levels)
                counter += 1
                continue

            found_valid = False
            for i in range(len(levels)):
                part = [level for idx, level in enumerate(levels) if idx != i]

                if is_valid(part):
                    print(f"({counter}/{line_nb}) X+ ", levels, part)
                    counter += 1

                    found_valid = True

                    break

            if found_valid:
                continue

            print(f"({counter}/{line_nb}) X  ", levels)

    return counter


if __name__ == "__main__":
    print(main())
