---
tags: [ml, python, pandera, data-validation]
aliases: ["Pandera cheatsheet"]
created: 2026-06-11
status: complete
parent: "[[MOCs/ML & Data Science Packages -- Map of Content]]"
---

## 80/20

```python
import pandera as pa
from pandera.typing import DataFrame, Series

# Define schema
schema = pa.DataFrameSchema(
    {
        "site_id": pa.Column(str, pa.Check.isin(["site_a", "site_b", "site_c"])),
        "kwh_consumed": pa.Column(float, pa.Check.ge(0)),
        "rolling_7d_avg": pa.Column(float, pa.Check.ge(0)),
        "is_weekend": pa.Column(int, pa.Check.isin([0, 1])),
        "is_holiday": pa.Column(int, nullable=True),  # nulls are OK
    },
    strict=True,  # reject columns NOT in schema
)

# Validate -- catches renamed columns, wrong dtypes, constraint violations
schema.validate(df)

# Lazy mode: collect ALL failures before raising (useful in CI)
try:
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as e:
    for _, row in e.failure_cases.iterrows():
        logger.warning(f"{row['column']}: {row['check']} failed at index {row['index']}")

# Decorator pattern
@pa.check_output(schema)
def clean_data(raw: DataFrame) -> DataFrame:
    ...

@pa.check_input(schema, "df")
def train_model(df: DataFrame[site_schema]) -> ...:
    ...
```

## Built-in checks

| Check | What it enforces |
|-------|-----------------|
| `Check.ge(n)` | value >= n |
| `Check.le(n)` | value <= n |
| `Check.isin(values)` | value in allowed set |
| `Check.notnull()` | no nulls allowed |
| `Check.str_matches(r"pattern")` | string matches regex |
| `Check.between(a, b)` | a <= value <= b |
| `Check(lambda s: s.mean() > 0)` | custom predicate on Series |

## Error handling modes

| Mode | Behaviour |
|------|-----------|
| `lazy=False` (default) | stop at first failure, raise `SchemaError` |
| `lazy=True` | collect all failures, raise `SchemaErrors` with `.failure_cases` DataFrame |

```python
# Collect all failures
try:
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as e:
    failures = e.failure_cases  # DataFrame with column, check, index, value
```

## Traps

- **`strict=True` catches renamed columns** -- if a column is renamed or dropped downstream, `strict=True` raises. Without it, extra columns are silently ignored.
- **Null handling is explicit** -- `nullable=True` allows nulls; `nullable=False` rejects them. The default is `nullable=True`, which can mask null-spike bugs.
- **@check_io requires argument name** -- `@pa.check_input(schema, "df_name")`, the second argument is the parameter name in the function signature.
- **Custom Check lambdas return boolean Series** -- not scalar. Pandera checks each element.
- **Coercion** -- use `pa.Column(float, coerce=True)` to auto-cast dtypes. Be careful: coercion can mask wrong input types.
