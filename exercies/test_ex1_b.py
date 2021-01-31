from database import (
    generate_database,
    Database,
    Relation,
    RelationTuple,
    create_database_sqlite,
)
from time import perf_counter
from test_database import check_relations_equal
import sqlite3
import ex1_b
import zlib


def test_your_query():
    database: Database = generate_database()

    sale: RelationTuple = database["sale"][-1]
    year: int = database["time"][sale["time_id"]]["year"]
    state: str = database["location"][sale["location_id"]]["state"]
    category: str = database["product"][sale["product_id"]]["category"]

    expected_relation: Relation = compute_expected_relation(
        database, year, state, category
    )

    start_time: float = perf_counter()

    # The example queries will run out of memory or take months to complete.
    # relation = ex1_b.example_query_allowed_but_slow(database, year, state, category)
    # relation = ex1_b.example_query_for_loops_not_allowed(database, year, state, category)

    relation: Relation = ex1_b.your_query(database, year, state, category)

    elapsed_time: float = perf_counter() - start_time

    check_relations_equal(relation, expected_relation)

    print(f"Your query took {elapsed_time:.4f} seconds.\n")
    print(
        "For comparison, the SQL query took 0.05 seconds and the Python query took 0.17 seconds on our test computer."
    )


def compute_expected_relation(
    database: Database, year: int, state: str, category: str,
) -> Relation:
    connection = sqlite3.connect(":memory:")

    create_database_sqlite(database, connection)

    query = """
    SELECT
        product.price,
        sale.quantity
    FROM
        sale,
        time,
        product,
        location
    WHERE
        sale.time_id = time.time_id AND
        sale.product_id = product.product_id AND
        sale.location_id = location.location_id AND
        time.year = ? AND
        location.state = ? AND
        product.category = ?
    """

    start_time = perf_counter()

    relation: Relation = []

    with connection:
        cursor = connection.cursor()

        for price, quantity in cursor.execute(query, (year, state, category)):
            tup = {
                "price": price,
                "quantity": quantity,
            }
            relation.append(tup)

    elapsed_time = perf_counter() - start_time

    print(f"For comparison, the SQL query took {elapsed_time:.4f} seconds.\n")

    return relation


def check_if_file_has_been_modified():
    with open(__file__, "rb") as f:
        if zlib.crc32(f.read()) != 0:
            raise ValueError("You are not allowed to modify " + __file__)


if __name__ == "__main__":
    check_if_file_has_been_modified()
    test_your_query()

# 8336964854
