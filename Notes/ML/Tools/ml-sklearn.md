---
tags: [ml, sklearn, machine-learning, preprocessing, evaluation]
aliases: ["scikit-learn", "sklearn"]
parent: "[[MOCs/ML & Data Science Packages -- Map of Content]]"
created: 2026-06-11
status: complete
---

# L3 -- scikit-learn

## 80/20 Cheat Sheet

```python
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, confusion_matrix,
    precision_score, recall_score, f1_score, roc_auc_score, average_precision_score)
from sklearn.pipeline import Pipeline

# 1. Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 2. Scale (fit ONLY on train)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# 3. Train
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train_s, y_train)

# 4. Predict
y_pred = model.predict(X_test_s)             # hard labels
y_prob = model.predict_proba(X_test_s)[:, 1] # probabilities

# 5. Evaluate
print(classification_report(y_test, y_pred))
print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.3f}")
print(f"PR-AUC:  {average_precision_score(y_test, y_prob):.3f}")

# 6. Pipeline (prevents leakage)
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier(random_state=42))
])
pipe.fit(X_train, y_train)
cross_val_score(pipe, X, y, cv=5, scoring='f1')

# 7. Grid search
param_grid = {'clf__n_estimators': [100, 200], 'clf__max_depth': [5, 10]}
grid = GridSearchCV(pipe, param_grid, cv=5, scoring='f1')
grid.fit(X_train, y_train)
print(grid.best_params_)
```

## Core API pattern

Every sklearn object is either a **Transformer** or an **Estimator**. Same three methods:

| Method | Transformer | Estimator |
|--------|------------|-----------|
| `.fit(X, y)` | Learns params (mean, std) | Trains model |
| `.transform(X)` | Applies learned params | -- |
| `.predict(X)` | -- | Generates predictions |
| `.fit_transform(X)` | Fit + transform (train only) | -- |
| `.score(X, y)` | -- | Default metric |

**Golden rule:** Fit ONLY on training data. Transform both train and test with the same fitted object. Fitting on all data leaks test information into training.

```python
# CORRECT
scaler = StandardScaler()
scaler.fit(X_train)                     # learn from train
X_train_s = scaler.transform(X_train)
X_test_s  = scaler.transform(X_test)    # same params applied to test

# WRONG -- leakage
full_scaler = StandardScaler().fit(X)   # test influenced mean/std
```

## Preprocessing -- scaling

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# StandardScaler: (x - mean) / std -> mean=0, std=1
# For: gradient-based models (LR, SVM, NN, LSTM), PCA
StandardScaler()

# MinMaxScaler: (x - min) / (max - min) -> [0, 1]
# For: NNs with sigmoid/tanh. BUT: one outlier compresses everything else
MinMaxScaler()

# RobustScaler: (x - median) / IQR -> robust to outliers
# For: industrial sensor data with spikes, faults
RobustScaler()
```

**Trap:** Tree-based models (Random Forest, Gradient Boosting) don't need scaling. Scaling for them is wasted compute.

## Preprocessing -- encoding categories

```python
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# LabelEncoder: string -> integer (0, 1, 2...)
# For: ordinal categories, tree models
le = LabelEncoder()
y_encoded = le.fit_transform(['A', 'B', 'A', 'C'])
# [0, 1, 0, 2]
le.classes_                                # ['A', 'B', 'C']

# OneHotEncoder: each category -> binary column
# For: nominal categories with linear models/NNs
ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded = ohe.fit_transform([['A'], ['B'], ['A'], ['C']])
# [[1, 0, 0], [0, 1, 0], [1, 0, 0], [0, 0, 1]]

# ColumnTransformer for mixed types (numeric + categorical)
from sklearn.compose import ColumnTransformer, make_column_selector

ct = ColumnTransformer([
    ('scale', StandardScaler(), ['temp', 'pressure']),
    ('encode', OneHotEncoder(), ['op_setting']),
])
```

**Trap:** `handle_unknown='ignore'` handles unseen categories in test data. Without it, unseen categories break `.transform()`.

## Train-test split

```python
from sklearn.model_selection import train_test_split

# Standard random split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,          # reproducible
    stratify=y                # keep class ratio -- critical for imbalance
)

# Time-series: DON'T shuffle -- split by time
train = df[df['cycle'] < cutoff]
test  = df[df['cycle'] >= cutoff]

# Panel data (C-MAPSS): split by UNIT, not by row
units = df['unit'].unique()
train_units = units[:int(len(units)*0.8)]
test_units  = units[int(len(units)*0.8):]
train = df[df['unit'].isin(train_units)]
test  = df[df['unit'].isin(test_units)]
```

**Critical:** Never use `train_test_split` on time-series data without `shuffle=False` or manual split by time. Random shuffle leaks future into past.

## Models -- when to use what

### Classification

```python
# Logistic Regression -- baseline, fast, interpretable
from sklearn.linear_model import LogisticRegression
LogisticRegression(C=1.0, class_weight='balanced', max_iter=1000)
# C: inverse of regularization (smaller = stronger regularization)
# class_weight='balanced' for imbalanced data

# Random Forest -- strong default for tabular data
from sklearn.ensemble import RandomForestClassifier
RandomForestClassifier(
    n_estimators=100,          # more trees = better, diminishing returns
    max_depth=10,              # limit depth to prevent overfitting
    min_samples_split=5,       # min samples to split a node
    min_samples_leaf=2,        # min samples per leaf
    class_weight='balanced',   # handle imbalance
    random_state=42,
    n_jobs=-1                  # use all CPUs
)
# Feature importance: model.feature_importances_

# Gradient Boosting -- high performance, slower train
from sklearn.ensemble import GradientBoostingClassifier
GradientBoostingClassifier(
    n_estimators=100,          # number of boosting stages
    learning_rate=0.1,         # smaller = better but needs more estimators
    max_depth=3,               # shallow trees for boosting
    subsample=0.8,             # stochastic (fraction of samples per tree)
    random_state=42,
)
# XGBoost/LightGBM are faster alternatives (not in sklearn)

# SVM -- good for high-dimensional, non-linear boundaries
from sklearn.svm import SVC
SVC(kernel='rbf', C=1.0, gamma='scale', class_weight='balanced')
# kernel: 'rbf' (default), 'linear', 'poly'
# C: regularization (smaller = softer margin)
# gamma: kernel width (smaller = smoother)
# REQUIRES scaling -- sensitive to feature magnitudes

# KNN -- simple, non-parametric baseline
from sklearn.neighbors import KNeighborsClassifier
KNeighborsClassifier(n_neighbors=5, weights='distance')
# REQUIRES scaling
# Slow for large datasets -- distance computation scales badly

# Naive Bayes -- fast, good for text/high-dim sparse data
from sklearn.naive_bayes import GaussianNB
GaussianNB()                                # continuous features
# Also: MultinomialNB (counts), BernoulliNB (binary)
```

### Anomaly detection

```python
# Isolation Forest -- standard for anomaly detection
from sklearn.ensemble import IsolationForest
iso = IsolationForest(
    n_estimators=200,
    contamination=0.05,         # expected proportion of anomalies
    random_state=42,
)
iso.fit(X_train)                              # train only on normal
scores = iso.score_samples(X_test)            # lower = more anomalous
labels = iso.predict(X_test)                  # -1 = anomaly, 1 = normal

# One-Class SVM -- boundary-based
from sklearn.svm import OneClassSVM
OneClassSVM(nu=0.1, kernel='rbf', gamma='scale')
# nu: upper bound on fraction of anomalies

# Local Outlier Factor -- density-based
from sklearn.neighbors import LocalOutlierFactor
# Works as novelty detection: fit on normal, predict on test
lof = LocalOutlierFactor(novelty=True)
lof.fit(X_train)
lof.score_samples(X_test)
```

### Regression

```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

# Linear -- baseline
LinearRegression()

# Ridge (L2) -- penalizes large coefficients, keeps all features
Ridge(alpha=1.0)

# Lasso (L1) -- feature selection (drives some coeffs to 0)
Lasso(alpha=0.01)

# Tree-based regressors
RandomForestRegressor(n_estimators=100, max_depth=10)
GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
```

### Dimensionality reduction

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=0.95)               # keep 95% of variance
X_pca = pca.fit_transform(X_scaled)
print(pca.explained_variance_ratio_)       # variance per component
print(pca.components_)                     # feature loadings

from sklearn.manifold import TSNE          # visualization only
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X)             # no .transform() for new data
```

## Evaluation metrics

```python
from sklearn.metrics import (confusion_matrix, classification_report,
    precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score,
    mean_squared_error, mean_absolute_error, r2_score)

y_true = np.array([0, 0, 0, 1, 0, 1, 0, 0, 1, 0])
y_pred = np.array([0, 0, 0, 1, 0, 0, 0, 0, 1, 0])
y_prob = np.array([0.1, 0.2, 0.1, 0.9, 0.3, 0.4, 0.1, 0.2, 0.8, 0.15])

# Confusion matrix
cm = confusion_matrix(y_true, y_pred)
#           Pred 0  Pred 1
# Actual 0   TN=7     FP=0
# Actual 1   FN=1     TP=2

# Precision, Recall, F1
# Precision: TP / (TP + FP) -- of flagged anomalies, how many were real?
# Recall:    TP / (TP + FN) -- of real anomalies, how many were caught?
# F1:        harmonic mean of precision and recall
print(classification_report(y_true, y_pred, target_names=['normal', 'anomaly']))

# For imbalanced data:
# PR-AUC is better than ROC-AUC
print(f"ROC-AUC: {roc_auc_score(y_true, y_prob):.3f}")          # can be misleading
print(f"PR-AUC:  {average_precision_score(y_true, y_prob):.3f}") # better for imbalance

# Regression
y_true_r = [100, 200, 300]
y_pred_r = [110, 190, 310]
print(f"RMSE: {np.sqrt(mean_squared_error(y_true_r, y_pred_r)):.2f}")
print(f"MAE:  {mean_absolute_error(y_true_r, y_pred_r):.2f}")
print(f"R2:   {r2_score(y_true_r, y_pred_r):.3f}")
```

## Pipelines

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# Build
pipe = Pipeline([
    ('scaler', StandardScaler()),          # step name, transformer
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Use like a normal estimator
pipe.fit(X_train, y_train)
preds = pipe.predict(X_test)

# Cross-validation scales inside each fold -- no leakage
scores = cross_val_score(pipe, X, y, cv=5, scoring='f1_macro')

# Access named steps
pipe.named_steps['scaler'].mean_
pipe.named_steps['clf'].feature_importances_

# ColumnTransformer inside pipeline (mixed types)
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), ['temp', 'pressure', 'vib']),
    ('cat', OneHotEncoder(), ['op_setting']),
])

full_pipe = Pipeline([
    ('prep', preprocessor),
    ('clf', RandomForestClassifier(random_state=42))
])
```

**Why pipelines:** Prevents leakage, simplifies cross-validation, makes deployment trivial (one fitted object instead of many).

## Hyperparameter tuning

```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

# Grid search -- exhaustive
param_grid = {
    'clf__n_estimators': [100, 200, 300],
    'clf__max_depth': [5, 10, 15, None],
    'clf__min_samples_split': [2, 5, 10],
}
grid = GridSearchCV(pipe, param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=1)
grid.fit(X_train, y_train)
print(grid.best_params_)                   # {'clf__max_depth': 10, ...}
print(grid.best_score_)                    # best CV score

# Randomized search -- sample from distributions (faster)
from scipy.stats import randint
param_dist = {
    'clf__n_estimators': randint(50, 500),
    'clf__max_depth': randint(3, 20),
    'clf__min_samples_split': randint(2, 20),
}
random_search = RandomizedSearchCV(pipe, param_dist, n_iter=20, cv=5,
                                   scoring='f1', random_state=42, n_jobs=-1)
random_search.fit(X_train, y_train)
```

## Cross-validation

```python
from sklearn.model_selection import (cross_val_score, cross_validate,
    StratifiedKFold, KFold, TimeSeriesSplit)

# Basic CV
scores = cross_val_score(pipe, X, y, cv=5, scoring='f1')

# More detail
cv_results = cross_validate(pipe, X, y, cv=5,
    scoring=['f1', 'roc_auc', 'precision'],
    return_estimator=True,                    # access each fold's model
    return_train_score=True)                  # detect overfitting

# Stratified KFold (preserves class ratio per fold)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Time-series CV
tscv = TimeSeriesSplit(n_splits=5)
for train_idx, test_idx in tscv.split(X):
    X_train_fold, X_test_fold = X[train_idx], X[test_idx]
```

## Common traps

```python
# TRAP 1: Data leakage via scaling before split
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)          # test data influenced mean/std
X_train, X_test = train_test_split(X_scaled, ...)  # WRONG

# TRAP 2: Using accuracy on imbalanced data
# 99% normal, 1% fault -> 99% accuracy by predicting "normal" always
# Use: precision, recall, F1, PR-AUC

# TRAP 3: Not stratifying on imbalanced data
train_test_split(X, y, test_size=0.2)       # might get 0 anomalies in test
train_test_split(X, y, test_size=0.2, stratify=y)  # correct

# TRAP 4: predict vs predict_proba confusion
model.predict(X)                             # hard labels (0 or 1)
model.predict_proba(X)[:, 1]                # probability of class 1
# For anomaly scoring (threshold tuning), use predict_proba

# TRAP 5: Random Forest with default params on small data -> overfitting
rf = RandomForestClassifier()               # max_depth=None, overfits
# Fix: set max_depth, min_samples_split, min_samples_leaf

# TRAP 6: Not scaling for SVM/KNN/PCA/LR
# Distance-based models assume all features on same scale.
# Tree models don't need scaling.

# TRAP 7: Forgetting class_weight='balanced' for imbalanced data
# Without it, the model optimises for majority class accuracy.
# The minority class (anomalies) gets ignored.

# TRAP 8: Hyperparameter tuning on full data (overfitting the search)
grid = GridSearchCV(pipe, params, cv=5)
grid.fit(X, y)                               # WRONG -- uses test info
# Correct: fit on X_train only, evaluate on X_test

# TRAP 9: Leakage via feature engineering before split
df['rolling_mean'] = df.groupby('unit')['vib'].transform(lambda s: s.rolling(3).mean())
X = df[['rolling_mean']]                     # WRONG -- future info leaked
# Correct: engineer features within each CV fold (use Pipeline)
```
