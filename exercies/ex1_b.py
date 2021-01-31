from database import inner_join, where_equal, select_attributes, Database, Relation
from ex1_a import natural_join


def your_query(database: Database, year: int, state: str, category: str,) -> Relation:
    # You MUST solve this exercise only with the following functions:
    # - inner_join
    # - natural_join
    # - where_equal
    # - rename_attribute
    # - select_attributes
    #
    # For-loops and other looping constructs are not allowed for this exercise.
    # See the function `example_query_allowed_but_slow` for an example of acceptable use.

    # Your code goes here:

    # relation = ...


    return relation


def example_query_allowed_but_slow(
    database: Database, year: int, state: str, category: str,
) -> Relation:
    # Your goal is to express this query in a form such that it runs much faster.

    # Join relations.
    relation = database["time"]
    relation = inner_join(relation, database["location"])
    relation = inner_join(relation, database["product"])
    relation = natural_join(relation, database["sale"])

    # Filter interesting tuples.
    relation = where_equal(relation, "year", year)
    relation = where_equal(relation, "state", state)
    relation = where_equal(relation, "category", category)

    # Discard unneeded attributes.
    relation = select_attributes(relation, ["price", "quantity"])

    return relation


def example_query_for_loops_not_allowed(
    database: Database, year: int, state: str, category: str,
) -> Relation:
    # This horrible abomination of nested for-loops and if-statements computes the same result.
    # It is only here as an additional example to illustrate the query.

    relation: Relation = []

    for sale in database["sale"]:
        for time in database["time"]:
            for location in database["location"]:
                for product in database["product"]:
                    if sale["time_id"] == time["time_id"]:
                        if sale["location_id"] == location["location_id"]:
                            if sale["product_id"] == product["product_id"]:
                                if time["year"] == year:
                                    if location["state"] == state:
                                        if product["category"] == category:
                                            tup = {
                                                "quantity": sale["quantity"],
                                                "price": product["price"],
                                            }

                                            relation.append(tup)

    return relation
