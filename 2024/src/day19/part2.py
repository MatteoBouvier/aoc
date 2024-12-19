from collections import defaultdict


def nb_possible_arrangements(design: str, towels: list[str]) -> int:
    cache: defaultdict[str, int] = defaultdict(lambda: 0)

    cache[""] = 1

    for i in range(1, len(design) + 1):
        design_i = design[-i:]
        cache[design_i] = 0

        for towel in towels:
            if design_i.startswith(towel):
                sub_design = design_i[len(towel) :]
                cache[design_i] += cache[sub_design]

    return cache[design]


def main() -> None:
    towels: list[str] = []
    designs: list[str] = []

    with open("input.txt") as data:
        towels = data.readline().strip().split(", ")
        assert data.readline() == "\n"

        for line in data:
            designs.append(line.strip())

    count = 0
    for i, design in enumerate(designs):
        nb = nb_possible_arrangements(design, towels)
        count += nb

    print(count)


if __name__ == "__main__":
    main()
