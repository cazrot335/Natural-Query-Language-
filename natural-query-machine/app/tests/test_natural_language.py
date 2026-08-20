from main import parse_query
from query.sql_generator import generate_sql


def run_query(query):

    parsed = parse_query(query)

    sql = generate_sql(parsed)

    return parsed, sql


# ==========================================
# GREATER THAN VARIATIONS
# ==========================================

def test_greater_than():

    _, sql = run_query(
        "Show students with marks greater than 80"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE marks > 80;"
    )


def test_more_than():

    _, sql = run_query(
        "Show students with marks more than 80"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE marks > 80;"
    )


def test_above():

    _, sql = run_query(
        "Show students with marks above 80"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE marks > 80;"
    )


def test_over():

    _, sql = run_query(
        "Show students with marks over 80"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE marks > 80;"
    )


def test_higher_than():

    _, sql = run_query(
        "Show students with marks higher than 80"
    )

    assert sql == (
    "SELECT marks FROM students "
    "WHERE marks > 80;"
)


def test_exceeding():

    _, sql = run_query(
        "Show students with marks exceeding 80"
    )

    assert sql == (
    "SELECT marks FROM students "
    "WHERE marks > 80;"
)


# ==========================================
# LESS THAN VARIATIONS
# ==========================================

def test_less_than():

    _, sql = run_query(
        "Show students with marks less than 50"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE marks < 50;"
    )


def test_lower_than():

    _, sql = run_query(
        "Show students with marks lower than 50"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE marks < 50;"
    )


def test_below():

    _, sql = run_query(
        "Show students with marks below 50"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE marks < 50;"
    )


def test_under():

    _, sql = run_query(
        "Show students with marks under 50"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE marks < 50;"
    )


def test_fewer_than():

    _, sql = run_query(
        "Show students with marks fewer than 50"
    )

    assert sql == (
    "SELECT marks FROM students "
    "WHERE marks < 50;"
)


# ==========================================
# EQUAL VARIATIONS
# ==========================================

def test_equal_to():

    _, sql = run_query(
        "Show students with age equal to 20"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE age = 20;"
    )


def test_equals():

    _, sql = run_query(
        "Show students with age equals 20"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE age = 20;"
    )


def test_equal():

    _, sql = run_query(
        "Show students with age equal 20"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE age = 20;"
    )


# ==========================================
# DECIMAL VALUES
# ==========================================

def test_decimal_greater_than():

    _, sql = run_query(
        "Show rentals with daily rate above 500.50"
    )

    assert sql == (
        "SELECT * FROM rentals "
        "WHERE daily_rate > 500.5;"
    )


def test_decimal_less_than():

    _, sql = run_query(
        "Show rentals with daily rate below 999.99"
    )

    assert sql == (
        "SELECT * FROM rentals "
        "WHERE daily_rate < 999.99;"
    )


# ==========================================
# NATURAL LANGUAGE + ORDERING
# ==========================================

def test_natural_language_with_ordering():

    _, sql = run_query(
        "Show rentals with daily rate greater than 500 "
        "ordered by daily rate descending"
    )

    assert sql == (
        "SELECT * FROM rentals "
        "WHERE daily_rate > 500 "
        "ORDER BY daily_rate DESC;"
    )


# ==========================================
# NATURAL LANGUAGE + LIMIT
# ==========================================

def test_natural_language_with_limit():

    _, sql = run_query(
        "Show rentals with daily rate less than 1000 "
        "limit 5"
    )

    assert sql == (
        "SELECT * FROM rentals "
        "WHERE daily_rate < 1000 "
        "LIMIT 5;"
    )


# ==========================================
# NATURAL LANGUAGE + AND
# ==========================================

def test_natural_language_and():

    _, sql = run_query(
        "Show rentals with daily rate greater than 500 "
        "and daily rate less than 1000"
    )

    assert sql == (
        "SELECT * FROM rentals "
        "WHERE (daily_rate > 500 "
        "AND daily_rate < 1000);"
    )


# ==========================================
# NATURAL LANGUAGE + OR
# ==========================================

def test_natural_language_or():

    _, sql = run_query(
        "Show students with marks greater than 90 "
        "or age less than 18"
    )

    assert sql == (
        "SELECT * FROM students "
        "WHERE (marks > 90 OR age < 18);"
    )


# ==========================================
# FULL NATURAL LANGUAGE QUERY
# ==========================================

def test_full_natural_language_query():

    _, sql = run_query(
        "Show car model and daily rate for rentals "
        "with daily rate greater than 500 "
        "and daily rate less than 1000 "
        "ordered by daily rate descending "
        "limit 5"
    )

    assert sql == (
        "SELECT car_model, daily_rate "
        "FROM rentals "
        "WHERE (daily_rate > 500 "
        "AND daily_rate < 1000) "
        "ORDER BY daily_rate DESC "
        "LIMIT 5;"
    )