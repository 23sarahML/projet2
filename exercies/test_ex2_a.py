from ex2_bp_tree import make_bp_tree
import random

random.seed(0)
# Your code goes here.
# This is the only test file that you are allowed to modify.



def test_min():
    # Test if the smallest value is at the expected position in the B+ tree.
    # This is just an example test.
    # "Unfortunately", the test passes, so there must be a different issue.

    key_value_pairs = [
        (4, "value4"),
        (2, "value2"),
        (1, "value1"),
        (3, "value3"),
    ]
    node = make_bp_tree(key_value_pairs, m=2)

    # Walk to first leaf.
    while not node.is_leaf:
        node = node._values[0]
    # Retrieve the value corresponding to the smallest key.
    value = node._values[0]

    print(f"The value corresponding to the smallest key is {value}")

    assert value == "value1"

    print("Test passed.")


if __name__ == "__main__":
    test_min()
    # Add more tests here.


# 131854520
