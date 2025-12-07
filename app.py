import streamlit as st
from datetime import date, timedelta
import pandas as pd

from config import APP_NAME, APP_ICON
from database.db_manager import DatabaseManager
from nlp.parser import NLPParser
from utils.data_processor import (
    transactions_to_dataframe,
    df_to_csv_bytes,
    df_to_excel_bytes,
)
from utils.visualizations import (
    create_income_expense_chart,
    create_category_pie_chart,
    create_spending_trend_chart,
)
from utils.pdf_generator import generate_pdf_report


# ---------- Initialize app ----------

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
)

st.title(f"{APP_ICON} {APP_NAME}")

# Connect to database
db = DatabaseManager()

# NLP parser
parser = NLPParser()


# ---------- Sidebar: Account selection & management ----------

st.sidebar.header("Accounts")

accounts = db.get_all_accounts()
selected_account = None

# --- Select existing account ---
if accounts:
    account_names = [a["name"] for a in accounts]
    selected_account_name = st.sidebar.selectbox(
        "Choose existing account",
        account_names,
        key="account_select",
    )

    selected_account = next(
        (a for a in accounts if a["name"] == selected_account_name), None
    )
else:
    st.sidebar.info("No accounts found. Please create one below.")

# --- Create new account ---
st.sidebar.subheader("Create New Account")

with st.sidebar.form("add_account_form"):
    new_acc_name = st.text_input("Account Name")
    new_acc_desc = st.text_area("Description")
    submitted = st.form_submit_button("Create Account")

    if submitted:
        if new_acc_name.strip():
            acc_id = db.add_account(new_acc_name.strip(), new_acc_desc.strip())
            if acc_id:
                st.sidebar.success("Account created! Please refresh or rerun.")
            else:
                st.sidebar.error("Account name already exists.")
        else:
            st.sidebar.error("Account name required.")

# --- Delete account ---
st.sidebar.subheader("Delete Account")

if accounts:
    del_acc_name = st.sidebar.selectbox(
        "Select account to delete",
        account_names,
        key="delete_account_select",
    )
    confirm_delete = st.sidebar.checkbox(
        f"I understand this will delete '{del_acc_name}' and all its transactions.",
        key="confirm_delete_account",
    )
    if st.sidebar.button("Delete Selected Account"):
        if confirm_delete:
            acc_to_delete = next(a for a in accounts if a["name"] == del_acc_name)
            db.delete_account(acc_to_delete["id"])
            st.sidebar.success(f"Deleted account '{del_acc_name}'.")
            st.rerun()
        else:
            st.sidebar.error("Please tick the confirmation checkbox before deleting.")
else:
    st.sidebar.info("No accounts to delete.")


# ---------- Main UI ----------

if selected_account:

    # ---------- All Accounts Overview ----------
    with st.expander("All Accounts Overview", expanded=False):
        if not accounts:
            st.info("No accounts available.")
        else:
            rows = []
            for acc in accounts:
                acc_summary = db.get_account_summary(account_id=acc["id"])
                rows.append(
                    {
                        "Account": acc["name"],
                        "Total Income": acc_summary["total_income"],
                        "Total Expenses": acc_summary["total_expense"],
                        "Balance": acc_summary["balance"],
                    }
                )
            overview_df = pd.DataFrame(rows)
            st.dataframe(overview_df)

    # ---------- Account Summary Section ----------
    summary = db.get_account_summary(account_id=selected_account["id"])

    st.subheader("Account Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹ {summary['total_income']:.2f}")
    col2.metric("Total Expenses", f"₹ {summary['total_expense']:.2f}")

    balance = summary["balance"]
    delta = summary["total_income"] - summary["total_expense"]

    # Balance: green if positive, red if negative
    col3.metric(
        "Balance",
        f"₹ {balance:.2f}",
        delta=delta,
        delta_color="normal",  # Streamlit auto green/red based on sign
    )

    # ---------- Transaction Input ----------
    st.subheader(f"Add Transaction to: **{selected_account['name']}**")

    text_input = st.text_area(
        "Enter transaction in natural language:",
        placeholder="Example: bought milk for 50 rupees yesterday",
    )

    if st.button("Parse & Add Transaction"):
        if not text_input.strip():
            st.error("Please enter some text.")
        else:
            try:
                parsed = parser.parse(text_input)

                # Insert into DB
                db.add_transaction(
                    account_id=selected_account["id"],
                    trans_type=parsed.trans_type,
                    amount=parsed.amount,
                    description=parsed.description,
                    category=parsed.category or "",
                    transaction_date=parsed.transaction_date.isoformat(),
                )

                st.success(
                    f"Added {parsed.trans_type} of {parsed.amount} "
                    f"for '{parsed.description}'"
                )
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    # ---------- Transaction list with filters ----------
    st.subheader("Recent Transactions")

    # Default filter range: last 30 days
    default_start = date.today() - timedelta(days=30)
    default_end = date.today()

    with st.expander("Filters", expanded=True):
        colf1, colf2, colf3 = st.columns(3)

        with colf1:
            date_range = st.date_input(
                "Date range",
                value=(default_start, default_end),
            )

        with colf2:
            type_option = st.selectbox(
                "Transaction type",
                ["All", "Income", "Expense"],
            )

        with colf3:
            category_filter_text = st.text_input(
                "Category (optional)",
                placeholder="e.g. Groceries, Income",
            )

    # Normalize date range
    start_date_str = None
    end_date_str = None

    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
        start_date_str = start_date.isoformat()
        end_date_str = end_date.isoformat()
    elif isinstance(date_range, date):
        start_date_str = date_range.isoformat()
        end_date_str = date_range.isoformat()

    # Normalize type filter
    trans_type_filter = None
    if type_option == "Income":
        trans_type_filter = "income"
    elif type_option == "Expense":
        trans_type_filter = "expense"

    # Normalize category filter
    category_filter = (
        category_filter_text.strip() if category_filter_text.strip() else None
    )

    # Fetch filtered transactions
    txns = db.get_transactions(
        account_id=selected_account["id"],
        start_date=start_date_str,
        end_date=end_date_str,
        trans_type=trans_type_filter,
        category=category_filter,
    )

    # ---------- Table + Downloads ----------
    if not txns:
        st.info("No transactions found for selected filters.")
        df = transactions_to_dataframe(txns)  # empty DF
    else:
        st.dataframe(txns)

        df = transactions_to_dataframe(txns)

        st.markdown("### Download Data")

        # Summary for current filtered range
        filtered_summary = db.get_account_summary(
            account_id=selected_account["id"],
            start_date=start_date_str,
            end_date=end_date_str,
        )

        col_d1, col_d2, col_d3 = st.columns(3)

        with col_d1:
            csv_bytes = df_to_csv_bytes(df)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv_bytes,
                file_name=f"{selected_account['name']}_transactions.csv",
                mime="text/csv",
            )

        with col_d2:
            excel_bytes = df_to_excel_bytes(df)
            st.download_button(
                label="⬇️ Download Excel (.xlsx)",
                data=excel_bytes,
                file_name=f"{selected_account['name']}_transactions.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
            )

        with col_d3:
            pdf_bytes = generate_pdf_report(
                account_name=selected_account["name"],
                summary=filtered_summary,
                df=df,
                start_date=start_date_str,
                end_date=end_date_str,
            )
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes,
                file_name=f"{selected_account['name']}_report.pdf",
                mime="application/pdf",
            )

    # ---------- Dashboard: Charts ----------
    st.subheader("Dashboard")

    df = transactions_to_dataframe(txns)

    if df.empty:
        st.info("Not enough data to display charts. Add some transactions first.")
    else:
        colc1, colc2 = st.columns(2)

        fig1 = create_income_expense_chart(df)
        if fig1 is not None:
            colc1.plotly_chart(fig1, use_container_width=True)

        fig2 = create_category_pie_chart(df)
        if fig2 is not None:
            colc2.plotly_chart(fig2, use_container_width=True)

        fig3 = create_spending_trend_chart(df)
        if fig3 is not None:
            st.plotly_chart(fig3, use_container_width=True)

    # ---------- Manage Transactions ----------
    st.subheader("Manage Transactions")

    if not txns:
        st.info("No transactions available to edit or delete.")
    else:
        # ----- Edit Transaction -----
        st.markdown("#### Edit Transaction")

        # Build simple list of (id, label) for selection
        txn_options = []
        for t in txns:
            label = (
                f"[{t['id']}] {t['transaction_date']} | {t['type']} | "
                f"{t['amount']} | {t.get('description', '')}"
            )
            txn_options.append((t["id"], label))

        txn_labels = [opt[1] for opt in txn_options]
        selected_label = st.selectbox(
            "Choose a transaction to edit",
            txn_labels,
            key="edit_txn_select",
        )

        # Get the selected transaction id + dict
        selected_txn_id = next(
            tid for tid, lbl in txn_options if lbl == selected_label
        )
        selected_txn = next(t for t in txns if t["id"] == selected_txn_id)

        with st.form("edit_txn_form"):
            # Type
            new_type = st.selectbox(
                "Type",
                ["income", "expense"],
                index=0 if selected_txn["type"] == "income" else 1,
            )

            # Amount
            new_amount = st.number_input(
                "Amount",
                min_value=0.01,
                value=float(selected_txn["amount"]),
                step=1.0,
            )

            # Description
            new_desc = st.text_input(
                "Description",
                value=selected_txn.get("description", "") or "",
            )

            # Category
            new_category = st.text_input(
                "Category",
                value=selected_txn.get("category", "") or "",
            )

            # Date
            try:
                current_date_obj = date.fromisoformat(selected_txn["transaction_date"])
            except Exception:
                current_date_obj = date.today()

            new_date = st.date_input(
                "Transaction Date",
                value=current_date_obj,
            )

            edit_submit = st.form_submit_button("Save Changes")

            if edit_submit:
                try:
                    db.update_transaction(
                        transaction_id=selected_txn_id,
                        trans_type=new_type,
                        amount=float(new_amount),
                        description=new_desc,
                        category=new_category,
                        transaction_date=new_date.isoformat(),
                    )
                    st.success(f"Updated transaction ID {selected_txn_id}.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating transaction: {e}")

        # ----- Delete Transaction -----
        st.markdown("#### Delete Transaction")

        with st.form("delete_txn_form"):
            del_id = st.number_input(
                "Enter Transaction ID to delete",
                min_value=1,
                step=1,
                help="Use the ID shown in the transactions table above.",
            )
            del_submit = st.form_submit_button("Delete Transaction")

            if del_submit:
                try:
                    db.delete_transaction(int(del_id))
                    st.success(
                        f"Deleted transaction with ID {int(del_id)} (if it existed)."
                    )
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting transaction: {e}")

else:
    st.warning("Please select an account or create one from the sidebar.")
