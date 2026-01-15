import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier


CSV_PATH = "road-traffic-data.csv"
SAMPLE_FRAC = 0.2
RANDOM_STATE = 42


df = pd.read_csv(CSV_PATH)

if SAMPLE_FRAC < 1.0:
    df = df.sample(frac=SAMPLE_FRAC, random_state=RANDOM_STATE).reset_index(drop=True)

speed_cols = [c for c in df.columns if "SPEEDAVGARITH" in c]
occ_cols = [c for c in df.columns if "OCCUPRATE" in c]
veh_cols = [c for c in df.columns if "VEHS(ALL)" in c]
queue_cols = [c for c in df.columns if "QUEUEDELAY" in c]

X = pd.DataFrame()
X["mean_speed"] = df[speed_cols].mean(axis=1)
X["std_speed"] = df[speed_cols].std(axis=1)
X["mean_occupancy"] = df[occ_cols].mean(axis=1)
X["max_occupancy"] = df[occ_cols].max(axis=1)
X["total_vehicles"] = df[veh_cols].sum(axis=1)
X["mean_queue_delay"] = df[queue_cols].mean(axis=1)

y_cont = X["mean_occupancy"]
mask = y_cont.notna() & np.isfinite(y_cont)

X = X.loc[mask].reset_index(drop=True)
y_cont = y_cont.loc[mask].reset_index(drop=True)

y = pd.qcut(y_cont, q=3, labels=[0, 1, 2], duplicates="drop").astype(int)
X = X.drop(columns=["mean_occupancy"])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)

models = {
    "LogReg": LogisticRegression(max_iter=2000),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=200),
    "Neural Network": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=400, early_stopping=True, random_state=RANDOM_STATE)
}

results = []
cms = {}

for name, model in models.items():
    start = time.time()

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", model)
    ])

    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

    results.append([name, acc, prec, rec, f1])

    cm = confusion_matrix(y_test, y_pred)
    cms[name] = cm / cm.sum(axis=1, keepdims=True)

    print(f"{name} finished in {time.time() - start:.1f} seconds")

df_perf = pd.DataFrame(
    results,
    columns=["Model", "Accuracy", "Precision", "Recall", "F1"]
).sort_values("Accuracy", ascending=False).reset_index(drop=True)

print(df_perf.to_string(index=False))

plt.figure(figsize=(10, 5))
sns.barplot(data=df_perf, x="Model", y="Accuracy")
plt.ylim(0, 1)
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.ravel()

for i, name in enumerate(cms):
    sns.heatmap(cms[name], annot=True, fmt=".2f", ax=axes[i], cmap="Blues")
    axes[i].set_title(name)

plt.tight_layout()
plt.show()

best_model_name = df_perf.iloc[0]["Model"]
best_model = models[best_model_name]

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", best_model)
])

pipe.fit(X_train, y_train)

sample = X_test.iloc[0].values.reshape(1, -1)

print("DEMO RUN")
print("Best Model:", best_model_name)
print("True Label:", y_test.iloc[0])
print("Predicted Label:", pipe.predict(sample)[0])
print("Class Probabilities:", pipe.predict_proba(sample)[0])
