import pandas as pd
import numpy as np

def check_row_count_anomaly(conn, threshold=2.0):
    history_counts = conn.execute("""
        SELECT CAST(created_at AS DATE) as dt, COUNT(*) as cnt
        FROM daily_transactions
        GROUP BY dt
    """).df()["cnt"]

    today_count = conn.execute("SELECT COUNT(*) as cnt FROM today_transactions").fetchone()[0]

    mean = history_counts.mean()
    std = history_counts.std() if len(history_counts) > 1 else 1.0

    z_score = (today_count - mean) / std if std != 0 else 0
    is_anomaly = abs(z_score) > threshold

    return {
        "check": "Row Count Anomaly",
        "is_anomaly": bool(is_anomaly),
        "z_score": round(float(z_score), 2),
        "today_count": int(today_count),
        "historical_mean": round(float(mean), 2)
    }

def check_null_rates(conn, threshold_pct=0.10):
    df_today = conn.execute("SELECT * FROM today_transactions").df()
    total_rows = len(df_today)
    null_anomalies = {}

    if total_rows == 0:
        return {"check": "Null Rate Check", "is_anomaly": True, "details": "Table is completely empty!"}

    for col in df_today.columns:
        null_count = df_today[col].isnull().sum()
        null_pct = null_count / total_rows
        if null_pct > threshold_pct:
            null_anomalies[col] = {
                "null_count": int(null_count),
                "null_pct": f"{round(float(null_pct * 100), 2)}%"
            }

    return {
        "check": "Null Rate Check",
        "is_anomaly": len(null_anomalies) > 0,
        "anomalies": null_anomalies
    }

def check_schema_drift(conn, expected_schema):
    today_schema_info = conn.execute("DESCRIBE today_transactions").fetchall()
    today_cols = {row[0]: row[1] for row in today_schema_info}

    missing_cols = set(expected_schema.keys()) - set(today_cols.keys())
    new_cols = set(today_cols.keys()) - set(expected_schema.keys())

    return {
        "check": "Schema Drift Check",
        "is_anomaly": len(missing_cols) > 0 or len(new_cols) > 0,
        "missing_columns": list(missing_cols),
        "new_columns": list(new_cols)
    }

def run_all_checks(conn):
    expected_schema = {
        "symbol": "VARCHAR",
        "lastPrice": "DOUBLE",
        "volume": "DOUBLE",
        "count": "BIGINT",
        "priceChangePercent": "DOUBLE",
        "created_at": "TIMESTAMP"
    }

    return [
        check_row_count_anomaly(conn),
        check_null_rates(conn),
        check_schema_drift(conn, expected_schema)
    ]