"""
Soluciones: ejercicios del notebook 01_pipelines_iris (módulo 07).

    uv run python 07-Pipelines/ejercicios/soluciones/solucion_07_iris.py
"""

import time

from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

SEMILLA = 42
X, y = load_iris(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=SEMILLA, stratify=y)
cv = StratifiedKFold(5, shuffle=True, random_state=SEMILLA)

# --- 1. SVC con grilla ---------------------------------------------------------------------
pipe_svc = Pipeline([("scaler", StandardScaler()), ("pca", PCA(n_components=2)), ("clf", SVC())])
grid_svc = GridSearchCV(
    pipe_svc,
    {"pca__n_components": [2, 3, 4], "clf__C": [0.1, 1, 10], "clf__kernel": ["linear", "rbf"]},
    cv=cv, n_jobs=-1,
).fit(X_train, y_train)
print(f"1) SVC → mejores {grid_svc.best_params_} · accuracy CV = {grid_svc.best_score_:.3f}")
print("   (El Gradient Boosting del notebook llegó a ~0.95: el SVC le compite o le gana con un modelo mucho más simple.)\n")

# --- 2. Sin PCA ---------------------------------------------------------------------------------
con_pca = Pipeline([("scaler", StandardScaler()), ("pca", PCA(n_components=2)), ("clf", LogisticRegression(max_iter=1000))])
sin_pca = Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=1000))])
for nombre, pipe in [("Con PCA(2)", con_pca), ("Sin PCA", sin_pca)]:
    print(f"2) {nombre:<11} accuracy CV = {cross_val_score(pipe, X_train, y_train, cv=cv).mean():.3f}")
print("   → Sin PCA mejora: con solo 4 variables no hace falta reducir dimensiones, y PCA(2) bota información útil.")
print("     PCA sirve cuando hay muchas variables correlacionadas o para visualizar.\n")

# --- 3. RandomizedSearch vs. GridSearch -------------------------------------------------------------
pipe_gb = Pipeline([("scaler", StandardScaler()), ("pca", PCA()), ("clf", GradientBoostingClassifier(random_state=SEMILLA))])
grilla = {"pca__n_components": [2, 3, 4], "clf__n_estimators": [10, 50, 100], "clf__max_depth": [1, 2, 3]}

inicio = time.perf_counter()
grid = GridSearchCV(pipe_gb, grilla, cv=cv, n_jobs=-1).fit(X_train, y_train)
t_grid = time.perf_counter() - inicio

inicio = time.perf_counter()
rand = RandomizedSearchCV(pipe_gb, grilla, n_iter=10, cv=cv, n_jobs=-1, random_state=SEMILLA).fit(X_train, y_train)
t_rand = time.perf_counter() - inicio

print(f"3) GridSearch:       27 combinaciones · {t_grid:.1f} s · mejor CV = {grid.best_score_:.3f}")
print(f"   RandomizedSearch: 10 combinaciones · {t_rand:.1f} s · mejor CV = {rand.best_score_:.3f}")
print("   → Con grillas grandes, RandomizedSearch encuentra algo casi igual de bueno en una fracción del tiempo.")
