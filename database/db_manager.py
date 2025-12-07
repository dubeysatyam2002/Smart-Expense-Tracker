"""
DatabaseManager: handles all SQLite operations for the expense tracker.
"""

import os
import sqlite3
from typing import List, Dict, Any, Optional
from datetime import date

from config import DB_PATH


def _dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> Dict[str, Any]:
    """
    Convert SQLite rows to dictionaries: {"column": value, ...}
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


class DatabaseManager:
    """
    Wrapper around SQLite for accounts and transactions.
    """

    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path
        # Ensure the data folder exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        # Initialize database schema (tables + indexes)
        self._initialize_database()

    # ---------- Internal helpers ----------

    def _get_connection(self) -> sqlite3.Connection:
        """
        Create a new SQLite connection.
        Row factory makes results come back as dictionaries.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = _dict_factory
        return conn

    def _initialize_database(self) -> None:
        """
        Run schema.sql to create tables and indexes if they don't exist.
        """
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        with self._get_connection() as conn:
            conn.executescript(schema_sql)

    # ---------- Account methods ----------

    def add_account(self, name: str, description: str = "") -> Optional[int]:
        """
        Create a new account.
        Returns the new account ID, or None if the name already exists.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO accounts (name, description)
                    VALUES (?, ?)
                    """,
                    (name, description),
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            # UNIQUE constraint failed (duplicate name)
            return None

    def get_all_accounts(self) -> List[Dict[str, Any]]:
        """
        Return all accounts as a list of dictionaries.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT id, name, description, created_at FROM accounts ORDER BY id;"
            )
            return cursor.fetchall()

    def delete_account(self, account_id: int) -> None:
        """
        Delete an account (and its transactions due to ON DELETE CASCADE).
        """
        with self._get_connection() as conn:
            conn.execute("DELETE FROM accounts WHERE id = ?;", (account_id,))

    # ---------- Transaction methods ----------

    def add_transaction(
        self,
        account_id: int,
        trans_type: str,
        amount: float,
        description: str = "",
        category: str = "",
        transaction_date: Optional[str] = None,
    ) -> int:
        """
        Add a new transaction (income or expense).
        transaction_date: 'YYYY-MM-DD' string. If None, today's date is used.
        Returns new transaction ID.
        """
        trans_type = trans_type.lower()
        if trans_type not in ("income", "expense"):
            raise ValueError("trans_type must be 'income' or 'expense'")

        if amount <= 0:
            raise ValueError("amount must be > 0")

        if transaction_date is None:
            transaction_date = date.today().isoformat()

        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO transactions (
                    account_id, type, amount, description, category, transaction_date
                )
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (account_id, trans_type, amount, description, category, transaction_date),
            )
            return cursor.lastrowid

    def get_transactions(
        self,
        account_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trans_type: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch transactions with optional filters.
        Dates are 'YYYY-MM-DD' strings.
        """
        query = """
            SELECT
                id, account_id, type, amount, description,
                category, transaction_date, created_at
            FROM transactions
            WHERE 1 = 1
        """
        params: List[Any] = []

        if account_id is not None:
            query += " AND account_id = ?"
            params.append(account_id)

        if start_date is not None:
            query += " AND transaction_date >= ?"
            params.append(start_date)

        if end_date is not None:
            query += " AND transaction_date <= ?"
            params.append(end_date)

        if trans_type is not None:
            query += " AND type = ?"
            params.append(trans_type.lower())

        if category is not None:
            query += " AND category = ?"
            params.append(category)

        query += " ORDER BY transaction_date ASC, id ASC;"

        with self._get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def update_transaction(
        self,
        transaction_id: int,
        *,
        trans_type: Optional[str] = None,
        amount: Optional[float] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        transaction_date: Optional[str] = None,
    ) -> None:
        """
        Update fields of a transaction.
        Only non-None arguments will be updated.
        """
        fields = []
        params: List[Any] = []

        if trans_type is not None:
            trans_type = trans_type.lower()
            if trans_type not in ("income", "expense"):
                raise ValueError("trans_type must be 'income' or 'expense'")
            fields.append("type = ?")
            params.append(trans_type)

        if amount is not None:
            if amount <= 0:
                raise ValueError("amount must be > 0")
            fields.append("amount = ?")
            params.append(amount)

        if description is not None:
            fields.append("description = ?")
            params.append(description)

        if category is not None:
            fields.append("category = ?")
            params.append(category)

        if transaction_date is not None:
            fields.append("transaction_date = ?")
            params.append(transaction_date)

        if not fields:
            # Nothing to update
            return

        params.append(transaction_id)
        set_clause = ", ".join(fields)

        query = f"UPDATE transactions SET {set_clause} WHERE id = ?;"

        with self._get_connection() as conn:
            conn.execute(query, params)

    def delete_transaction(self, transaction_id: int) -> None:
        """
        Delete a transaction by ID.
        """
        with self._get_connection() as conn:
            conn.execute("DELETE FROM transactions WHERE id = ?;", (transaction_id,))

    # ---------- Summary / analytics helpers ----------

    def get_account_summary(
        self,
        account_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Return summary for an account:
        - total_income
        - total_expense
        - balance
        - transaction_count
        """
        query = """
            SELECT
                COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) AS total_income,
                COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) AS total_expense,
                COUNT(*) AS transaction_count
            FROM transactions
            WHERE account_id = ?
        """
        params: List[Any] = [account_id]

        if start_date is not None:
            query += " AND transaction_date >= ?"
            params.append(start_date)

        if end_date is not None:
            query += " AND transaction_date <= ?"
            params.append(end_date)

        with self._get_connection() as conn:
            cursor = conn.execute(query, params)
            row = cursor.fetchone()

        total_income = row["total_income"]
        total_expense = row["total_expense"]
        balance = total_income - total_expense

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "transaction_count": row["transaction_count"],
        }
