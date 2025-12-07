"""
NLP parser: converts natural language text into structured transaction data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Literal
from datetime import date, timedelta

import re
import spacy
from dateutil import parser as date_parser

from .patterns import AMOUNT_REGEXES, INCOME_KEYWORDS, EXPENSE_KEYWORDS, CATEGORY_KEYWORDS


TransactionType = Literal["income", "expense"]


@dataclass
class ParsedTransaction:
    """
    Result of parsing a natural language transaction sentence.
    """

    trans_type: TransactionType
    amount: float
    description: str
    category: Optional[str]
    transaction_date: date


class NLPParser:
    """
    High-level NLP parser that uses:
    - regex for amounts
    - keyword rules for income/expense
    - dateutil for dates
    - optional spaCy for tokenization later
    """

    def __init__(self, model_name: str = "en_core_web_sm") -> None:
        # Load spaCy model for future advanced parsing.
        # We keep it simple for now (main logic uses regex/keywords).
        try:
            self.nlp = spacy.load(model_name)
        except OSError as exc:
            raise RuntimeError(
                f"spaCy model '{model_name}' is not installed. "
                f"Run: python -m spacy download {model_name}"
            ) from exc

    # ---------- Public API ----------

    def parse(self, text: str) -> ParsedTransaction:
        """
        Main entry point.
        Input: raw user text like "bought pen for 5 rupees yesterday"
        Output: ParsedTransaction object.
        """
        if not text or not text.strip():
            raise ValueError("Input text is empty")

        original_text = text
        text = text.strip().lower()

        amount = self._extract_amount(text)
        trans_type = self._detect_transaction_type(text)
        tx_date = self._extract_date(text)
        description = self._extract_description(original_text, amount, tx_date, trans_type)
        category = self._detect_category(description or original_text)

        return ParsedTransaction(
            trans_type=trans_type,
            amount=amount,
            description=description,
            category=category,
            transaction_date=tx_date,
        )

    # ---------- Internal helpers ----------

    def _extract_amount(self, text: str) -> float:
        """
        Extract the amount from text.

        Supports:
        - Normal patterns via AMOUNT_REGEXES (₹500, 5,000, 50 rupees, etc.)
        - Multiplicative patterns like:
          "bought 2 shirts of 300 each" -> 600
          "got 3 books for 150 each"   -> 450
        """

        # 1) Try "quantity ... of/for ... each" style, e.g. "2 shirts of 300 each"
        mult_match = re.search(
            r"(\d+(?:\.\d+)?)\s+\w+(?:\s+\w+)*?\s+(?:of|for)\s+(\d+(?:,\d+)*(?:\.\d+)?)\s+each",
            text,
        )
        if mult_match:
            qty_str, price_str = mult_match.groups()
            try:
                qty = float(qty_str)
                price = float(price_str.replace(",", ""))
                return qty * price
            except ValueError:
                # If anything goes wrong, fall back to normal patterns
                pass

        # 2) Fallback to predefined amount regexes
        # If "each" is present, we try to avoid the very generic standalone-number
        # pattern (last in AMOUNT_REGEXES) so we don't pick just "2" in "2 shirts of 300 each".
        has_each = "each" in text

        for idx, regex in enumerate(AMOUNT_REGEXES):
            # Skip plain-number pattern when "each" is in text and this is the last pattern
            if has_each and idx == len(AMOUNT_REGEXES) - 1:
                continue

            match = regex.search(text)
            if match:
                number_str = match.group(1)
                # Remove commas like "5,000"
                number_str = number_str.replace(",", "")
                try:
                    return float(number_str)
                except ValueError:
                    continue

        raise ValueError("Could not detect any amount in the text")

    def _detect_transaction_type(self, text: str) -> TransactionType:
        """
        Decide if it's income or expense based on keywords.
        Default: 'expense' if ambiguous.
        """
        for kw in INCOME_KEYWORDS:
            if kw in text:
                return "income"

        for kw in EXPENSE_KEYWORDS:
            if kw in text:
                return "expense"

        # If no keyword matched, default to expense
        return "expense"

    def _extract_date(self, text: str) -> date:
        """
        Extract a date from the text.
        Supported examples:
        - "today", "yesterday"
        - "on 5 dec", "on 05/12/2024", "on 2024-12-05"
        - "2 days ago"
        If nothing is found, returns today's date.
        """
        today = date.today()

        # Relative keywords
        if "today" in text:
            return today
        if "yesterday" in text:
            return today - timedelta(days=1)

        # "X days ago"
        m = re.search(r"(\d+)\s+days?\s+ago", text)
        if m:
            days = int(m.group(1))
            return today - timedelta(days=days)

        # Look for "on <date expression>"
        m = re.search(r"on\s+(.+)", text)
        if m:
            date_part = m.group(1)
            # Try to stop at " for " or " rupees " etc
            date_part = re.split(r"\bfor\b|\brupees?\b|\brs\.?\b", date_part)[0].strip()
            try:
                dt = date_parser.parse(date_part, dayfirst=True).date()
                return dt
            except (ValueError, OverflowError):
                pass

        # If nothing else worked, use today's date
        return today

    def _detect_category(self, text: str) -> Optional[str]:
        """
        Very simple rule-based category detection using CATEGORY_KEYWORDS.
        """
        lowered = text.lower()
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in lowered:
                    return cat
        return None

    def _extract_description(
        self,
        original_text: str,
        amount: float,
        tx_date: date,
        trans_type: TransactionType,
    ) -> str:
        """
        Derive a simple description by removing amounts, currency words,
        and obvious keywords. This is a heuristic, not perfect.
        """
        text = original_text.lower()

        # Remove numbers related to amount
        amount_str = str(int(amount)) if amount.is_integer() else str(amount)
        text = text.replace(amount_str, " ")

        # Remove common currency / filler tokens
        for token in ["rupees", "rupee", "rs.", "rs", "₹", "each"]:
            text = text.replace(token, " ")

        # Remove transaction keywords
        for kw in INCOME_KEYWORDS + EXPENSE_KEYWORDS:
            text = text.replace(kw, " ")

        # Remove relative date words
        for t in ["today", "yesterday", "ago"]:
            text = text.replace(t, " ")

        text = re.sub(r"\bon\b", " ", text)  # remove 'on' used for dates
        text = re.sub(r"\s+", " ", text).strip()

        # Very small cleanup of starting words like 'for', 'to'
        text = re.sub(r"^(for|to)\s+", "", text)

        # If after cleanup nothing remains, fallback to original text
        if not text:
            return original_text.strip()

        return text
