import os
import sqlite3
from typing import Optional, List, Dict, Any


DB_PATH = os.path.join("data", "expenses.db")
SCHEMA_PATH = os.path.join("database", "schema.sql")


class DatabaseManager:
    """
    Handles all DB operations:
    - users
    - accounts (per user)
    - transactions
    """

    def __init__(self, db_path: str = DB_PATH, schema_path: str = SCHEMA_PATH) -> None:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")

        self._initialize_db(schema_path)

    # ---------- Initialization ----------

    def _initialize_db(self, schema_path: str) -> None:
        """Create tables if they don't exist."""
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        self.conn.executescript(schema_sql)
        self.conn.commit()

    # ---------- User management ----------

    def create_user(
        self,
        username: str,
        password_hash: str,
        recovery_question: Optional[str] = None,
        recovery_answer_hash: Optional[str] = None,
    ) -> Optional[int]:
        """
        Create a new user.
        Returns user_id if created, or None if username already exists.
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                INSERT INTO users (username, password_hash, recovery_question, recovery_answer_hash)
                VALUES (?, ?, ?, ?)
                """,
                (username, password_hash, recovery_question, recovery_answer_hash),
            )
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError:
            # UNIQUE(username) violated
            return None

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,),
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,),
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def update_user_password(self, user_id: int, new_password_hash: str) -> None:
        """
        Update the password hash for a user (used by 'forgot password' flow).
        """
        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE users
            SET password_hash = ?
            WHERE id = ?
            """,
            (new_password_hash, user_id),
        )
        self.conn.commit()

    # ---------- Account management (per user) ----------

    def add_account(self, user_id: int, name: str, description: str = "") -> Optional[int]:
        """
        Create an account for a given user.
        Returns account_id if created, or None if (user_id, name) already exists.
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                INSERT INTO accounts (user_id, name, description)
                VALUES (?, ?, ?)
                """,
                (user_id, name, description),
            )
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError:
            return None

    def get_all_accounts(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Return all accounts belonging to this user.
        """
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT id, user_id, name, description, created_at
            FROM accounts
            WHERE user_id = ?
            ORDER BY created_at
            """,
            (user_id,),
        )
        rows = cur.fetchall()
        return [dict(r) for r in rows]

    def delete_account(self, account_id: int, user_id: Optional[int] = None) -> None:
        """
        Delete an account (and cascade-delete its transactions).
        If user_id is given, ensures the account belongs to that user.
        """
        cur = self.conn.cursor()
        if user_id is not None:
            cur.execute(
                "DELETE FROM accounts WHERE id = ? AND user_id = ?",
                (account_id, user_id),
            )
        else:
            cur.execute(
                "DELETE FROM accounts WHERE id = ?",
                (account_id,),
            )
        self.conn.commit()

    # ---------- Transaction management ----------

    def add_transaction(
        self,
        account_id: int,
        trans_type: str,
        amount: float,
        description: str,
        category: str,
        transaction_date: str,
    ) -> int:
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO transactions (
                account_id, type, amount, description, category, transaction_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (account_id, trans_type, amount, description, category, transaction_date),
        )
        self.conn.commit()
        return cur.lastrowid

    def get_transactions(
        self,
        account_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trans_type: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch transactions for a given account with optional filters.
        """
        query = [
            "SELECT id, account_id, type, amount, description, category,",
            "       transaction_date, created_at",
            "FROM transactions",
            "WHERE account_id = ?",
        ]
        params: List[Any] = [account_id]

        if start_date is not None:
            query.append("AND transaction_date >= ?")
            params.append(start_date)

        if end_date is not None:
            query.append("AND transaction_date <= ?")
            params.append(end_date)

        if trans_type is not None:
            query.append("AND type = ?")
            params.append(trans_type)

        if category is not None:
            query.append("AND LOWER(category) = LOWER(?)")
            params.append(category)

        query.append("ORDER BY transaction_date DESC, id DESC")

        sql = " ".join(query)
        cur = self.conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        return [dict(r) for r in rows]

    def update_transaction(
        self,
        transaction_id: int,
        trans_type: str,
        amount: float,
        description: str,
        category: str,
        transaction_date: str,
    ) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE transactions
            SET type = ?,
                amount = ?,
                description = ?,
                category = ?,
                transaction_date = ?
            WHERE id = ?
            """,
            (trans_type, amount, description, category, transaction_date, transaction_id),
        )
        self.conn.commit()

    def delete_transaction(self, transaction_id: int) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,),
        )
        self.conn.commit()

    # ---------- Summary / analytics ----------

    def get_account_summary(
        self,
        account_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, float]:
        """
        Calculate total income, total expense, and balance for an account.
        Optional date range filter.
        """
        conditions = ["account_id = ?"]
        params: List[Any] = [account_id]

        if start_date is not None:
            conditions.append("transaction_date >= ?")
            params.append(start_date)

        if end_date is not None:
            conditions.append("transaction_date <= ?")
            params.append(end_date)

        where_clause = " AND ".join(conditions)

        sql = f"""
            SELECT
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS total_income,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS total_expense
            FROM transactions
            WHERE {where_clause}
        """

        cur = self.conn.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()

        total_income = row["total_income"] if row["total_income"] is not None else 0.0
        total_expense = row["total_expense"] if row["total_expense"] is not None else 0.0

        return {
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "balance": float(total_income - total_expense),
        }

    def close(self) -> None:
        self.conn.close()
