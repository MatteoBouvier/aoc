def INSTRUCTION(
    opcode: int, operand: int, registers: dict[str, int], stdout: list[int]
) -> None:
    match opcode:
        case 0:
            registers["A"] = registers["A"] // (2 ** COMBO_OPERAND(operand, registers))

        case 1:
            registers["B"] = registers["B"] ^ operand

        case 2:
            registers["B"] = COMBO_OPERAND(operand, registers) % 8

        case 3:
            if registers["A"] != 0:
                registers["INSTRUCTION"] = operand
                return

        case 4:
            registers["B"] = registers["B"] ^ registers["C"]

        case 5:
            stdout.append(COMBO_OPERAND(operand, registers) % 8)

        case 6:
            registers["B"] = registers["A"] // (2 ** COMBO_OPERAND(operand, registers))

        case 7:
            registers["C"] = registers["A"] // (2 ** COMBO_OPERAND(operand, registers))

        case _:
            raise RuntimeError

    registers["INSTRUCTION"] += 2


def COMBO_OPERAND(op: int, registers: dict[str, int]) -> int:
    if op < 4:
        return op

    return {4: registers["A"], 5: registers["B"], 6: registers["C"]}[op]


def fetch(program: list[int], pointer: int) -> tuple[int | None, int]:
    if pointer >= len(program):
        return None, 0

    return program[pointer], program[pointer + 1]


def run(program: list[int], registers: dict[str, int], stdout: list[int]) -> None:
    while True:
        opcode, operand = fetch(program, registers["INSTRUCTION"])
        if opcode is None:
            break

        # print(opcode, operand)
        INSTRUCTION(opcode, operand, registers, stdout)
        # for reg, val in registers.items():
        #     print(reg, val)
        # print("---------------------------------------------")


def main() -> None:
    registers: dict[str, int] = {"INSTRUCTION": 0, "A": 0, "B": 0, "C": 0}
    stdout: list[int] = []
    program: list[int] = []

    search = False

    with open("test6.txt") as file:
        for line in file:
            if line.startswith("Register"):
                register, value = line.split(":")
                if value.strip() == "?":
                    search = True
                else:
                    registers[register[-1]] = int(value.strip())

            elif line.startswith("Program"):
                values = line.split(":")[1].strip().split(",")
                program = [int(v) for v in values]

    if not search:
        run(program, registers, stdout)

        if len(stdout):
            print(",".join(map(str, stdout)))

    else:
        registers_copy = {reg: val for reg, val in registers.items()}
        registers_copy["A"] = -1

        while stdout != program:
            registers = {reg: val for reg, val in registers_copy.items()}
            registers["A"] += 1
            stdout = []

            run(program, registers, stdout)

        print(registers["A"])


if __name__ == "__main__":
    main()
