from time import perf_counter
from ex2_bp_tree import make_bp_tree
import random
import zlib

random.seed(0)


def test_find_inclusive_simple():
    key_value_pairs = [
        (1, "value1"),
        (2, "value2"),
        (3, "value3"),
        (3, "value3again"),
        (4, "value4"),
    ]

    root = make_bp_tree(key_value_pairs, m=1)

    values = list(root.find_inclusive(2, 3))

    expected_values = ["value2", "value3", "value3again"]

    check_lists(values, expected_values)


def test_find_inclusive(n: int, m: int):
    key_value_pairs = []

    for _ in range(n):
        key = random.randrange(100)
        value = random.randrange(100)

        key_value_pairs.append((key, value))

    root = make_bp_tree(key_value_pairs, m=m)

    key_value_pairs.sort(key=lambda values: values[0])

    # Test a few key ranges
    for _ in range(10):
        key1 = random.choice(key_value_pairs)[0]
        key2 = random.choice(key_value_pairs)[0]

        # Ensure that key1 <= key2
        if key1 > key2:
            key2, key1 = key1, key2

        values = list(root.find_inclusive(key1, key2))

        expected_values = [
            value for key, value in key_value_pairs if key1 <= key <= key2
        ]

        check_lists(values, expected_values)


def test_find_inclusive_large():
    key_value_pairs = []

    for _ in range(1_000_000):
        key = random.randrange(1_000_000)
        value = random.randrange(1_000_000)

        key_value_pairs.append((key, value))

    root = make_bp_tree(key_value_pairs, m=20)

    key_value_pairs.sort(key=lambda values: values[0])

    key1 = 250_000
    key2 = 750_000

    start_time: float = perf_counter()

    values = list(root.find_inclusive(key1, key2))

    elapsed_time: float = perf_counter() - start_time

    print(f"Your query took {elapsed_time:.4f} seconds.")
    print("For comparison, it took 0.2 seconds on our test computer.")

    expected_values = [value for key, value in key_value_pairs if key1 <= key <= key2]

    check_lists(values, expected_values)


def check_lists(values: list, expected_values: list):
    if len(values) != len(expected_values):
        raise ValueError(
            f"Expected {len(expected_values)} ({expected_values}), but got {len(values)} ({values})"
        )

    for index in range(len(values)):
        value = values[index]
        expected_value = expected_values[index]

        if value != expected_value:
            raise ValueError(
                f"Expected value {expected_value} at index {index}, but got {value} instead.\nExpected list:\n    {expected_values}\nActual list:\n    {values}"
            )


def check_if_file_has_been_modified():
    with open(__file__, "rb") as f:
        if zlib.crc32(f.read()) != 0:
            raise ValueError("You are not allowed to modify " + __file__)


if __name__ == "__main__":
    check_if_file_has_been_modified()
    test_find_inclusive_simple()

    for n in range(1, 10):
        for m in range(1, 10):
            test_find_inclusive(n, m)

    test_find_inclusive_large()

# 0319601298
