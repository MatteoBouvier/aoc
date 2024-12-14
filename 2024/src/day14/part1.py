import numpy as np
from dataclasses import dataclass


@dataclass()
class Robot:
    x: int
    y: int
    vx: int
    vy: int


MAP_X, MAP_Y = 101, 103


def print_map(robots: list[Robot]) -> None:
    map = [["." for _ in range(MAP_X)] for _ in range(MAP_Y)]

    for robot in robots:
        map[robot.y][robot.x] = (
            "1" if map[robot.y][robot.x] == "." else str(int(map[robot.y][robot.x]) + 1)
        )

    for y in range(MAP_Y):
        print("".join(map[y]))

    print()


def get_values(line: str) -> tuple[int, int, int, int]:
    parts = [p.split("=")[1] for p in line.split(" ")]
    parts = [p.split(",") for p in parts]

    x, y = map(int, parts[0])
    vx, vy = map(int, parts[1])

    return x, y, vx, vy


def main() -> None:
    robots: list[Robot] = []
    with open("input.txt") as file:
        for line in file:
            robots.append(Robot(*get_values(line.strip())))

    for seconds in range(1, 10001):
        for robot in robots:
            robot.x = (robot.x + robot.vx) % MAP_X
            robot.y = (robot.y + robot.vy) % MAP_Y

        coordinates = np.array([[robot.y, robot.x] for robot in robots])

        hist = np.histogramdd(coordinates)[0]
        hist /= hist.sum()
        hist = hist.flatten()
        hist = hist[hist.nonzero()]
        entropy = -0.5 * np.sum(hist * np.log2(hist))

        if entropy < 2.9:
            print(f"{seconds}seconds elapsed", entropy)
            print_map(robots)
            _ = input()

    quad_top_left = 0
    quad_top_right = 0
    quad_bottom_left = 0
    quad_bottom_right = 0

    for robot in robots:
        if robot.x < MAP_X // 2:
            if robot.y < MAP_Y // 2:
                quad_top_left += 1

            elif robot.y > MAP_Y // 2:
                quad_bottom_left += 1

        elif robot.x > MAP_X // 2:
            if robot.y < MAP_Y // 2:
                quad_top_right += 1

            elif robot.y > MAP_Y // 2:
                quad_bottom_right += 1

    print(quad_top_left * quad_top_right * quad_bottom_left * quad_bottom_right)


if __name__ == "__main__":
    main()
