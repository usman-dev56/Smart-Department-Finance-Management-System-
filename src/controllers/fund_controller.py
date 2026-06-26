# src/controllers/fund_controller.py
"""Fund Controller - Handles fund operations"""
from src.database.db_manager import get_db
from src.models.fund import Fund
from src.models.campaign import Campaign


# ─── CREATE ──────────────────────────────────────────────────────────────

def create_fund(fund_name, description="", department_id=1, fund_type="General"):
    """Create a new fund"""
    db = get_db()
    existing = db.fetchone(
        "SELECT id FROM funds WHERE fund_name = ? AND department_id = ?",
        (fund_name, department_id)
    )
    if existing:
        raise ValueError(f"Fund '{fund_name}' already exists")
    
    data = {
        "department_id": department_id,
        "fund_name": fund_name,
        "fund_description": description,
        "fund_type": fund_type,
        "is_active": 1
    }
    return db.insert("funds", data)


# ─── READ ────────────────────────────────────────────────────────────────

def get_all_funds(department_id=1):
    """Get all funds for a department"""
    db = get_db()
    return db.fetchall(
        "SELECT * FROM funds WHERE department_id = ? ORDER BY id ASC",
        (department_id,)
    )


def get_active_funds(department_id=1):
    """Get all active funds"""
    db = get_db()
    return db.fetchall(
        "SELECT * FROM funds WHERE department_id = ? AND is_active = 1 ORDER BY fund_name",
        (department_id,)
    )


def get_fund_by_id(fund_id):
    """Get fund by ID"""
    return Fund.find(fund_id)


def get_fund_dropdown_list(department_id=1):
    """Get funds as dropdown options (id, name)"""
    db = get_db()
    funds = db.fetchall(
        "SELECT id, fund_name FROM funds WHERE department_id = ? AND is_active = 1 ORDER BY fund_name",
        (department_id,)
    )
    return [{"id": f["id"], "name": f["fund_name"]} for f in funds]


# ─── UPDATE ──────────────────────────────────────────────────────────────

def update_fund(fund_id, data):
    """Update a fund"""
    fund = Fund.find(fund_id)
    if not fund:
        raise ValueError("Fund not found")
    
    if "fund_name" in data:
        fund.fund_name = data["fund_name"]
    if "fund_description" in data:
        fund.fund_description = data["fund_description"]
    if "fund_type" in data:
        fund.fund_type = data["fund_type"]
    
    fund.save()
    return True


def toggle_fund_status(fund_id):
    """Activate/deactivate a fund"""
    db = get_db()
    fund = db.fetchone("SELECT is_active FROM funds WHERE id = ?", (fund_id,))
    if not fund:
        raise ValueError("Fund not found")
    new_status = 0 if fund["is_active"] else 1
    db.execute("UPDATE funds SET is_active = ? WHERE id = ?", (new_status, fund_id))
    return new_status


# ─── DELETE ──────────────────────────────────────────────────────────────

def delete_fund(fund_id):
    """Delete a fund (only if no campaigns linked)"""
    db = get_db()
    campaigns = db.fetchone("SELECT id FROM campaigns WHERE fund_id = ? LIMIT 1", (fund_id,))
    if campaigns:
        raise ValueError("Cannot delete fund with linked campaigns")
    db.delete("funds", "id = ?", (fund_id,))
    return True


# ─── SUMMARY ─────────────────────────────────────────────────────────────

def get_fund_summary(fund_id):
    """Get summary of a fund including collections and expenses"""
    db = get_db()
    
    # Get all campaigns for this fund
    campaigns = db.fetchall(
        """SELECT c.*, 
                  (SELECT COALESCE(SUM(amount), 0) FROM payments WHERE campaign_id = c.id) as collected
           FROM campaigns c
           WHERE c.fund_id = ?""",
        (fund_id,)
    )
    
    # Get total expenses for this fund
    total_expenses = db.fetchone(
        "SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE fund_id = ?",
        (fund_id,)
    )
    
    total_collected = sum(c["collected"] for c in campaigns) if campaigns else 0
    
    return {
        "total_collected": total_collected,
        "total_expenses": total_expenses["total"] if total_expenses else 0,
        "balance": total_collected - (total_expenses["total"] if total_expenses else 0),
        "campaigns": campaigns
    }


def get_fund_collection_total(fund_id):
    """Get total collection for a fund"""
    db = get_db()
    result = db.fetchone(
        """SELECT COALESCE(SUM(p.amount), 0) as total 
           FROM payments p
           JOIN campaigns c ON p.campaign_id = c.id
           WHERE c.fund_id = ?""",
        (fund_id,)
    )
    return result["total"] if result else 0


def get_fund_expense_total(fund_id):
    """Get total expenses for a fund"""
    db = get_db()
    result = db.fetchone(
        "SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE fund_id = ?",
        (fund_id,)
    )
    return result["total"] if result else 0


def get_fund_balance(fund_id):
    """Get balance for a fund (collection - expenses)"""
    collection = get_fund_collection_total(fund_id)
    expenses = get_fund_expense_total(fund_id)
    return collection - expenses