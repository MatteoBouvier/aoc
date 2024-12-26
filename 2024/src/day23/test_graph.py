from day23.part2 import get_groups


def test_2_nodes():
    graph = {1: [2], 2: [1]}

    groups = get_groups(graph)
    assert groups == {(1, 2)}


def test_3_nodes():
    graph = {1: [2, 3], 2: [1, 3], 3: [1, 2]}

    groups = get_groups(graph)
    assert groups == {(1, 2, 3)}


def test_2_groups_sep():
    graph = {1: [2, 3], 2: [1, 3], 3: [1, 2], 4: [5], 5: [4]}

    groups = get_groups(graph)
    assert groups == {(1, 2, 3), (4, 5)}


def test_2_groups_near():
    graph = {1: [2, 3], 2: [1, 3], 3: [1, 2, 4], 4: [3, 5], 5: [4]}

    groups = get_groups(graph)
    assert groups == {(1, 2, 3), (4, 5)}
