from typing import NamedTuple
from decimal import Decimal


class Machine(NamedTuple):
    ax: Decimal
    ay: Decimal
    bx: Decimal
    by: Decimal
    x: Decimal
    y: Decimal


A_COST = 3
B_COST = 1


def get_cost(machine: Machine) -> int:
    nb_b = (machine.y * machine.ax - machine.x * machine.ay) / (
        machine.by * machine.ax - machine.bx * machine.ay
    )
    nb_a = (machine.x - machine.bx * nb_b) / machine.ax

    if nb_b % 1 == 0 and nb_a % 1 == 0:
        return int(nb_a) * A_COST + int(nb_b) * B_COST
    return 0


def get_coefficients(line: str) -> tuple[Decimal, Decimal]:
    f1, f2 = line.find("+"), line.find(",")
    f3 = line.find("+", f2)

    return Decimal(line[f1 + 1 : f2]), Decimal(line[f3 + 1 :])


def get_goals(line: str) -> tuple[Decimal, Decimal]:
    f1, f2 = line.find("="), line.find(",")
    f3 = line.find("=", f2)

    return Decimal(line[f1 + 1 : f2]), Decimal(line[f3 + 1 :])


def main() -> None:
    machines: list[Machine] = []

    with open("input.txt", "r") as file:
        for line1 in file:
            line2, line3, _ = next(file), next(file), next(file)

            machines.append(
                Machine(
                    *get_coefficients(line1.strip()),
                    *get_coefficients(line2.strip()),
                    *get_goals(line3.strip()),
                )
            )

    print("part1", sum(get_cost(machine) for machine in machines))
    print(
        "part2",
        sum(
            get_cost(machine)
            for machine in (
                Machine(
                    m.ax, m.ay, m.bx, m.by, m.x + 10000000000000, m.y + 10000000000000
                )
                for m in machines
            )
        ),
    )


if __name__ == "__main__":
    main()
