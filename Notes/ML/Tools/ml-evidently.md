---
tags: [ml, python, evidently, monitoring, drift]
aliases: ["Evidently cheatsheet"]
created: 2026-06-11
status: complete
parent: "[[MOCs/ML & Data Science Packages -- Map of Content]]"
---

## 80/20

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, RegressionPreset
from evidently.test_suite import TestSuite
from evidently.tests import TestColumnDrift
from evidently.pipeline.column_mapping import ColumnMapping

# Map your column roles
col_map = ColumnMapping(
    target="kwh_consumed",
    prediction="predicted_kwh",
    numerical_features=["rolling_7d_avg", "kwh_lag_1d", "rainfall_mm"],
    categorical_features=["site_type_enc", "is_weekend", "month"],
)

# REPORT: human-readable HTML for manual review
report = Report(metrics=[
    DataDriftPreset(),       # feature-level drift statistics
    RegressionPreset(),      # model performance: MAPE, MAE, RMSE
])
report.run(reference_data=ref_df, current_data=curr_df, column_mapping=col_map)
report.save_html("reports/drift_2024-06-01.html")

# TEST SUITE: programmatic pass/fail for alerting
suite = TestSuite(tests=[
    TestColumnDrift(column_name="rolling_7d_avg", stattest_threshold=0.2),
    TestColumnDrift(column_name="hour_of_week", stattest_threshold=0.1),
])
suite.run(reference_data=ref_df, current_data=curr_df, column_mapping=col_map)

# Programmatic check for alerting
all_passed = suite.as_dict()["summary"]["all_passed"]
if not all_passed:
    logger.warning("Drift detected -- triggering investigation")
```

## PSI interpretation

| PSI | Meaning | Action |
|-----|---------|--------|
| < 0.1 | No meaningful shift | None |
| 0.1 -- 0.2 | Moderate shift | Investigate, check feature importance |
| > 0.2 | Significant drift | Trigger retraining if feature is important |

## Reports vs TestSuites

| | Report | TestSuite |
|--|--------|-----------|
| Purpose | Human review | Automated alerting |
| Output | HTML, JSON | Python dict (bool pass/fail) |
| When | Manual inspection, compliance | CI/CD gates, Slack alerts |

## Traps

- **Reference dataset must be representative** -- pick a known-good window (e.g., first 30 days post-deployment). Bad reference = bad drift detection.
- **Column mapping is required** -- without it, Evidently treats all columns as numerical features and _guesses_ the target/prediction columns.
- **Dataset size matters** -- very small current_data (< 100 rows) produces unreliable drift statistics.
- **PSI thresholds are domain-specific** -- 0.2 is a starting point. Tune after observing real drift patterns.
- **`as_dict()` structure is nested** -- always inspect `suite.as_dict()["summary"]["all_passed"]` first to understand the shape.
