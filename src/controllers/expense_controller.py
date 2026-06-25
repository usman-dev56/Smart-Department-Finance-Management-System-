# src/controllers/expense_controller.py
"""Expense Controller - Handles expense operations"""
from src.database.db_manager import get_db
from src.models.expense import Expense
from src.models.fund import Fund
from src.utils.helpers import today_str


def add_expense(data):
    """Add a new expense"""
    db = get_db()
    
    # Validate fund exists
    fund = Fund.find(data["fund_id"])
    if not fund:
        raise ValueError("Fund not found")
    
    expense_data = {
        "department_id": data.get("department_id", 1),
        "fund_id": data["fund_id"],
        "expense_title": data["expense_title"].strip(),
        "expense_description": data.get("expense_description", ""),
        "amount": float(data["amount"]),
        "expense_date": data.get("expense_date", today_str()),
        "created_by": data.get("created_by", "Admin")
    }
    return db.insert("expenses", expense_data)


def get_all_expenses(department_id=1, fund_id=None):
    """Get all expenses with optional fund filter"""
    db = get_db()
    if fund_id:
        return db.fetchall(
            """SELECT e.*, f.fund_name 
               FROM expenses e
               LEFT JOIN funds f ON e.fund_id = f.id
               WHERE e.department_id = ? AND e.fund_id = ?
               ORDER BY e.expense_date DESC""",
            (department_id, fund_id)
        )
    return db.fetchall(
        """SELECT e.*, f.fund_name 
           FROM expenses e
           LEFT JOIN funds f ON e.fund_id = f.id
           WHERE e.department_id = ?
           ORDER BY e.expense_date DESC""",
        (department_id,)
    )


def get_expense_by_id(expense_id):
    """Get expense with details by ID"""
    db = get_db()
    return db.fetchone(
        """SELECT e.*, f.fund_name 
           FROM expenses e
           LEFT JOIN funds f ON e.fund_id = f.id
           WHERE e.id = ?""",
        (expense_id,)
    )


def update_expense(expense_id, data):
    """Update an expense"""
    db = get_db()
    expense_data = {}
    
    if "expense_title" in data:
        expense_data["expense_title"] = data["expense_title"].strip()
    if "expense_description" in data:
        expense_data["expense_description"] = data["expense_description"]
    if "amount" in data:
        expense_data["amount"] = float(data["amount"])
    if "expense_date" in data:
        expense_data["expense_date"] = data["expense_date"]
    if "fund_id" in data:
        expense_data["fund_id"] = data["fund_id"]
    
    if not expense_data:
        return False
    
    db.update("expenses", expense_data, "id = ?", (expense_id,))
    return True


def delete_expense(expense_id):
    """Delete an expense"""
    db = get_db()
    db.delete("expenses", "id = ?", (expense_id,))
    return True


def get_expenses_by_date_range(start_date, end_date, department_id=1):
    """Get expenses within a date range"""
    db = get_db()
    return db.fetchall(
        """SELECT e.*, f.fund_name 
           FROM expenses e
           LEFT JOIN funds f ON e.fund_id = f.id
           WHERE e.department_id = ? 
           AND e.expense_date BETWEEN ? AND ?
           ORDER BY e.expense_date DESC""",
        (department_id, start_date, end_date)
    )


def get_total_expenses_by_fund(fund_id):
    """Get total expenses for a specific fund"""
    db = get_db()
    result = db.fetchone(
        "SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE fund_id = ?",
        (fund_id,)
    )
    return result["total"] if result else 0


def get_expense_summary(department_id=1):
    """Get expense summary by fund"""
    db = get_db()
    return db.fetchall(
        """SELECT f.fund_name, COALESCE(SUM(e.amount), 0) as total
           FROM funds f
           LEFT JOIN expenses e ON f.id = e.fund_id AND e.department_id = ?
           WHERE f.department_id = ?
           GROUP BY f.id
           ORDER BY total DESC""",
        (department_id, department_id)
    )


def get_monthly_expense_summary(year, department_id=1):
    """Get monthly expense summary for a year"""
    db = get_db()
    return db.fetchall(
        """SELECT strftime('%m', expense_date) as month,
                  COALESCE(SUM(amount), 0) as total
           FROM expenses
           WHERE department_id = ? AND strftime('%Y', expense_date) = ?
           GROUP BY month
           ORDER BY month""",
        (department_id, str(year))
    )