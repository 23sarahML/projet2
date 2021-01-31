from database import Database
from ex4_e import build_bitmap_index_for_months_range_coded
from ex4_e import build_bitmap_index_for_days_range_coded
import zlib


def test_range_coded_bitmap_index_for_months():
    print("Testing range-coded bitmap index for months.\n")

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

    bitmap_indexes = build_bitmap_index_for_months_range_coded(database)

    expected_bitmap_indexes = {
        1: 0b001,
        2: 0b111,
        3: 0b111,
        4: 0b111,
        5: 0b111,
        6: 0b111,
        7: 0b111,
        8: 0b111,
        9: 0b111,
        10: 0b111,
        11: 0b111,
    }

    print("Your bitmap index:\n")
    for month in range(1, 12):
        if month not in bitmap_indexes:
            raise ValueError("Your bitmap index is missing month {month}")

        print(f"month {month:2d}: 0b{bitmap_indexes[month]:03b}")
    print()

    print("Expected bitmap index:\n")
    for month in range(1, 12):
        print(f"month {month:2d}: 0b{expected_bitmap_indexes[month]:03b}")
    print()

    for month in range(1, 12):
        if bitmap_indexes[month] != expected_bitmap_indexes[month]:
            raise ValueError(f"Bits for month {month} are different")

    print("Range-coded bitmap index for months OK.")


def test_range_coded_bitmap_index_for_days():
    print("Testing range-coded bitmap index for days.\n")

    database: Database = {
        "time": [
            {"time_id": 0, "day": 1},
            {"time_id": 1, "day": 2},
            {"time_id": 2, "day": 31},
        ],
        "sale": [
            {"time_id": 2},
            {"time_id": 1},
            {"time_id": 0},
        ],
    }

    bitmap_indexes = build_bitmap_index_for_days_range_coded(database)

    expected_bitmap_indexes = {
        1: 0b100,
        2: 0b110,
        3: 0b110,
        4: 0b110,
        5: 0b110,
        6: 0b110,
        7: 0b110,
        8: 0b110,
        9: 0b110,
        10: 0b110,
        11: 0b110,
        12: 0b110,
        13: 0b110,
        14: 0b110,
        15: 0b110,
        16: 0b110,
        17: 0b110,
        18: 0b110,
        19: 0b110,
        20: 0b110,
        21: 0b110,
        22: 0b110,
        23: 0b110,
        24: 0b110,
        25: 0b110,
        26: 0b110,
        27: 0b110,
        28: 0b110,
        29: 0b110,
        30: 0b110,
    }

    print("Your bitmap index:\n")
    for day in range(1, 31):
        if day not in bitmap_indexes:
            raise ValueError("Your bitmap index is missing day {day}")

        print(f"day {day:2d}: 0b{bitmap_indexes[day]:03b}")
    print()

    print("Expected bitmap index:\n")
    for day in range(1, 31):
        print(f"day {day:2d}: 0b{expected_bitmap_indexes[day]:03b}")
    print()

    for day in range(1, 31):
        if bitmap_indexes[day] != expected_bitmap_indexes[day]:
            raise ValueError(f"Bits for day {day} are different")

    print("Range-coded bitmap index for days OK.")


def check_if_file_has_been_modified():
    with open(__file__, "rb") as f:
        if zlib.crc32(f.read()) != 0:
            raise ValueError("You are not allowed to modify " + __file__)


if __name__ == "__main__":
    check_if_file_has_been_modified()
    test_range_coded_bitmap_index_for_months()
    test_range_coded_bitmap_index_for_days()

# 6579951223
