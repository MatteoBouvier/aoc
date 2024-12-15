from typing import Literal, cast
from dataclasses import dataclass


OFFSET = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0),
}


@dataclass
class Robot:
    x: int
    y: int


def print_map(
    map: list[list[Literal["#", "[", "]", "."]]], robot: Robot, direction: str = "@"
) -> None:
    for x, line in enumerate(map):
        if x == robot.x:
            line = [c for c in line]
            line = (
                line[: robot.y] + [f"\033[31m{direction}\033[39m"] + line[robot.y + 1 :]
            )

        print("".join(line))


def GPS(x: int, y: int) -> int:
    return 100 * x + y


def get_boxes(
    map: list[list[Literal["#", "[", "]", "."]]],
    x: int,
    y: int,
    direction: Literal[">", "<", "^", "v"],
    is_robot: bool,
) -> set[tuple[int, int]]:
    boxes: set[tuple[int, int]] = set()

    match direction:
        case ">":
            offset = 1 if is_robot else 2
            if map[x][y + offset] == "[":
                boxes.add((x, y + offset))

        case "<":
            if map[x][y - 1] == "]":
                boxes.add((x, y - 2))

        case "^":
            if map[x - 1][y] == "[":
                boxes.add((x - 1, y))

            elif map[x - 1][y] == "]":
                boxes.add((x - 1, y - 1))

            if not is_robot and map[x - 1][y + 1] == "[":
                boxes.add((x - 1, y + 1))

        case "v":
            if map[x + 1][y] == "[":
                boxes.add((x + 1, y))

            elif map[x + 1][y] == "]":
                boxes.add((x + 1, y - 1))

            if not is_robot and map[x + 1][y + 1] == "[":
                boxes.add((x + 1, y + 1))

    return boxes


def move_robot(
    map: list[list[Literal["#", "[", "]", "."]]],
    x: int,
    y: int,
    direction: Literal["<", ">", "^", "v"],
    is_robot: bool = False,
) -> tuple[bool, set[tuple[int, int]]]:
    assert len(map) > x >= 0
    assert len(map[0]) > y >= 0

    boxes = get_boxes(map, x, y, direction, is_robot)

    match direction:
        case ">":
            offset = 1 if is_robot else 2
            if map[x][y + offset] == "#":
                return False, set()

            for box in boxes:
                can_move, boxes_to_move = move_robot(map, *box, ">")

                if not can_move:
                    return False, set()

                boxes = boxes.union(boxes_to_move)

            if is_robot:
                for box in sorted(list(boxes), key=lambda x: -x[1]):
                    map[box[0]][box[1]] = "."
                    map[box[0]][box[1] + 1] = "["
                    map[box[0]][box[1] + 2] = "]"

            return True, boxes

        case "<":
            if map[x][y - 1] == "#":
                return False, set()

            for box in boxes:
                can_move, boxes_to_move = move_robot(map, *box, "<")

                if not can_move:
                    return False, set()

                boxes = boxes.union(boxes_to_move)

            if is_robot:
                for box in sorted(list(boxes), key=lambda x: x[1]):
                    map[box[0]][box[1] + 1] = "."
                    map[box[0]][box[1]] = "]"
                    map[box[0]][box[1] - 1] = "["

            return True, boxes

        case "^":
            if map[x - 1][y] == "#" or (not is_robot and map[x - 1][y + 1] == "#"):
                return False, set()

            for box in boxes:
                can_move, boxes_to_move = move_robot(map, *box, "^")

                if not can_move:
                    return False, set()

                boxes = boxes.union(boxes_to_move)

            if is_robot:
                for box in sorted(list(boxes), key=lambda x: x[0]):
                    map[box[0]][box[1]] = "."
                    map[box[0]][box[1] + 1] = "."
                    map[box[0] - 1][box[1]] = "["
                    map[box[0] - 1][box[1] + 1] = "]"

            return True, boxes

        case "v":
            if map[x + 1][y] == "#" or (not is_robot and map[x + 1][y + 1] == "#"):
                return False, set()

            for box in boxes:
                can_move, boxes_to_move = move_robot(map, *box, "v")

                if not can_move:
                    return False, set()

                boxes = boxes.union(boxes_to_move)

            if is_robot:
                for box in sorted(list(boxes), key=lambda x: -x[0]):
                    map[box[0]][box[1]] = "."
                    map[box[0]][box[1] + 1] = "."
                    map[box[0] + 1][box[1]] = "["
                    map[box[0] + 1][box[1] + 1] = "]"

            return True, boxes


def main() -> None:
    moves: str = ""
    map: list[list[Literal["#", "[", "]", "."]]] = []
    robot = Robot(0, 0)

    parsing_map = True
    with open("input.txt") as file:
        for x, line in enumerate(file):
            if line == "\n":
                parsing_map = False
                continue

            if parsing_map:
                line = line.strip()
                new_line = ["" for _ in range(len(line) * 2)]
                for idx, c in enumerate(line.replace("@", ".")):
                    if c in (".", "#"):
                        new_line[idx * 2] = c
                        new_line[idx * 2 + 1] = c

                    else:
                        new_line[idx * 2] = "["
                        new_line[idx * 2 + 1] = "]"

                map.append(new_line)  # pyright: ignore[reportArgumentType]

                y = line.find("@")
                if y > -1:
                    robot.x, robot.y = x, y * 2

            else:
                moves += line.strip()

    for move in moves:
        move = cast(Literal[">", "<", "^", "v"], move)
        can_move_robot, _ = move_robot(map, robot.x, robot.y, move, is_robot=True)

        if can_move_robot:
            robot.x += OFFSET[move][0]
            robot.y += OFFSET[move][1]

    print(
        sum(
            GPS(x, y)
            for x, line in enumerate(map)
            for y, char in enumerate(line)
            if char == "["
        )
    )


if __name__ == "__main__":
    main()
