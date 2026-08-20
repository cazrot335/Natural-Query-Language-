from main import parse_query
from query.sql_generator import generate_sql


# --------------------------------
# Helper
# --------------------------------

def run_query(query):

    parsed = parse_query(query)

    sql = generate_sql(parsed)

    return parsed, sql


# --------------------------------
# 1. Basic SELECT
# --------------------------------

def test_basic_select():

    parsed, sql = run_query(
        "Show students"
    )

    assert parsed["intent"] == "SELECT"
    assert parsed["table"] == "students"

    assert sql == (
        "SELECT * FROM students;"
    )


# --------------------------------
# 2. Field selection
# --------------------------------

def test_field_selection():

    parsed, sql = run_query(
        "Show car model and daily rate for rentals"
    )

    assert parsed["table"] == "rentals"

    assert parsed["fields"] == [
        "car_model",
        "daily_rate"
    ]

    assert sql == (
        "SELECT car_model, daily_rate "
        "FROM rentals;"
    )


# --------------------------------
# 3. Single condition
# --------------------------------

def test_single_condition():

    parsed, sql = run_query(
        "Show students with marks above 80"
    )

    assert parsed["conditions"] == [
        {
            "field": "marks",
            "operator": ">",
            "value": 80,
            "connector": None
        }
    ]

    assert sql == (
    "SELECT * FROM students "
    "WHERE marks > 80;"
)


# --------------------------------
# 4. Multiple AND conditions
# --------------------------------

def test_and_conditions():

    parsed, sql = run_query(
        "Show students with marks above 80 "
        "and age below 25"
    )

    assert len(
        parsed["conditions"]
    ) == 2

    assert (
        parsed["conditions"][1]["connector"]
        == "AND"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE (marks > 80 AND age < 25);"
    )


# --------------------------------
# 5. OR condition
# --------------------------------

def test_or_condition():

    parsed, sql = run_query(
        "Show students with marks above 90 "
        "or age below 18"
    )

    assert (
        parsed["conditions"][1]["connector"]
        == "OR"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE (marks > 90 OR age < 18);"
    )


# --------------------------------
# 6. AND / OR precedence
# --------------------------------

def test_boolean_precedence():

    parsed, sql = run_query(
        "Show students with marks above 90 "
        "or age below 18 "
        "and marks above 50"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE "
        "(marks > 90 OR (age < 18 AND marks > 50));"
    )


# --------------------------------
# 7. ORDER BY
# --------------------------------

def test_ordering():

    parsed, sql = run_query(
        "Show rentals ordered by daily rate descending"
    )

    assert parsed["order_by"] == {
        "field": "daily_rate",
        "direction": "DESC"
    }

    assert sql == (
    "SELECT * FROM rentals "
    "ORDER BY daily_rate DESC;"
)


# --------------------------------
# 8. LIMIT
# --------------------------------

def test_limit():

    parsed, sql = run_query(
        "Show the first 5 rental records"
    )

    assert parsed["limit"] == 5


# --------------------------------
# 9. Full rental query
# --------------------------------

def test_full_rental_query():

    parsed, sql = run_query(
        "Show car model and daily rate "
        "for rentals with daily rate above 500 "
        "and daily rate below 1000 "
        "ordered by daily rate descending "
        "limit 5"
    )

    assert parsed["table"] == "rentals"

    assert parsed["fields"] == [
        "car_model",
        "daily_rate"
    ]

    assert parsed["limit"] == 5

    assert parsed["order_by"] == {
        "field": "daily_rate",
        "direction": "DESC"
    }

    assert sql == (
        "SELECT car_model, daily_rate "
        "FROM rentals "
        "WHERE (daily_rate > 500 "
        "AND daily_rate < 1000) "
        "ORDER BY daily_rate DESC "
        "LIMIT 5;"
    )


# --------------------------------
# 10. Implicit table detection
# --------------------------------

def test_implicit_table_detection():

    parsed, sql = run_query(
        "Show car model and daily rate "
        "ordered by daily rate descending"
    )

    assert parsed["table"] == "rentals"

    assert sql == (
        "SELECT car_model, daily_rate "
        "FROM rentals "
        "ORDER BY daily_rate DESC;"
    )