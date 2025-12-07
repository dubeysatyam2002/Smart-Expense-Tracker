"""
PDF report generation using ReportLab.
"""

from typing import Dict, Any, Optional
from io import BytesIO

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_pdf_report(
    account_name: str,
    summary: Dict[str, Any],
    df: pd.DataFrame,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> bytes:
    """
    Create a PDF report as bytes.

    - account_name: name of the selected account
    - summary: dict with keys total_income, total_expense, balance, transaction_count
    - df: transactions dataframe (already filtered by date/type/category)
    - start_date, end_date: filter range (YYYY-MM-DD strings) for display
    """

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    elements = []

    # ----- Title -----
    title_text = f"Smart Expense Tracker - Report ({account_name})"
    elements.append(Paragraph(title_text, styles["Title"]))
    elements.append(Spacer(1, 12))

    # ----- Date Range -----
    if start_date and end_date:
        date_range_text = f"Date Range: {start_date} to {end_date}"
    else:
        date_range_text = "Date Range: All available data"

    elements.append(Paragraph(date_range_text, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # ----- Summary -----
    elements.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    summary_lines = [
        f"Total Income: ₹ {summary.get('total_income', 0):.2f}",
        f"Total Expenses: ₹ {summary.get('total_expense', 0):.2f}",
        f"Balance: ₹ {summary.get('balance', 0):.2f}",
        f"Number of Transactions: {summary.get('transaction_count', 0)}",
    ]
    for line in summary_lines:
        elements.append(Paragraph(line, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # ----- Transactions Table -----
    elements.append(Paragraph("<b>Transactions</b>", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    if df.empty:
        elements.append(Paragraph("No transactions for the selected filters.", styles["Italic"]))
    else:
        # Limit rows if too many, to avoid huge PDFs (optional)
        max_rows = 100
        df_display = df.copy()
        if len(df_display) > max_rows:
            df_display = df_display.head(max_rows)

        # Select and rename columns for the report
        cols_to_use = []
        for col in ["transaction_date", "type", "amount", "description", "category"]:
            if col in df_display.columns:
                cols_to_use.append(col)

        table_df = df_display[cols_to_use].copy()

        # Convert to string for safety
        table_df["transaction_date"] = table_df["transaction_date"].dt.strftime("%Y-%m-%d")

        data = [ [col.replace("_", " ").title() for col in table_df.columns] ]
        for _, row in table_df.iterrows():
            data.append([str(v) for v in row.values])

        table = Table(data, repeatRows=1)
        table_style = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ]
        )
        table.setStyle(table_style)
        elements.append(table)

        if len(df.index) > max_rows:
            elements.append(Spacer(1, 6))
            elements.append(
                Paragraph(
                    f"Showing first {max_rows} rows out of {len(df.index)} transactions.",
                    styles["Italic"],
                )
            )

    # Build the PDF
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
