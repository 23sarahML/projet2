from ex1_a import natural_join
from database import (
    generate_database,
    Relation,
    Database,
    create_database_sqlite,
    where_equal,
)
from test_database import check_relations_equal
from time import perf_counter
import sqlite3
import zlib


def test_natural_join_disjunct_attributes():
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

    result_relation: Relation = natural_join(input_relation1, input_relation2)

    check_relations_equal(result_relation, expected_relation)


def test_natural_join_common_attributes():
    input_relation1: Relation = [
        {"a": 0, "b": 2},
        {"a": 1, "b": 3},
        {"a": 2, "b": 4},
    ]

    input_relation2: Relation = [
        {"b": 3, "c": 5},
        {"b": 4, "c": 6},
        {"b": 4, "c": 7},
        {"b": 5, "c": 8},
    ]

    expected_relation: Relation = [
        {"a": 1, "b": 3, "c": 5},
        {"a": 2, "b": 4, "c": 6},
        {"a": 2, "b": 4, "c": 7},
    ]

    result_relation: Relation = natural_join(input_relation1, input_relation2)

    check_relations_equal(result_relation, expected_relation)


def test_natural_join_empty_relation():
    empty_relation: Relation = []

    not_empty_relation: Relation = [
        {"a": 0, "b": 2},
        {"a": 1, "b": 3},
        {"a": 2, "b": 4},
    ]

    empty_not_empty_result: Relation = natural_join(empty_relation, not_empty_relation)
    not_empty_empty_result: Relation = natural_join(not_empty_relation, empty_relation)
    empty_empty_result: Relation = natural_join(empty_relation, empty_relation)

    check_relations_equal(empty_not_empty_result, [])
    check_relations_equal(not_empty_empty_result, [])
    check_relations_equal(empty_empty_result, [])


def compute_expected_relation(database: Database) -> Relation:
    connection = sqlite3.connect(":memory:")

    create_database_sqlite(database, connection)

    query = """
    SELECT
        sale.sale_id,
        sale.time_id,
        sale.location_id,
        sale.product_id,
        sale.quantity,
        product.name,
        product.category,
        product.subcategory,
        product.price
    FROM
        sale,
        product
    WHERE
        sale.product_id = product.product_id
    """

    start_time: float = perf_counter()

    relation: Relation = []

    with connection:
        cursor = connection.cursor()

        attributes = [
            "sale_id",
            "time_id",
            "location_id",
            "product_id",
            "quantity",
            "name",
            "category",
            "subcategory",
            "price",
        ]

        for tup in cursor.execute(query):

            relation.append(dict(zip(attributes, tup)))

    elapsed_time: float = perf_counter() - start_time

    print(f"For comparison, the SQL query took {elapsed_time:.4f} seconds.")

    return relation


def test_natural_join_large():
    database: Database = generate_database()

    start_time: float = perf_counter()

    relation: Relation = natural_join(database["sale"], database["product"])

    elapsed_time: float = perf_counter() - start_time

    print(
        f"Your natural_join implementation took {elapsed_time:.4f} seconds for the large test.\n"
    )

    expected_relation = compute_expected_relation(database)

    print(
        "On our test computer, the timing results are 0.2 seconds and 0.35 seconds respectively."
    )

    # Discard all but some products to make this test run faster.
    relation = where_equal(relation, "quantity", 1)
    expected_relation = where_equal(expected_relation, "quantity", 1)

    check_relations_equal(relation, expected_relation)


def check_if_file_has_been_modified():
    with open(__file__, "rb") as f:
        if zlib.crc32(f.read()) != 0:
            raise ValueError("You are not allowed to modify " + __file__)


if __name__ == "__main__":
    check_if_file_has_been_modified()
    test_natural_join_disjunct_attributes()
    test_natural_join_common_attributes()
    test_natural_join_empty_relation()
    test_natural_join_large()

# 7760159956
