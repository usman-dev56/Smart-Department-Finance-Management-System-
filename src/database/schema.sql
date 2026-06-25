-- SDFMS Database Schema
PRAGMA foreign_keys = ON;

-- ============================================================
-- 1. DEPARTMENTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL,
    university_name TEXT NOT NULL,
    logo_path TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    receipt_prefix TEXT DEFAULT 'DEPT',
    next_receipt_number INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 2. ACADEMIC STRUCTURE
-- ============================================================

-- Sessions
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    session_name TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    UNIQUE(department_id, session_name)
);

-- Programs
CREATE TABLE IF NOT EXISTS programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    program_name TEXT NOT NULL,
    program_code TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    UNIQUE(department_id, program_code)
);

-- Shifts
CREATE TABLE IF NOT EXISTS shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    shift_name TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    UNIQUE(department_id, shift_name)
);

-- Sections
CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    section_name TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    UNIQUE(department_id, section_name)
);

-- ============================================================
-- 3. FUNDS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS funds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    fund_name TEXT NOT NULL,
    fund_description TEXT,
    fund_type TEXT DEFAULT 'General',
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    UNIQUE(department_id, fund_name)
);

-- ============================================================
-- 4. STUDENTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    roll_number TEXT NOT NULL UNIQUE,
    student_name TEXT NOT NULL,
    program_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL,
    semester INTEGER NOT NULL DEFAULT 1,
    section_id INTEGER,
    shift_id INTEGER,
    phone TEXT,
    email TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (program_id) REFERENCES programs(id),
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    FOREIGN KEY (section_id) REFERENCES sections(id),
    FOREIGN KEY (shift_id) REFERENCES shifts(id)
);

-- ============================================================
-- 5. CAMPAIGNS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    campaign_name TEXT NOT NULL,
    fund_id INTEGER NOT NULL,
    program_id INTEGER,
    session_id INTEGER,
    semester INTEGER,
    shift_id INTEGER,
    required_amount REAL NOT NULL DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (fund_id) REFERENCES funds(id),
    FOREIGN KEY (program_id) REFERENCES programs(id),
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    FOREIGN KEY (shift_id) REFERENCES shifts(id)
);

-- ============================================================
-- 6. PAYMENTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    receipt_number TEXT NOT NULL UNIQUE,
    campaign_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    payment_date DATE NOT NULL,
    payment_method TEXT DEFAULT 'Cash',
    received_by TEXT,
    qr_code_path TEXT,
    receipt_path TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- ============================================================
-- 7. EXPENSES TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    fund_id INTEGER NOT NULL,
    expense_title TEXT NOT NULL,
    expense_description TEXT,
    amount REAL NOT NULL,
    expense_date DATE NOT NULL,
    created_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (fund_id) REFERENCES funds(id)
);

-- ============================================================
-- 8. INDEXES FOR PERFORMANCE
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_students_roll_number ON students(roll_number);
CREATE INDEX IF NOT EXISTS idx_students_program ON students(program_id);
CREATE INDEX IF NOT EXISTS idx_students_session ON students(session_id);
CREATE INDEX IF NOT EXISTS idx_payments_receipt ON payments(receipt_number);
CREATE INDEX IF NOT EXISTS idx_payments_campaign ON payments(campaign_id);
CREATE INDEX IF NOT EXISTS idx_payments_student ON payments(student_id);
CREATE INDEX IF NOT EXISTS idx_campaigns_fund ON campaigns(fund_id);
CREATE INDEX IF NOT EXISTS idx_expenses_fund ON expenses(fund_id);