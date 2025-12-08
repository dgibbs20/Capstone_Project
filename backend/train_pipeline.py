# backend/train_pipeline.py
"""
Train a text-aware classification pipeline:
- Features:
    text: TF-IDF on "description + merchant" (or existing 'text' column)
    cat : OneHot on payment_method
    num : amount, month, day, is_weekend (passthrough)
- Model: LinearSVC (fast, robust for sparse text)
- Outputs:
    backend/model_pipeline.pkl
    backend/metrics/classification_report.txt
    backend/metrics/metrics.json
    backend/metrics/confusion_matrix.png
"""

import os, json, joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.svm import LinearSVC

HERE = os.path.dirname(__file__)
DATA_PATH = os.path.join(HERE, "expenses_preprocessed.csv")
MODEL_PATH = os.path.join(HERE, "model_pipeline.pkl")
METRICS_DIR = os.path.join(HERE, "metrics")
os.makedirs(METRICS_DIR, exist_ok=True)

def ensure_text_column(df: pd.DataFrame) -> pd.DataFrame:
    # If 'text' is missing, synthesize it from 'description' and 'merchant' if present
    if "text" not in df.columns:
        desc = df["description"].astype(str) if "description" in df.columns else ""
        merch = df["merchant"].astype(str) if "merchant" in df.columns else ""
        df = df.copy()
        df["text"] = (desc + " " + merch).str.strip()
    # Fill NaNs
    df["text"] = df["text"].fillna("")
    return df

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Expected target column
    if "category" not in df.columns:
        raise ValueError("Expected 'category' column in dataset.")
    # Ensure text
    df = ensure_text_column(df)
    # Ensure required feature columns exist
    for col in ["amount", "month", "day", "is_weekend", "payment_method"]:
        if col not in df.columns:
            if col in ["month", "day", "is_weekend"]:
                df[col] = 1 if col == "is_weekend" else 1  # minimal fallback
            else:
                raise ValueError(f"Missing required column: {col}")
    # Clean types
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["month"] = pd.to_numeric(df["month"], errors="coerce").fillna(1).astype(int)
    df["day"] = pd.to_numeric(df["day"], errors="coerce").fillna(1).astype(int)
    df["is_weekend"] = pd.to_numeric(df["is_weekend"], errors="coerce").fillna(0).astype(int)
    df["payment_method"] = df["payment_method"].astype(str).fillna("Unknown")
    df["category"] = df["category"].astype(str)
    return df

def plot_confusion_matrix(cm: np.ndarray, labels: list, out_path: str):
    fig = plt.figure(figsize=(8, 6), dpi=200)
    ax = plt.gca()
    im = ax.imshow(cm, interpolation="nearest")
    ax.set_title("Confusion Matrix")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)
    # write counts
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center", fontsize=9)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)

def main():
    print("🔹 Loading data:", DATA_PATH)
    df = load_data(DATA_PATH)

    feature_cols_text = ["text"]
    feature_cols_cat = ["payment_method"]
    feature_cols_num = ["amount", "month", "day", "is_weekend"]
    target_col = "category"

    X = df[feature_cols_text + feature_cols_cat + feature_cols_num].copy()
    y = df[target_col].copy()

    # Build preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ("text", TfidfVectorizer(max_features=5000, ngram_range=(1,2)), "text"),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["payment_method"]),
            ("num", "passthrough", feature_cols_num),
        ],
        remainder="drop",
        sparse_threshold=0.3,  # keep sparse for text
    )

    # Classifier
    clf = LinearSVC(random_state=42)

    pipe = Pipeline(steps=[
        ("prep", preprocessor),
        ("clf", clf),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    print("🔹 Training model...")
    pipe.fit(X_train, y_train)

    print("🔹 Evaluating...")
    y_pred = pipe.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")

    report_dict = classification_report(y_test, y_pred, output_dict=True)
    report_txt = classification_report(y_test, y_pred)

    # Save model
    joblib.dump(pipe, MODEL_PATH)
    print("✅ Saved model to:", MODEL_PATH)

    # Save metrics
    with open(os.path.join(METRICS_DIR, "metrics.json"), "w") as f:
        json.dump({"accuracy": acc, "labels": list(sorted(y.unique()))}, f, indent=2)

    with open(os.path.join(METRICS_DIR, "classification_report.txt"), "w") as f:
        f.write(report_txt)

    # Confusion matrix
    labels = sorted(y.unique())
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    plot_confusion_matrix(cm, labels, os.path.join(METRICS_DIR, "confusion_matrix.png"))

    print("✅ Wrote metrics to:", METRICS_DIR)
    print("Done.")

if __name__ == "__main__":
    main()