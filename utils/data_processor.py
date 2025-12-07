"""
Data processing helpers: convert DB rows to pandas DataFrame and
prepare them for visualizations and analysis.
"""

from typing import List, Dict, Any
from io import BytesIO

import pandas as pd


def transactions_to_dataframe(transactions: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Convert a list of transaction dictionaries (from DatabaseManager)
    into a pandas DataFrame with proper dtypes.
    """
    if not transactions:
        return pd.DataFrame()

    df = pd.DataFrame(transactions)

    # Ensure transaction_date is a datetime column
    if "transaction_date" in df.columns:
        df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    # Fill missing categories with "Uncategorized"
    if "category" in df.columns:
        df["category"] = df["category"].fillna("Uncategorized")
        df.loc[df["category"] == "", "category"] = "Uncategorized"

    return df


def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """
    Convert a DataFrame to UTF-8 CSV bytes (no index).
    """
    return df.to_csv(index=False).encode("utf-8")


def df_to_excel_bytes(df: pd.DataFrame) -> bytes:
    """
    Convert a DataFrame to an in-memory Excel file (.xlsx) and return bytes.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Transactions")
    return output.getvalue()
