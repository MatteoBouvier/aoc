from typing import Literal
from dataclasses import dataclass


@dataclass
class Robot:
    x: int
    y: int


def print_map(map: list[list[Literal["#", "O", "."]]], robot: Robot) -> None:
    for x, line in enumerate(map):
        if x == robot.x:
            line = [c for c in line]
            line[robot.y] = "@"

        print("".join(line))


def GPS(x: int, y: int) -> int:
    return 100 * x + y


def push_box(
    map: list[list[Literal["#", "O", "."]]],
    x: int,
    y: int,
    direction: Literal["left", "right", "up", "down"],
) -> bool:
    assert len(map) > x >= 0
    assert len(map[0]) > y >= 0
    assert map[x][y] == "O"

    match direction:
        case "right":
            if map[x][y + 1] == "#":
                return False

            elif map[x][y + 1] == "." or push_box(map, x, y + 1, "right"):
                map[x][y] = "."
                map[x][y + 1] = "O"
                return True

            return False

        case "left":
            if map[x][y - 1] == "#":
                return False

            elif map[x][y - 1] == "." or push_box(map, x, y - 1, "left"):
                map[x][y] = "."
                map[x][y - 1] = "O"
                return True

            return False

        case "up":
            if map[x - 1][y] == "#":
                return False

            elif map[x - 1][y] == "." or push_box(map, x - 1, y, "up"):
                map[x][y] = "."
                map[x - 1][y] = "O"
                return True

            return False

        case "down":
            if map[x + 1][y] == "#":
                return False

            elif map[x + 1][y] == "." or push_box(map, x + 1, y, "down"):
                map[x][y] = "."
                map[x + 1][y] = "O"
                return True

            return False


def main() -> None:
    moves: str = ""
    map: list[list[Literal["#", "O", "."]]] = []
    robot = Robot(0, 0)

    parsing_map = True
    with open("input.txt") as file:
        for x, line in enumerate(file):
            if line == "\n":
                parsing_map = False
                continue

            if parsing_map:
                map.append(list(line.strip().replace("@", ".")))  # pyright: ignore[reportArgumentType]

                y = line.find("@")
                if y > -1:
                    robot.x, robot.y = x, y

            else:
                moves += line.strip()

    for move in moves:
        match move:
            case ">":
                if map[robot.x][robot.y + 1] == ".":
                    robot.y += 1

                elif map[robot.x][robot.y + 1] == "O" and push_box(
                    map, robot.x, robot.y + 1, "right"
                ):
                    robot.y += 1

            case "<":
                if map[robot.x][robot.y - 1] == ".":
                    robot.y -= 1

                elif map[robot.x][robot.y - 1] == "O" and push_box(
                    map, robot.x, robot.y - 1, "left"
                ):
                    robot.y -= 1

            case "^":
                if map[robot.x - 1][robot.y] == ".":
                    robot.x -= 1

                elif map[robot.x - 1][robot.y] == "O" and push_box(
                    map, robot.x - 1, robot.y, "up"
                ):
                    robot.x -= 1

            case "v":
                if map[robot.x + 1][robot.y] == ".":
                    robot.x += 1

                elif map[robot.x + 1][robot.y] == "O" and push_box(
                    map, robot.x + 1, robot.y, "down"
                ):
                    robot.x += 1

            case _:
                raise ValueError

    print(
        sum(
            GPS(x, y)
            for x, line in enumerate(map)
            for y, char in enumerate(line)
            if char == "O"
        )
    )


if __name__ == "__main__":
    main()
