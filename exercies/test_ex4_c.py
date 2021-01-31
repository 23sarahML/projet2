from database import Database
from ex4_c import build_bitmap_index_for_days
import zlib


def test_bitmap_index():
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

    bitmap_indexes = build_bitmap_index_for_days(database)

    expected_bitmap_indexes = {
        1: 0b100,
        2: 0b010,
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
        13: 0b000,
        14: 0b000,
        15: 0b000,
        16: 0b000,
        17: 0b000,
        18: 0b000,
        19: 0b000,
        20: 0b000,
        21: 0b000,
        22: 0b000,
        23: 0b000,
        24: 0b000,
        25: 0b000,
        26: 0b000,
        27: 0b000,
        28: 0b000,
        29: 0b000,
        30: 0b000,
        31: 0b001,
    }

    print("Your bitmap index:\n")
    for day in range(1, 32):
        if day not in bitmap_indexes:
            raise ValueError("Your bitmap index is missing day {day}")

        print(f"day {day:2d}: 0b{bitmap_indexes[day]:03b}")
    print()

    print("Expected bitmap index:\n")
    for day in range(1, 32):
        print(f"day {day:2d}: 0b{expected_bitmap_indexes[day]:03b}")
    print()

    for day in range(1, 32):
        if bitmap_indexes[day] != expected_bitmap_indexes[day]:
            raise ValueError(f"Bits for day {day} are different")

    print("Index OK.")


def check_if_file_has_been_modified():
    with open(__file__, "rb") as f:
        if zlib.crc32(f.read()) != 0:
            raise ValueError("You are not allowed to modify " + __file__)


if __name__ == "__main__":
    check_if_file_has_been_modified()
    test_bitmap_index()

# 1620442107
