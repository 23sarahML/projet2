from database import generate_database, create_database_sqlite, Database
import sqlite3
from typing import Dict
from time import perf_counter
from ex4_a import build_bitmap_index_for_months
from ex4_b import count_sales_between_months
import zlib


def test_bitmap_index_for_months(
    cursor,
    bitmap_indexes: Dict[int, int],
    first_month: int,
    last_month: int,
):
    start_time = perf_counter()

    num_sales = count_sales_between_months(bitmap_indexes, first_month, last_month)

    elapsed_time = perf_counter() - start_time

    print(f"Your query took {elapsed_time*1000:.4f} milliseconds.")

    start_time = perf_counter()

    query = """
    SELECT
        COUNT(*)
    FROM
        sale NATURAL JOIN time
    WHERE
        time.month BETWEEN ? AND ?
    """

    (expected_num_sales,) = cursor.execute(query, (first_month, last_month)).fetchone()

    elapsed_time = perf_counter() - start_time

    print(f"SQL query took {elapsed_time*1000:.4f} milliseconds.\n")

    if num_sales != expected_num_sales:
        raise ValueError(
            f"The number of sales between months {first_month} "
            f"and {last_month} should have been {expected_num_sales}, "
            "but you computed {num_sales}"
        )

    print(
        "For comparison, our bitmap index query "
        "took 0.6 milliseconds and the SQL query "
        "took 50 milliseconds on our test computer.\n"
    )


def test_bitmap_index():
    database: Database = generate_database()

    conn = sqlite3.connect(":memory:")

    cursor = conn.cursor()

    create_database_sqlite(database, conn)

    bitmap_indexes = build_bitmap_index_for_months(database)

    for first_month in range(1, 10):
        last_month = first_month + 3

        test_bitmap_index_for_months(cursor, bitmap_indexes, first_month, last_month)


def check_if_file_has_been_modified():
    with open(__file__, "rb") as f:
        if zlib.crc32(f.read()) != 0:
            raise ValueError("You are not allowed to modify " + __file__)


if __name__ == "__main__":
    check_if_file_has_been_modified()
    test_bitmap_index()

# 4199618693
