import json



def first(values):
    return values[0]


def div_round_up(a, b):
    return (a + b - 1) // b


def transpose(columns):
    rows = [list(row) for row in zip(*columns)]
    return rows


class BPTreeNode:
    def __init__(self, keys: list, values: list, is_leaf: bool):
        self._keys = keys
        self._values = values
        self.is_leaf = is_leaf
        self.next_leaf = None

    def to_dict(self):
        values = (
            self._values
            if self.is_leaf
            else [value.to_dict() for value in self._values]
        )
        return {
            "is_leaf": self.is_leaf,
            "keys": self._keys,
            "values": values,
        }

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)


    def find_inclusive(self, key1, key2):

        # Your code for exercise 2 (b) goes here.
        pass


    def find(self, key):
        return self.find_inclusive(key, key)


def _compute_tree_height(num_leaves, m):
    height = 1

    while num_leaves > 1:
        num_leaves = div_round_up(num_leaves, 2 * m + 1)
        height += 1

    return height


def _make_bp_tree_recursive(leaves, m, depth, height):
    if depth == height:
        leaf = leaves.pop()

        minimum = leaf._keys[0]
        maximum = leaf._keys[-1]

        return leaf, minimum, maximum
    else:
        results = [
            _make_bp_tree_recursive(leaves, m, depth + 1, height)
            for _ in range(2 * m + 1)
            if leaves
        ]

        children, minimums, maximums = transpose(results)

        minimum = minimums[0]
        maximum = maximums.pop()
        node = BPTreeNode(keys=maximums, values=children, is_leaf=False)

        return node, minimum, maximum


def make_bp_tree(key_value_pairs, m=10) -> BPTreeNode:
    if not key_value_pairs:
        return BPTreeNode(keys=[], values=[], is_leaf=True)

    key_value_pairs = sorted(key_value_pairs, key=first)

    num_leaves = div_round_up(len(key_value_pairs), 2 * m)

    height = _compute_tree_height(num_leaves, m)

    leaves = []
    for i in range(num_leaves):
        start = i * 2 * m
        end = (i + 1) * 2 * m
        keys, groups = transpose(key_value_pairs[start:end])

        leaves.append(BPTreeNode(keys=keys, values=groups, is_leaf=True))

    for leaf1, leaf2 in zip(leaves, leaves[1:]):
        leaf1.next_leaf = leaf2

    leaves = list(reversed(leaves))

    root, minimum, maximum = _make_bp_tree_recursive(leaves, m, 1, height)

    return root
