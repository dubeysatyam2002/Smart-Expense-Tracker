"""
Visualization helpers using Plotly.
"""

from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_income_expense_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Bar chart comparing total income vs total expense.
    """
    if df.empty or "type" not in df.columns or "amount" not in df.columns:
        return None

    grouped = (
        df.groupby("type", as_index=False)["amount"]
        .sum()
        .query("type in ['income', 'expense']")
    )

    if grouped.empty:
        return None

    fig = px.bar(
        grouped,
        x="type",
        y="amount",
        title="Income vs Expense",
        text="amount",
    )
    fig.update_layout(xaxis_title="Type", yaxis_title="Amount")
    fig.update_traces(texttemplate="₹%{text:.2f}", textposition="outside")
    return fig


def create_category_pie_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Pie chart of expenses by category (only expense rows).
    """
    if df.empty or "type" not in df.columns or "amount" not in df.columns:
        return None

    expenses = df[df["type"] == "expense"].copy()
    if expenses.empty:
        return None

    grouped = (
        expenses.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )

    fig = px.pie(
        grouped,
        names="category",
        values="amount",
        title="Spending by Category (Expenses)",
    )
    return fig


def create_spending_trend_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Line chart showing total income and expense over time.
    """
    if df.empty or "transaction_date" not in df.columns:
        return None

    grouped = (
        df.groupby(["transaction_date", "type"], as_index=False)["amount"]
        .sum()
        .query("type in ['income', 'expense']")
    )

    if grouped.empty:
        return None

    fig = px.line(
        grouped,
        x="transaction_date",
        y="amount",
        color="type",
        markers=True,
        title="Income & Expense Over Time",
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Amount")
    return fig
