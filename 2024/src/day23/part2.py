import sys
import itertools as it
from collections import defaultdict


def get_groups(graph: defaultdict[str, list[str]]) -> set[tuple[str, ...]]:
    groups: set[tuple[str, ...]] = set()

    for node, children in graph.items():
        group = [node]
        for child in children:
            if all(child in graph[group_node] for group_node in group):
                group.append(child)

        groups.add(tuple(sorted(group)))

    return groups


def main(filename: str) -> None:
    graph: defaultdict[str, list[str]] = defaultdict(list)

    with open(filename, "r") as data:
        for line in data:
            c1, c2 = line.strip().split("-")
            graph[c1].append(c2)
            graph[c2].append(c1)

    groups = get_groups(graph)
    largest = ()
    for group in groups:
        if len(group) > len(largest):
            largest = group

    print(",".join(largest), len(largest))


if __name__ == "__main__":
    main(sys.argv[1])
