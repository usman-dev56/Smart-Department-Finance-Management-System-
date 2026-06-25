# src/services/excel_service.py
"""Excel Export Service"""
import os
import pandas as pd
from src.utils.helpers import get_export_dir, format_currency
from src.utils.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)


def export_students(students):
    """Export student list to Excel"""
    try:
        filepath = os.path.join(get_export_dir(), f"students_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        if not students:
            logger.warning("No students data to export")
            return None
            
        data = []
        for s in students:
            data.append({
                "Roll Number": s.get("roll_number", ""),
                "Name": s.get("student_name", ""),
                "Program": s.get("program_name", ""),
                "Session": s.get("session_name", ""),
                "Semester": s.get("semester", ""),
                "Section": s.get("section_name", ""),
                "Shift": s.get("shift_name", ""),
                "Phone": s.get("phone", ""),
                "Email": s.get("email", ""),
            })
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        logger.info(f"Students exported: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Student export error: {e}")
        return None


def export_students_full(students):
    """Export student list with all fields to Excel"""
    try:
        filepath = os.path.join(get_export_dir(), f"students_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        if not students:
            return None
            
        df = pd.DataFrame(students)
        df.to_excel(filepath, index=False)
        logger.info(f"Full students exported: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Full student export error: {e}")
        return None


def export_payments(payments):
    """Export payment history to Excel"""
    try:
        filepath = os.path.join(get_export_dir(), f"payments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        if not payments:
            logger.warning("No payments data to export")
            return None
            
        data = []
        for p in payments:
            data.append({
                "Receipt No": p.get("receipt_number", ""),
                "Date": p.get("payment_date", ""),
                "Student": p.get("student_name", ""),
                "Roll No": p.get("roll_number", ""),
                "Campaign": p.get("campaign_name", ""),
                "Fund": p.get("fund_name", ""),
                "Amount": p.get("amount", 0),
                "Method": p.get("payment_method", ""),
                "Received By": p.get("received_by", ""),
            })
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        logger.info(f"Payments exported: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Payments export error: {e}")
        return None


def export_campaign_summary(campaigns_data):
    """Export campaign summary to Excel"""
    try:
        filepath = os.path.join(get_export_dir(), f"campaigns_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        if not campaigns_data:
            logger.warning("No campaign data to export")
            return None
            
        data = []
        for c in campaigns_data:
            data.append({
                "Campaign": c.get("campaign_name", ""),
                "Fund": c.get("fund_name", ""),
                "Eligible Students": c.get("total_eligible", 0),
                "Paid": c.get("total_paid", 0),
                "Pending": c.get("total_pending", 0),
                "Total Collected": c.get("total_collected", 0),
                "Collection %": f"{c.get('collection_percent', 0):.1f}%",
            })
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        logger.info(f"Campaign summary exported: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Campaign summary export error: {e}")
        return None


def export_expenses(expenses):
    """Export expense list to Excel"""
    try:
        filepath = os.path.join(get_export_dir(), f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        if not expenses:
            logger.warning("No expenses data to export")
            return None
            
        data = []
        for e in expenses:
            data.append({
                "Title": e.get("expense_title", ""),
                "Fund": e.get("fund_name", ""),
                "Amount": e.get("amount", 0),
                "Date": e.get("expense_date", ""),
                "Created By": e.get("created_by", ""),
            })
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        logger.info(f"Expenses exported: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Expenses export error: {e}")
        return None


def export_report(data, filename_prefix="report"):
    """Generic export function for any data"""
    try:
        filepath = os.path.join(get_export_dir(), f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        if not data:
            return None
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        return filepath
    except Exception as e:
        logger.error(f"Report export error: {e}")
        return None