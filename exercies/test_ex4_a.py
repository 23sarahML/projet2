from database import Database
from ex4_a import build_bitmap_index_for_months
import zlib


def test_bitmap_index():
    database: Database = {
        "time": [
            {"time_id": 0, "month": 1},
            {"time_id": 1, "month": 2},
        ],
        "sale": [
            {"time_id": 0},
            {"time_id": 1},
            {"time_id": 1},
        ],
    }

    bitmap_indexes = build_bitmap_index_for_months(database)

    expected_bitmap_indexes = {
        1: 0b001,
        2: 0b110,
        3: 0b000,
        4: 0b000,
        5: 0b000,
        6: 0b000,
        7: 0b000,
        8: 0b000,
        9: 0b000,
        10: 0b000,
        11: 0b000,
        12: 0b000,
    }

    print("Your bitmap index:\n")
    for month in range(1, 13):
        if month not in bitmap_indexes:
            raise ValueError("Your bitmap index is missing month {month}")

        print(f"month {month:2d}: 0b{bitmap_indexes[month]:03b}")
    print()

    print("Expected bitmap index:\n")
    for month in range(1, 13):
        print(f"month {month:2d}: 0b{expected_bitmap_indexes[month]:03b}")
    print()

    for month in range(1, 13):
        if bitmap_indexes[month] != expected_bitmap_indexes[month]:
            raise ValueError(f"Bits for month {month} are different")

    print("Index OK.")


def check_if_file_has_been_modified():
    with open(__file__, "rb") as f:
        if zlib.crc32(f.read()) != 0:
            raise ValueError("You are not allowed to modify " + __file__)


if __name__ == "__main__":
    check_if_file_has_been_modified()
    test_bitmap_index()

# 1494769429
