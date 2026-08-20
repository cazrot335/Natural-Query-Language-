# Natural Query Language (NQL)

A lightweight Python engine that converts plain English questions into SQL queries — no LLM, no external API, just deterministic rule-based parsing.

> "Show students with marks greater than 80 ordered by marks descending first 5"
> → `SELECT * FROM students WHERE marks > 80 ORDER BY marks DESC LIMIT 5;`

---

## How It Works

The engine treats a natural language query as a pipeline of independent detectors. Each stage extracts one piece of the final SQL statement, and the results are assembled into a structured intermediate representation before being rendered as SQL.

```
                         ┌───────────────────────┐
   "Show students with   │   1. Tokenizer         │
    marks greater than    │   query.lower().split()│
    80 ordered by marks   └───────────┬───────────┘
    descending first 5"               │
                                       ▼
                          ┌────────────────────────┐
                          │  2. Intent Detection     │  → SELECT / COUNT / UNKNOWN
                          │     parser/intent.py     │
                          └───────────┬─────────────┘
                                       ▼
                          ┌────────────────────────┐
                          │  3. Entity (Table)       │  → e.g. "students"
                          │     Detection            │     (alias match → schema
                          │     parser/entities.py   │      match → field-inference)
                          └───────────┬─────────────┘
                                       ▼
                          ┌────────────────────────┐
                          │  4. Field Detection      │  → SELECT columns,
                          │     parser/fields.py     │     excluding fields used
                          │                          │     in WHERE / ORDER BY
                          └───────────┬─────────────┘
                                       ▼
                          ┌────────────────────────┐
                          │  5. Condition Detection  │  → field / operator / value
                          │     parser/conditions.py │     + AND / OR connectors
                          └───────────┬─────────────┘
                                       ▼
                          ┌────────────────────────┐
                          │  6. Boolean Tree Builder │  → nested AND/OR expression
                          │     parser/boolean.py    │     tree (AND binds tighter
                          │                          │     than OR)
                          └───────────┬─────────────┘
                                       ▼
                          ┌────────────────────────┐
                          │  7. Ordering Detection   │  → ORDER BY field + ASC/DESC
                          │     parser/ordering.py   │
                          └───────────┬─────────────┘
                                       ▼
                          ┌────────────────────────┐
                          │  8. Limit Detection      │  → LIMIT n
                          │     parser/limit.py      │
                          └───────────┬─────────────┘
                                       ▼
                          ┌────────────────────────┐
                          │  Structured Query dict   │
                          │  { intent, table, fields,│
                          │    conditions, tree,     │
                          │    order_by, limit }     │
                          └───────────┬─────────────┘
                                       ▼
                          ┌────────────────────────┐
                          │  9. Validation            │  → checks table/fields exist
                          │     query/validator.py    │     against SCHEMA
                          └───────────┬─────────────┘
                                       ▼
                          ┌────────────────────────┐
                          │ 10. SQL Generation        │  → walks the boolean tree,
                          │     query/sql_generator.py│     assembles final SQL
                          └───────────┬─────────────┘
                                       ▼
                    "SELECT * FROM students WHERE marks > 80
                     ORDER BY marks DESC LIMIT 5;"
```

### Why this design

- **No ML/LLM dependency.** Every stage is regex- and rule-based, so results are 100% deterministic and reproducible — the same input always produces the same SQL.
- **Separation of concerns.** Parsing (understanding the English) is fully decoupled from query building (producing the SQL), via `parser/` and `query/` respectively.
- **Schema-driven.** All table/field validity is derived from a single source of truth (`query/models.py::SCHEMA`), so adding a table is a one-line change that automatically ripples through entity detection, field detection, and validation.
- **Boolean tree over flat conditions.** Conditions aren't just concatenated with `AND`/`OR` — they're compiled into a small expression tree (`parser/boolean.py`) so precedence (AND groups within an OR) is preserved and rendered with correct parentheses.

---

## Project Structure

```
natural-query-machine/
├── requirements.txt
└── app/
    ├── main.py                    # Entry point — orchestrates the pipeline
    ├── parser/                    # Natural language understanding
    │   ├── tokenizer.py           # Splits raw text into tokens
    │   ├── intent.py              # SELECT / COUNT detection
    │   ├── entities.py            # Table detection (aliases, schema, inference)
    │   ├── fields.py              # SELECT-column detection
    │   ├── conditions.py          # WHERE condition detection (field, operator, value)
    │   ├── boolean.py             # Builds AND/OR expression tree from conditions
    │   ├── ordering.py            # ORDER BY detection
    │   └── limit.py                # LIMIT detection
    ├── query/                     # SQL construction
    │   ├── models.py              # SCHEMA — the source of truth for tables/fields
    │   ├── validator.py           # Validates parsed query against SCHEMA
    │   └── sql_generator.py       # Renders the structured query into SQL text
    └── tests/
        ├── test_parser.py         # Unit tests for individual parser stages
        └── test_natural_language.py  # End-to-end English → SQL tests
```

---

## Supported Schema

The engine currently understands four demo tables, defined in `app/query/models.py`:

| Table      | Fields                                                              |
|------------|----------------------------------------------------------------------|
| `students` | `id`, `name`, `age`, `marks`, `branch`, `state`                      |
| `teachers` | `id`, `name`, `age`, `subject`                                       |
| `rentals`  | `rental_id`, `car_model`, `daily_rate`, `customer_name`, `rental_date`, `return_date` |
| `courses`  | `id`, `course_name`, `duration`, `fee`                                |

To add a new table, add it to `SCHEMA` in `query/models.py` (and optionally register friendly aliases in `parser/entities.py::ENTITY_ALIASES` and `parser/fields.py::FIELD_ALIASES`).

---

## Supported Query Features

| Feature      | Example phrases                                                       |
|--------------|-------------------------------------------------------------------------|
| Intent       | `show`, `find`, `list`, `display`, `get` → `SELECT`; `how many` → `COUNT` |
| Table        | Direct name (`students`), alias (`student`), or inferred from mentioned fields |
| Fields       | Column names or human-readable aliases (e.g. `car model` → `car_model`) |
| Conditions   | `greater than`, `more than`, `above`, `over`, `less than`, `below`, `under`, `equal to`, `equals`, etc. |
| Logic        | `and` / `or` between multiple conditions, compiled into a precedence-aware tree |
| Ordering     | `ordered by`, `order by`, `sorted by`, `sort by` + `ascending`/`descending` |
| Limit        | `first N`, `top N`, `only N`, `just N`, `limit N`                      |

---

## Usage

### Requirements

- Python 3.9+

### Run interactively

```bash
cd natural-query-machine/app
python3 main.py
```

```
Enter query: Show name and marks of students with marks greater than 80 and age less than 20 ordered by marks descending first 5

Structured Query:
{'intent': 'SELECT', 'table': 'students', 'fields': ['name', 'marks'],
 'conditions': [...], 'condition_tree': {...},
 'order_by': {'field': 'marks', 'direction': 'DESC'}, 'limit': 5}

Generated SQL:
SELECT name, marks FROM students WHERE (marks > 80 AND age < 20) ORDER BY marks DESC LIMIT 5;
```

### Use as a library

```python
from main import parse_query
from query.validator import validate_query
from query.sql_generator import generate_sql

parsed = parse_query("How many teachers teach maths")
validate_query(parsed)
sql = generate_sql(parsed)

print(sql)  # SELECT COUNT(*) FROM teachers;
```

### More examples

| Natural language input                                                        | Generated SQL |
|---------------------------------------------------------------------------------|----------------|
| `Show students with marks greater than 80`                                      | `SELECT * FROM students WHERE marks > 80;` |
| `List course name and fee for courses`                                          | `SELECT course_name, fee FROM courses;` |
| `Find rentals with daily rate below 50 or car model equal to 5`                 | `SELECT * FROM rentals WHERE (daily_rate < 50 OR car_model = 5);` |
| `How many students are there`                                                   | `SELECT COUNT(*) FROM students;` |
| `Display teachers ordered by age descending`                                    | `SELECT * FROM teachers ORDER BY age DESC;` |

### Run the tests

```bash
pip install pytest
cd natural-query-machine/app
python3 -m pytest tests/ -v
```

---

## Roadmap / Ideas

- Support `JOIN`s across related tables
- Support `INSERT` / `UPDATE` / `DELETE` intents
- Pluggable schema loading (introspect an actual live database instead of a hardcoded `SCHEMA`)
- CLI flags for non-interactive / scripted usage
- Wrap the pipeline behind a small REST API

---

## Author

[Parth Kamat](https://github.com/cazrot335)
