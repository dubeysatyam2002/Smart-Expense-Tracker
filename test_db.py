from database.db_manager import DatabaseManager

def main() -> None:
    db = DatabaseManager()

    # Try adding some sample accounts
    print("Adding sample accounts...")
    db.add_account("Home", "Personal expenses")
    db.add_account("School", "Education related")
    db.add_account("Friends", "Money lent to friends")

    print("\nCurrent accounts in database:")
    accounts = db.get_all_accounts()
    for acc in accounts:
        print(f"- [{acc['id']}] {acc['name']} :: {acc['description']}")

    print("\nDelete test: deleting 'Friends' account if present...")
    # Find account with name 'Friends'
    friends = [a for a in accounts if a["name"] == "Friends"]
    if friends:
        db.delete_account(friends[0]["id"])
        print("Deleted 'Friends' account.")

    print("\nAccounts after delete:")
    for acc in db.get_all_accounts():
        print(f"- [{acc['id']}] {acc['name']} :: {acc['description']}")


if __name__ == "__main__":
    main()
