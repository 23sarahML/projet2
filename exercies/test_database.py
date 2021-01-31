from database import (
    Relation,
    RelationTuple,
    where_equal,
    inner_join,
    select_attributes,
    rename_attribute,
)
from typing import Set, Any
import zlib


def is_approximately_equal(actual_value: Any, expected_value: Any) -> bool:
    type1 = type(actual_value)
    type2 = type(expected_value)

    if type1 != type2:
        return False

    if isinstance(actual_value, dict):
        keys1 = set(actual_value.keys())
        keys2 = set(expected_value.keys())

        if keys1 != keys2:
            return False

        return all(
            is_approximately_equal(actual_value[key], expected_value[key])
            for key in keys2
        )

    elif isinstance(actual_value, list):
        if len(actual_value) != len(expected_value):
            return False

        return all(
            is_approximately_equal(a, b) for a, b in zip(actual_value, expected_value)
        )

    elif isinstance(actual_value, float):
        return abs(actual_value - float(expected_value)) < 0.001

    elif isinstance(actual_value, int):
        return actual_value == expected_value
    elif isinstance(actual_value, bool):
        return actual_value == expected_value
    elif isinstance(actual_value, str):
        return actual_value == expected_value
    else:
        raise NotImplementedError(
            f"Equality check for objects of type {type1} not implemented."
        )


def check_relations_equal(relation: Relation, expected_relation: Relation):
    if len(relation) != len(expected_relation):
        raise ValueError(
            f"The relation has {len(relation)} tuples, but should have {len(expected_relation)} tuples instead."
        )

    if len(expected_relation) == 0:
        return

    expected_attributes: Set[str] = set(expected_relation[0].keys())

    found: Relation = list(expected_relation)

    tuple1: RelationTuple
    for tuple1 in relation:
        attributes = set(tuple1.keys())

        if attributes != expected_attributes:
            raise ValueError(
                f"A tuple in a relation has attributes {attributes}, but should have {expected_attributes} instead."
            )

        for i, tuple2 in enumerate(found):
            if is_approximately_equal(tuple1, tuple2):
                del found[i]
                break
        else:
            raise ValueError(f"Tuple {tuple1} should not appear in relation.")


def test_where_equal():
    input_relation: Relation = [
        {"x": 1},
        {"x": 2},
        {"x": 3},
    ]

    expected_relation: Relation = [
        {"x": 2},
    ]

    result_relation: Relation = where_equal(input_relation, "x", 2)

    check_relations_equal(result_relation, expected_relation)


def test_inner_join():
    input_relation1: Relation = [
        {"a": 1},
        {"a": 2},
    ]

    input_relation2: Relation = [
        {"b": 3},
        {"b": 4},
    ]

    expected_relation: Relation = [
        {"a": 1, "b": 3},
        {"a": 1, "b": 4},
        {"a": 2, "b": 3},
        {"a": 2, "b": 4},
    ]

    result_relation: Relation = inner_join(input_relation1, input_relation2)

    check_relations_equal(result_relation, expected_relation)


def test_select_attributes():
    input_relation: Relation = [
        {"a": 1, "b": 2, "c": 3, "d": 4},
        {"a": 5, "b": 6, "c": 7, "d": 8},
    ]

    expected_relation: Relation = [
        {"a": 1, "c": 3},
        {"a": 5, "c": 7},
    ]

    result_relation: Relation = select_attributes(input_relation, ["a", "c"])

    check_relations_equal(result_relation, expected_relation)


def test_rename_attribute():
    input_relation: Relation = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
    ]

    expected_relation: Relation = [
        {"a": 1, "c": 2},
        {"a": 3, "c": 4},
    ]

    result_relation: Relation = rename_attribute(input_relation, "b", "c")

    check_relations_equal(result_relation, expected_relation)


def check_if_file_has_been_modified():
    with open(__file__, "rb") as f:
        if zlib.crc32(f.read()) != 0:
            raise ValueError("You are not allowed to modify " + __file__)


if __name__ == "__main__":
    check_if_file_has_been_modified()
    test_where_equal()
    test_inner_join()
    test_select_attributes()
    test_rename_attribute()
    print("Database tests passed :)")

# 3670945733
