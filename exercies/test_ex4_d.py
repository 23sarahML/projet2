from database import generate_database, create_database_sqlite, Database
import sqlite3
from time import perf_counter
from ex4_a import build_bitmap_index_for_months
from ex4_c import build_bitmap_index_for_days
from ex4_d import count_sales_between_dates
import zlib


def test_multi_component_bitmap_index(
    database: Database,
    first_month: int,
    first_day: int,
    last_month: int,
    last_day: int,
    cursor,
):
    print(f"Testing range from {first_month}-{first_day} to {last_month}-{last_day}")

    bitmap_indexes_months = build_bitmap_index_for_months(database)
    bitmap_indexes_days = build_bitmap_index_for_days(database)

    start_time = perf_counter()

    num_sales = count_sales_between_dates(
        bitmap_indexes_months,
        bitmap_indexes_days,
        first_month,
        first_day,
        last_month,
        last_day,
    )

    elapsed_time = perf_counter() - start_time

    print(f"Your query took {elapsed_time*1000:.4f} milliseconds.")

    query = """
    SELECT
        COUNT(*)
    FROM
        sale NATURAL JOIN time
    WHERE
        (
            (:first_month != :last_month) AND
            (
                (time.month == :first_month AND time.day >= :first_day) OR
                (:first_month < time.month AND time.month < :last_month) OR
                (time.month == :last_month AND time.day <= :last_day)
            )
        )
        OR
        (
            :first_month == :last_month AND
            time.month == :first_month AND
            time.day BETWEEN :first_day AND :last_day
        )
    """

    params = {
        "first_month": first_month,
        "last_month": last_month,
        "first_day": first_day,
        "last_day": last_day,
    }

    start_time = perf_counter()

    (expected_num_sales,) = cursor.execute(query, params).fetchone()

    elapsed_time = perf_counter() - start_time

    print(f"SQL query took {elapsed_time*1000:.4f} milliseconds.\n")

    if num_sales != expected_num_sales:
        raise ValueError(
            f"The number of sales between months {first_month} "
            f"and {last_month} should have been {expected_num_sales}, "
            f"but you computed {num_sales}"
        )


def test_multi_component_bitmap_index_multiple():
    database = generate_database()

    conn = sqlite3.connect(":memory:")

    create_database_sqlite(database, conn)

    cursor = conn.cursor()

    for first_month, first_day, last_month, last_day in [
        (1, 1, 12, 31),
        (1, 1, 1, 1),
        (12, 31, 12, 31),
        (2, 3, 11, 27),
        (2, 1, 11, 31),
        (5, 7, 5, 23),
        (5, 1, 5, 2),
        (3, 30, 3, 31),
        (12, 30, 12, 31),
        (12, 1, 12, 31),
    ]:
        test_multi_component_bitmap_index(
            database, first_month, first_day, last_month, last_day, cursor
        )

    print(
        "For comparison, our multi-component bitmap index query"
        "took up to 2.5 milliseconds and the SQL query took "
        "55 milliseconds on our test computer."
    )


def check_if_file_has_been_modified():
    with open(__file__, "rb") as f:
        if zlib.crc32(f.read()) != 0:
            raise ValueError("You are not allowed to modify " + __file__)


if __name__ == "__main__":
    check_if_file_has_been_modified()
    test_multi_component_bitmap_index_multiple()

# 104505678
