"""
Global configuration settings for the Smart Expense Tracker project.
"""

import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database file path
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "expenses.db")

# Streamlit UI settings
APP_NAME = "Smart Expense Tracker"
APP_ICON = "💰"
