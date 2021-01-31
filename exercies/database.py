import datetime
import random
from typing import Dict, List, Set, Union, Iterable

IntOrStrOrFloat = Union[int, str, float]
RelationTuple = Dict[str, IntOrStrOrFloat]
Relation = List[RelationTuple]
Database = Dict[str, Relation]

random.seed(0)


def generate_database() -> Database:
    # This project implements a very simple database in Python.
    # The data is stored in a Dict of Lists.
    # The lists represent the relations.
    # The relations contain Dicts which represent the tuples.
    # For simplicity, the attribute names are stored as the Dict keys.
    # A real database would of course only store the attribute names only once.
    #
    # What follows is an example.
    # This data will be cleared and replaced with pseudo-random data.
    database: Database = {
        "time": [
            {
                "time_id": 1,
                "year": 2020,
                "month": 12,
                "day": 31,
                "timestamp": 1_609_372_800,
            },
        ],
        "location": [
            {
                "location_id": 2,
                "state": "North Rhine-Westphalia",
                "district": "Bilk",
                "city": "Düsseldorf",
                "latitude": 51201499,
                "longitude": 6774496,
            },
        ],
        "product": [
            {
                "product_id": 3,
                "name": "1500 Ladybugs",
                "category": "Patio, Lawn & Garden",
                "subcategory": "Beneficial Insects",
                "price": 8.99,
            },
        ],
        "sale": [
            {
                "sale_id": 0,
                "time_id": 1,
                "location_id": 2,
                "product_id": 3,
                "quantity": 667,
            },
        ],
        "campaign": [
            {
                "campaign_id": 0,
                "start": 1_609_372_800,
                "end": 1_609_459_200,
            },
        ],
    }

    # clear example data
    relation: Relation
    for relation in database.values():
        relation.clear()

    # generate time
    time_id: int
    for time_id in range(100_000):
        timestamp: int = random.randrange(1_262_304_000, 1_609_459_200)

        date: datetime.datetime = datetime.datetime.utcfromtimestamp(timestamp)

        time: RelationTuple = {
            "time_id": time_id,
            "year": date.year,
            "month": date.month,
            "day": date.day,
            "timestamp": timestamp,
        }

        database["time"].append(time)

    # generate unique coordinates (latitude/longitude pairs)
    coordinates = []
    for _ in range(100_000):
        latitude = random.randint(41165700, 61165700)
        longitude = random.randint(5451500, 20451500)
        coordinates.append((latitude, longitude))

    # generate locations
    location_id: int
    for location_id in range(100_000):
        latitude, longitude = coordinates[location_id]

        location: RelationTuple = {
            "location_id": location_id,
            "state": f"state_{random.randrange(10)}",
            "district": f"district_{random.randrange(10)}",
            "city": f"city_{random.randrange(10)}",
            "latitude": latitude,
            "longitude": longitude,
        }

        database["location"].append(location)

    # generate products
    product_id: int
    for product_id in range(1_000):

        product: RelationTuple = {
            "product_id": product_id,
            "name": f"name_{random.randrange(10)}",
            "category": f"category_{random.randrange(10)}",
            "subcategory": f"subcategory_{random.randrange(10)}",
            "price": random.randrange(1_000) + 0.99,
        }

        database["product"].append(product)

    # generate sales
    sale_id: int
    for sale_id in range(100_000):
        time_id = random.choice(database["time"])["time_id"]
        location_id = random.choice(database["location"])["location_id"]
        product_id = random.choice(database["product"])["product_id"]

        sale: RelationTuple = {
            "sale_id": sale_id,
            "time_id": time_id,
            "location_id": location_id,
            "product_id": product_id,
            "quantity": random.randint(1, 100),
        }

        database["sale"].append(sale)

    # generate ad campaigns
    campaign_id: int
    for campaign_id in range(1_000):
        timestamp_start: int = random.randrange(1_262_304_000, 1_609_459_200)
        duration: int = random.randrange(86_400 * 7)
        timestamp_end: int = timestamp_start + duration

        campaign: RelationTuple = {
            "campaign_id": campaign_id,
            "timestamp_start": timestamp_start,
            "timestamp_end": timestamp_end,
        }

        database["campaign"].append(campaign)

    return database


def create_database_sqlite(database, connection):
    with connection:
        cursor = connection.cursor()

        cursor.execute(
            """
        CREATE TABLE time (
            time_id INTEGER PRIMARY KEY NOT NULL,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            timestamp INTEGER NOT NULL
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE location (
            location_id INTEGER PRIMARY KEY NOT NULL,
            state TEXT NOT NULL,
            city TEXT NOT NULL,
            district TEXT NOT NULL,
            latitude INTEGER NOT NULL,
            longitude INTEGER NOT NULL
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE product (
            product_id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT NOT NULL,
            price REAL NOT NULL
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE sale (
            sale_id INTEGER PRIMARY KEY NOT NULL,
            time_id INTEGER NOT NULL,
            location_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE campaign (
            campaign_id INTEGER PRIMARY KEY NOT NULL,
            timestamp_start INTEGER NOT NULL,
            timestamp_end INTEGER NOT NULL
        )
        """
        )

        queries = {
            "time": "INSERT INTO time (time_id, year, month, day, timestamp) VALUES (?, ?, ?, ?, ?)",
            "location": "INSERT INTO location (location_id, state, city, district, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
            "product": "INSERT INTO product (product_id, name, category, subcategory, price) VALUES (?, ?, ?, ?, ?)",
            "sale": "INSERT INTO sale (sale_id, time_id, location_id, product_id, quantity) VALUES (?, ?, ?, ?, ?)",
            "campaign": "INSERT INTO campaign (campaign_id, timestamp_start, timestamp_end) VALUES (?, ?, ?)",
        }

        attributes = {
            "time": ("time_id", "year", "month", "day", "timestamp"),
            "location": (
                "location_id",
                "state",
                "city",
                "district",
                "latitude",
                "longitude",
            ),
            "product": ("product_id", "name", "category", "subcategory", "price"),
            "sale": ("sale_id", "time_id", "location_id", "product_id", "quantity"),
            "campaign": ("campaign_id", "timestamp_start", "timestamp_end"),
        }

        for relation_name, relation in database.items():
            tuples = [
                tuple(tup[attribute] for attribute in attributes[relation_name])
                for tup in relation
            ]

            cursor.executemany(queries[relation_name], tuples)


def inner_join(relation1: Relation, relation2: Relation) -> Relation:
    result_relation: Relation = []

    tuple1: RelationTuple
    for tuple1 in relation1:
        tuple2: RelationTuple
        for tuple2 in relation2:
            common_attributes: Set[str] = set(tuple1.keys()) & set(tuple2.keys())

            if len(common_attributes) > 0:
                raise ValueError(
                    "This inner_join implementation only supports relations where all attributes have different names."
                )

            # Combine both tuples
            result_tuple: RelationTuple = dict(tuple1)
            result_tuple.update(tuple2)

            # Add the combined tuple to the resulting relation
            result_relation.append(result_tuple)

    return result_relation


def where_equal(
    relation1: Relation, attribute_name: str, attribute_value: IntOrStrOrFloat
) -> Relation:
    # Only keep tuples where a given attribute has a given value.

    result_relation: Relation = []

    tup: RelationTuple
    for tup in relation1:
        if tup[attribute_name] == attribute_value:
            result_relation.append(tup)

    return result_relation


def select_attributes(relation1: Relation, attributes: Iterable) -> Relation:
    # Only keep some attributes.

    result_relation: Relation = []

    tup: RelationTuple
    for tup in relation1:
        tup = dict((attribute, tup[attribute]) for attribute in attributes)
        result_relation.append(tup)

    return result_relation


def rename_attribute(
    relation1: Relation, old_attribute_name: str, new_attribute_name: str
) -> Relation:
    # Only keep some attributes.

    result_relation: Relation = []

    tup: RelationTuple
    for tup in relation1:
        tup = dict(
            (
                attribute if attribute != old_attribute_name else new_attribute_name,
                value,
            )
            for attribute, value in tup.items()
        )
        result_relation.append(tup)

    return result_relation
