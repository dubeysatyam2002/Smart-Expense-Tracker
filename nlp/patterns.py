"""
Regex patterns and keyword lists used by the NLP parser.
"""

import re

# ---------- Amount detection patterns ----------

AMOUNT_PATTERNS = [
    r"₹\s*(\d+(?:,\d+)*(?:\.\d+)?)",           # ₹500 or ₹5,000
    r"rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)",       # Rs 500 or Rs. 5,000
    r"(\d+(?:,\d+)*(?:\.\d+)?)\s*rupees?",     # 500 rupees
    r"(\d+(?:,\d+)*(?:\.\d+)?)\s*rs\.?",       # 500 rs
    r"\b(\d+(?:,\d+)*(?:\.\d+)?)\b",           # plain number (fallback)
]

# Pre-compiled regex objects for speed
AMOUNT_REGEXES = [re.compile(pat, re.IGNORECASE) for pat in AMOUNT_PATTERNS]

# ---------- Transaction type keywords ----------

INCOME_KEYWORDS = [
    "got",
    "received",
    "added",
    "credited",
    "salary",
    "income",
    "earned",
    "deposit",
    "refund",
    "bonus",
    "payment received",
]

EXPENSE_KEYWORDS = [
    "spent",
    "bought",
    "purchased",
    "paid",
    "expense",
    "cost",
    "bill",
    "fee",
    "withdrawal",
    "debit",
    "shopping",
]

# ---------- Very simple category keyword mapping ----------

CATEGORY_KEYWORDS = {
    "Groceries": ["milk", "vegetable", "vegetables", "fruits", "bread", "grocery"],
    "Education": ["book", "textbook", "tuition", "course", "class", "school", "college"],
    "Utilities": ["electricity", "water", "gas", "internet", "wifi", "mobile bill", "phone bill"],
    "Transport": ["bus", "taxi", "cab", "auto", "metro", "train", "fuel", "petrol", "diesel"],
    "Entertainment": ["movie", "netflix", "prime", "spotify", "game", "games"],
    "Income": ["salary", "stipend", "allowance", "bonus", "refund", "interest"],
}
