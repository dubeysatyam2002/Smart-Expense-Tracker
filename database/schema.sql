PRAGMA foreign_keys = ON;

-- =========================
-- Users table
-- =========================
-- Each login will be one row here
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    recovery_question TEXT,
    recovery_answer_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================
-- Accounts table
-- =========================
-- Each account belongs to a user
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    -- Each user can have 'Home', 'School', etc., but not duplicates
    UNIQUE (user_id, name)
);

-- =========================
-- Transactions table
-- =========================
-- Linked to accounts (and indirectly to user via accounts.user_id)
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
    amount REAL NOT NULL CHECK (amount > 0),
    description TEXT,
    category TEXT,
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);

-- =========================
-- Helpful indexes
-- =========================

-- Speed up date range queries
CREATE INDEX IF NOT EXISTS idx_transactions_date
    ON transactions(transaction_date);

-- Speed up lookups by account
CREATE INDEX IF NOT EXISTS idx_transactions_account_id
    ON transactions(account_id);

-- Speed up filtering by type (income/expense)
CREATE INDEX IF NOT EXISTS idx_transactions_type
    ON transactions(type);

-- Speed up fetching all accounts for a user
CREATE INDEX IF NOT EXISTS idx_accounts_user_id
    ON accounts(user_id);

-- Optional: if you often query by (user_id, name)
CREATE INDEX IF NOT EXISTS idx_accounts_user_id_name
    ON accounts(user_id, name);
