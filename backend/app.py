from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib, os, sqlite3
from typing import List
from datetime import datetime
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), "decision_tree_expenses.pkl")
DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")

app = FastAPI(title="Smart Budgeting Agent API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        with open(os.path.join(os.path.dirname(__file__), "schema.sql"), "r") as f:
            conn.executescript(f.read())
        conn.commit()

# Load model
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"[WARN] Model failed to load: {e}")

def safe_predict(model, rec: dict):
    """
    Try several input formats so the model can predict no matter how it was saved:
    1) Pipeline that accepts list-of-dicts
    2) Estimator that accepts a pandas DataFrame
    3) Bare estimator that wants numeric 2D arrays (fallback on core numeric fields)
    """
    # 1) Try as list-of-dicts (Pipeline with DictVectorizer/ColumnTransformer)
    try:
        return model.predict([rec])[0]
    except Exception:
        pass

    # 2) Try as pandas DataFrame
    try:
        import pandas as pd  # local import to avoid issues if not installed
        df = pd.DataFrame([rec])
        return model.predict(df)[0]
    except Exception:
        pass

    # 3) Fallback: numeric-only, fixed order (amount, month, day, is_weekend)
    X = [[
        float(rec.get("amount", 0.0)),
        int(rec.get("month", 1)),
        int(rec.get("day", 1)),
        int(rec.get("is_weekend", 0))
    ]]
    return model.predict(X)[0]

def category_override(rec: dict, predicted):
    """
    Lightweight keyword rules to polish categories for demo purposes.
    Checks description/merchant/text for common vendors/contexts.
    Returns a string category.
    """
    txt = " ".join([
        str(rec.get("text", "")),
        str(rec.get("merchant", "")),
        str(rec.get("description", "")),
    ]).lower()

    rules = [
        ("Food", ["starbucks", "chipotle", "mcdonald", "mcdonald's", "kfc", "subway", "dunkin", "panera", "maestro", "maestro's", "restaurant", "grill", "cafe", "coffee"]),
        ("Transportation", ["uber", "lyft", "exxon", "shell", "chevron", "bp", "mobil", "toll", "metro", "bus", "subway card"]),
        ("Utilities", ["verizon", "at&t", "att", "t-mobile", "tmobile", "comcast", "xfinity", "spectrum", "internet", "electric", "water bill", "utility", "sewer"]),
        ("Shopping", ["amazon", "walmart", "target", "best buy", "ikea", "costco", "sam's", "sams"]),
        ("Entertainment", ["netflix", "spotify", "amc", "regal", "cinema", "fandango", "concert", "ticketmaster"]),
        ("Health", ["walgreens", "cvs", "rite aid", "pharmacy", "clinic", "dentist", "optical", "gym", "planet fitness"]),
    ]
    for cat, keys in rules:
        if any(k in txt for k in keys):
            return cat
    return str(predicted)

class TransactionIn(BaseModel):
    description: str = Field(..., min_length=2)
    merchant: str = Field(..., min_length=2)
    amount: float = Field(..., gt=0)
    payment_method: str

class TransactionOut(TransactionIn):
    id: int
    category: str
    created_at: str

class PredictIn(BaseModel):
    description: str
    merchant: str
    amount: float
    payment_method: str

class PredictOut(BaseModel):
    category: str

@app.on_event("startup")
def on_startup():
    if not os.path.exists(DB_PATH):
        init_db()
    # optional warmup
    if model:
        try:
            _ = safe_predict(model, {
                "text": "warmup",
                "amount": 10.0, "month": 1, "day": 1, "is_weekend": 0, "payment_method": "Cash"
            })
        except Exception as e:
            print("[WARN] Warmup failed:", e)

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": bool(model)}

@app.post("/predict", response_model=PredictOut)
def predict(payload: PredictIn):
    if model is None:
        raise HTTPException(500, "Model not loaded.")
    now = datetime.now()
    features = [{
        "text": f"{payload.description} {payload.merchant}",
        "amount": payload.amount,
        "month": now.month,
        "day": now.day,
        "is_weekend": 1 if now.weekday() >= 5 else 0,
        "payment_method": payload.payment_method
    }]
    try:
        pred = safe_predict(model, features[0])
        final_cat = category_override(features[0], pred)
        return {"category": final_cat}
    except Exception as e:
        raise HTTPException(500, f"Prediction failed: {e}")

@app.post("/transactions", response_model=TransactionOut)
def create_transaction(tx: TransactionIn):
    if model is None:
        raise HTTPException(500, "Model not loaded.")
    now = datetime.now()
    X = [{
        "text": f"{tx.description} {tx.merchant}",
        "amount": tx.amount,
        "month": now.month,
        "day": now.day,
        "is_weekend": 1 if now.weekday() >= 5 else 0,
        "payment_method": tx.payment_method
    }]
    try:
        category = category_override(X[0], safe_predict(model, X[0]))
    except Exception as e:
        raise HTTPException(500, f"Prediction failed: {e}")

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO transactions(description, merchant, amount, payment_method, category, created_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (tx.description, tx.merchant, tx.amount, tx.payment_method, str(category)))
        tx_id = cur.lastrowid
        conn.commit()
        cur.execute("SELECT * FROM transactions WHERE id = ?", (tx_id,))
        row = cur.fetchone()

    return {
        "id": row["id"], "description": row["description"], "merchant": row["merchant"],
        "amount": row["amount"], "payment_method": row["payment_method"],
        "category": row["category"], "created_at": row["created_at"]
    }

@app.get("/transactions", response_model=List[TransactionOut])
def list_transactions(limit: int = 50, offset: int = 0):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, description, merchant, amount, payment_method, category, created_at
            FROM transactions
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))
        rows = cur.fetchall()
    return [
        {
            "id": r["id"], "description": r["description"], "merchant": r["merchant"],
            "amount": r["amount"], "payment_method": r["payment_method"],
            "category": r["category"], "created_at": r["created_at"]
        }
        for r in rows
    ]