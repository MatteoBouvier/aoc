import sys
import itertools as it
from collections import defaultdict


def get_groups_of_3(graph: defaultdict[str, list[str]]) -> set[tuple[str, ...]]:
    groups: set[tuple[str, ...]] = set()

    for node, children in graph.items():
        for c1, c2 in it.combinations(children, 2):
            if c2 in graph[c1]:
                groups.add(tuple(sorted((node, c1, c2))))

    return groups


def only_if_starts_with_t(groups: set[tuple[str, ...]]) -> list[tuple[str, ...]]:
    group_with_t: list[tuple[str, ...]] = []

    for c1, c2, c3 in groups:
        if c1[0] == "t" or c2[0] == "t" or c3[0] == "t":
            group_with_t.append((c1, c2, c3))

    return group_with_t


def main(filename: str) -> None:
    graph: defaultdict[str, list[str]] = defaultdict(list)

    with open(filename, "r") as data:
        for line in data:
            c1, c2 = line.strip().split("-")
            graph[c1].append(c2)
            graph[c2].append(c1)

    print(len(only_if_starts_with_t(get_groups_of_3(graph))))


if __name__ == "__main__":
    main(sys.argv[1])
