from database import (
    generate_database,
    Database,
    create_database_sqlite,
)
import sqlite3
from time import perf_counter
from ex2_c import compute_campaign_revenue
import zlib


def test_campaign_revenue():
    database: Database = generate_database()

    start_time: float = perf_counter()

    revenue: float = compute_campaign_revenue(database)

    elapsed_time: float = perf_counter() - start_time

    print(f"Your query took {elapsed_time:.4f} seconds.\n")

    connection = sqlite3.connect(":memory:")

    create_database_sqlite(database, connection)

    query = """
    SELECT
        SUM(product.price * sale.quantity)
    FROM
        sale,
        time,
        product
    WHERE
        sale.time_id = time.time_id AND
        sale.product_id = product.product_id AND
        EXISTS (
            SELECT * FROM campaign WHERE
                campaign.timestamp_start <= time.timestamp AND
                time.timestamp <= campaign.timestamp_end
        )
    """

    start_time: float = perf_counter()

    with connection:
        cursor = connection.cursor()

        result = cursor.execute(query).fetchone()

        expected_revenue: float = result[0]

    if abs(revenue - expected_revenue) > 0.01:
        raise ValueError(
            f"You computed a revenue of {revenue}, but the value should have been {expected_revenue}."
        )

    elapsed_time: float = perf_counter() - start_time

    print(f"The SQL query took {elapsed_time:.4f} seconds.\n")
    print(
        "For comparison, our Python implementation took 0.3 seconds and the SQL query took 7 seconds on our test computer."
    )


def check_if_file_has_been_modified():
    with open(__file__, "rb") as f:
        if zlib.crc32(f.read()) != 0:
            raise ValueError("You are not allowed to modify " + __file__)


if __name__ == "__main__":
    check_if_file_has_been_modified()
    test_campaign_revenue()

# 2234642543
