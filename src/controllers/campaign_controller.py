# src/controllers/campaign_controller.py
"""Campaign Controller"""
from src.database.db_manager import get_db
from src.models.campaign import Campaign


def create_campaign(data):
    """Create a new campaign"""
    db = get_db()
    campaign_data = {
        "department_id": data.get("department_id", 1),
        "campaign_name": data["campaign_name"].strip(),
        "fund_id": data["fund_id"],
        "program_id": data.get("program_id"),
        "session_id": data.get("session_id"),
        "semester": data.get("semester"),
        "shift_id": data.get("shift_id"),
        "required_amount": float(data["required_amount"]),
        "is_active": 1,
    }
    return db.insert("campaigns", campaign_data)


def get_eligible_students(campaign_id):
    """Students who match the campaign criteria"""
    db = get_db()
    camp = db.fetchone("SELECT * FROM campaigns WHERE id=?", (campaign_id,))
    if not camp:
        return []
    
    query = """SELECT s.*, p.program_name, ss.session_name 
               FROM students s 
               LEFT JOIN programs p ON s.program_id = p.id 
               LEFT JOIN sessions ss ON s.session_id = ss.id 
               WHERE s.is_active=1"""
    params = []
    
    if camp["program_id"]:
        query += " AND s.program_id=?"
        params.append(camp["program_id"])
    if camp["session_id"]:
        query += " AND s.session_id=?"
        params.append(camp["session_id"])
    if camp["semester"]:
        query += " AND s.semester=?"
        params.append(camp["semester"])
    if camp["shift_id"]:
        query += " AND s.shift_id=?"
        params.append(camp["shift_id"])
    
    return db.fetchall(query, params)


def get_paid_students(campaign_id):
    """Get students who have paid for this campaign"""
    db = get_db()
    return db.fetchall(
        """SELECT s.*, p.payment_date, p.amount, p.receipt_number
           FROM payments p
           JOIN students s ON p.student_id = s.id
           WHERE p.campaign_id = ?
           ORDER BY s.student_name""",
        (campaign_id,)
    )


def get_pending_students(campaign_id):
    """Get eligible students who haven't paid yet"""
    eligible = get_eligible_students(campaign_id)
    paid = get_paid_students(campaign_id)
    paid_ids = {p["id"] for p in paid}
    return [s for s in eligible if s["id"] not in paid_ids]


def get_campaign_summary(campaign_id):
    """Get complete summary of a campaign"""
    db = get_db()
    camp = Campaign.get_with_details(campaign_id)
    if not camp:
        return None
    
    eligible = get_eligible_students(campaign_id)
    paid = get_paid_students(campaign_id)
    total_collected = sum(p["amount"] for p in paid) if paid else 0
    
    return {
        "campaign": camp,
        "total_eligible": len(eligible),
        "total_paid": len(paid),
        "total_pending": len(eligible) - len(paid),
        "total_collected": total_collected,
        "collection_percent": (len(paid) / len(eligible) * 100) if eligible else 0,
    }


def get_all_campaigns(department_id=1):
    """Get all campaigns with fund names"""
    db = get_db()
    return db.fetchall(
        """SELECT c.*, f.fund_name 
           FROM campaigns c
           LEFT JOIN funds f ON c.fund_id = f.id
           WHERE c.department_id = ?
           ORDER BY c.created_at ASC""",
        (department_id,)
    )


def get_campaign_by_id(campaign_id):
    """Get a single campaign by ID"""
    db = get_db()
    return db.fetchone(
        """SELECT c.*, f.fund_name, p.program_name, s.session_name, sh.shift_name
           FROM campaigns c
           LEFT JOIN funds f ON c.fund_id = f.id
           LEFT JOIN programs p ON c.program_id = p.id
           LEFT JOIN sessions s ON c.session_id = s.id
           LEFT JOIN shifts sh ON c.shift_id = sh.id
           WHERE c.id = ?""",
        (campaign_id,)
    )


def deactivate_campaign(campaign_id):
    """Deactivate a campaign"""
    db = get_db()
    db.execute("UPDATE campaigns SET is_active = 0 WHERE id = ?", (campaign_id,))
    return True


def activate_campaign(campaign_id):
    """Activate a campaign"""
    db = get_db()
    db.execute("UPDATE campaigns SET is_active = 1 WHERE id = ?", (campaign_id,))
    return True


def delete_campaign(campaign_id):
    """Delete a campaign (only if no payments exist)"""
    db = get_db()
    # Check if payments exist
    payments = db.fetchone("SELECT id FROM payments WHERE campaign_id = ? LIMIT 1", (campaign_id,))
    if payments:
        raise ValueError("Cannot delete campaign with existing payments")
    db.delete("campaigns", "id = ?", (campaign_id,))
    return True