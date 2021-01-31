from database import Database
from typing import Dict


def build_bitmap_index_for_months(database: Database) -> Dict[int, int]:
    # Compute a bitmap index for all 12 months.
    # For one sale in January and two sales in February,
    # the result could look like this:
    #
    # bitmap_indexes = {
    #      1: 0b001, # January
    #      2: 0b110, # February
    #      3: 0b000, # March
    #      4: 0b000, # April
    #     ...
    #     12: 0b000, # December
    # }

    # Your code goes here.


    return bitmap_indexes
