from datetime import date, timedelta

from database.db_manager import DatabaseManager


def main() -> None:
    db = DatabaseManager()

    # 1) Ensure we have (or create) a Home account
    accounts = db.get_all_accounts()
    home_account = next((a for a in accounts if a["name"] == "Home"), None)

    if home_account is None:
        home_id = db.add_account("Home", "Personal expenses")
        print(f"Created 'Home' account with id {home_id}")
        home_account = {"id": home_id, "name": "Home"}
    else:
        home_id = home_account["id"]
        print(f"Using existing 'Home' account with id {home_id}")

    # 2) Add some sample transactions
    today = date.today()
    yesterday = today - timedelta(days=1)

    print("\nAdding sample transactions...")
    db.add_transaction(
        account_id=home_id,
        trans_type="income",
        amount=5000,
        description="Monthly allowance",
        category="Income",
        transaction_date=today.isoformat(),
    )
    db.add_transaction(
        account_id=home_id,
        trans_type="expense",
        amount=50,
        description="Milk",
        category="Groceries",
        transaction_date=today.isoformat(),
    )
    db.add_transaction(
        account_id=home_id,
        trans_type="expense",
        amount=200,
        description="Vegetables",
        category="Groceries",
        transaction_date=yesterday.isoformat(),
    )

    # 3) Fetch and print all transactions for Home
    print("\nAll transactions for 'Home':")
    txns = db.get_transactions(account_id=home_id)
    for t in txns:
        print(
            f"- [{t['id']}] {t['transaction_date']} | {t['type']} | "
            f"{t['amount']} | {t['description']} ({t['category']})"
        )

    # 4) Show summary
    summary = db.get_account_summary(account_id=home_id)
    print("\nSummary for 'Home':")
    print(f"Total income : {summary['total_income']}")
    print(f"Total expense: {summary['total_expense']}")
    print(f"Balance      : {summary['balance']}")
    print(f"Transactions : {summary['transaction_count']}")


if __name__ == "__main__":
    main()
