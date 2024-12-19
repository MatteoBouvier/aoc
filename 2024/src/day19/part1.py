def possible_design(design: str, towels: list[str]) -> bool:
    if design == "":
        return True

    for towel in towels:
        if design.startswith(towel) and possible_design(design[len(towel) :], towels):
            return True

    return False


def main() -> None:
    towels: list[str] = []
    designs: list[str] = []

    with open("input.txt") as data:
        towels = data.readline().strip().split(", ")
        assert data.readline() == "\n"

        for line in data:
            designs.append(line.strip())

    count = 0
    for design in designs:
        if possible_design(design, towels):
            count += 1

    print(count)


if __name__ == "__main__":
    main()
