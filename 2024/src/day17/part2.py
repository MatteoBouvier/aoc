from collections.abc import Generator


def get_out(a: int) -> int:
    b = (a % 8) ^ 1
    return (b ^ (a // 2**b) ^ 4) % 8


def get_all_out(a: int) -> list[int]:
    out: list[int] = []
    while a > 0:
        out.append(get_out(a))
        a = a // 8

    return out


def next_A(seq: int, a: int) -> Generator[int]:
    while True:
        out = get_out(a)
        if out == seq:
            yield a

        a += 1


def main() -> None:
    seq: list[int] = [0, 3, 5, 5, 3, 0, 4, 1, 7, 4, 5, 7, 1, 1, 4, 2]
    a: int = 0

    steps: dict[int, Generator[int]] = {}
    i = 1
    while True:
        if i == len(seq) + 1:
            break

        s = seq[i - 1]

        if i not in steps:
            steps[i] = next_A(s, a)

        a = next(steps[i])

        out = get_all_out(a)
        if out == list(reversed(seq[:i])):
            i += 1
            a *= 8

    print(a // 8)


if __name__ == "__main__":
    main()
