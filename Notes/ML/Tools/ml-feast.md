---
tags: [ml, python, feast, feature-store]
aliases: ["Feast cheatsheet"]
created: 2026-06-11
status: complete
parent: "[[MOCs/ML & Data Science Packages -- Map of Content]]"
---

## 80/20

```python
from feast import Entity, FileSource, FeatureView, Field, FeatureStore
from feast.types import Float32, Int64, String

# 1. Define the join key
site = Entity(name="site_id", value_type=String)

# 2. Define the data source (Parquet)
source = FileSource(
    path="data/features/site_features.parquet",
    timestamp_field="event_timestamp",
)

# 3. Define the feature group
fv = FeatureView(
    name="site_features",
    entities=["site_id"],
    ttl="48h",          # features are valid for 48 hours
    schema=[
        Field(name="rolling_7d_avg", dtype=Float32),
        Field(name="kwh_lag_1d", dtype=Float32),
        Field(name="is_weekend", dtype=Int64),
        Field(name="hour_of_week", dtype=Int64),
    ],
    source=source,
)

# 4. Store client
store = FeatureStore(repo_path="src/features/feature_repo")

# --- TRAINING ---
entity_df = pd.DataFrame({
    "site_id": ["site_a", "site_b"],
    "event_timestamp": ["2024-06-01", "2024-06-01"],
    "kwh_consumed": [142.0, 89.0],       # label column
})
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=["site_features:rolling_7d_avg", "site_features:is_weekend"],
).to_df()
# Feast does AS-OF join -- for each row, scans backward and returns the most
# recent feature value at or before event_timestamp. Prevents data leakage.

# --- SERVING ---
features = store.get_online_features(
    features=["site_features:rolling_7d_avg", "site_features:is_weekend"],
    entity_rows=[{"site_id": "site_a"}],
).to_dict()

# --- MATERIALISE (bridge offline -> online) ---
store.materialize(start_date="2024-01-01", end_date="2024-06-01")
```

## Architecture

```
Feature Parquet -> Offline Store -> get_historical_features() -> Training DataFrame
                        |
                  materialize()
                        |
                   Online Store -> get_online_features() -> Serving API
```

The critical decoupling: both training (`get_historical_features`) and serving (`get_online_features`) read from the **same feature definitions**. No separate feature code at inference time = no train/serve skew.

## AS-OF join (critical concept)

For training, Feast receives an `entity_df` with `entity_key + event_timestamp + labels`. For each row it scans backward and picks the most recent feature value at or before that timestamp. This:

- Prevents **data leakage** (future features never leak into training)
- Works with **irregularly sampled** features
- Handles **multiple feature views** with different TTLs

## Key methods

| Method | Returns | Purpose |
|--------|---------|---------|
| `get_historical_features(entity_df, features).to_df()` | DataFrame | Training -- point-in-time correct features |
| `get_online_features(features, entity_rows).to_dict()` | dict | Serving -- latest value per entity key |
| `materialize(start_date, end_date)` | None | Bridge offline -> online store |

## Traps

- **TTL too short** -- if `ttl < training data span`, features expire and `get_historical_features` returns nulls.
- **Missing `materialize()`** -- if you skip materialization, `get_online_features` returns nothing.
- **Entity DataFrame must have `event_timestamp` column** -- this is how Feast performs the AS-OF join.
- **Feature names at retrieval** -- use colon notation: `feature_view_name:feature_name`.
- **Feature schema changes** -- when you add/remove features, you must also update the `FeatureView` definition and re-materialize.
