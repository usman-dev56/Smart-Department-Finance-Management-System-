# src/services/pdf_service.py
"""PDF Service - Receipt and Report Generation"""
import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from src.utils.helpers import get_receipt_dir, get_export_dir, format_currency, format_date
from src.utils.logger import get_logger

logger = get_logger(__name__)
styles = getSampleStyleSheet()


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def _get_receipt_style():
    return {
        "title": ParagraphStyle("title", parent=styles["Normal"],
                                fontSize=16, fontName="Helvetica-Bold",
                                alignment=TA_CENTER, textColor=colors.HexColor("#1a73e8")),
        "subtitle": ParagraphStyle("subtitle", parent=styles["Normal"],
                                   fontSize=11, fontName="Helvetica",
                                   alignment=TA_CENTER, textColor=colors.grey),
        "label": ParagraphStyle("label", parent=styles["Normal"],
                                fontSize=9, fontName="Helvetica-Bold",
                                textColor=colors.HexColor("#555555")),
        "value": ParagraphStyle("value", parent=styles["Normal"],
                                fontSize=10, fontName="Helvetica",
                                textColor=colors.black),
        "amount": ParagraphStyle("amount", parent=styles["Normal"],
                                 fontSize=14, fontName="Helvetica-Bold",
                                 alignment=TA_CENTER, textColor=colors.HexColor("#0f9d58")),
        "footer": ParagraphStyle("footer", parent=styles["Normal"],
                                 fontSize=8, fontName="Helvetica",
                                 alignment=TA_CENTER, textColor=colors.grey),
        "heading": ParagraphStyle("heading", parent=styles["Normal"],
                                  fontSize=12, fontName="Helvetica-Bold",
                                  alignment=TA_CENTER, textColor=colors.HexColor("#1a73e8")),
    }


def _get_dept_value(dept, key, default=""):
    """Safely get department value from dict or object"""
    if not dept:
        return default
    if isinstance(dept, dict):
        return dept.get(key, default)
    return getattr(dept, key, default)


def generate_receipt_pdf(payment, dept, qr_path=None):
    """Generate a payment receipt PDF - Small Size with Semester, Section, Shift on new line"""
    try:
        receipt_dir = get_receipt_dir()
        filename = f"{payment.get('receipt_number', 'receipt')}.pdf"
        filepath = os.path.join(receipt_dir, filename)
        
        # ─── SMALL RECEIPT SIZE ──────────────────────────────────────────
        doc = SimpleDocTemplate(
            filepath, 
            pagesize=(500, 350),
            rightMargin=0.5*cm,
            leftMargin=0.5*cm,
            topMargin=0.5*cm,
            bottomMargin=0.5*cm
        )
        
        st = _get_receipt_style()
        story = []

        # Get department values
        uni_name = _get_dept_value(dept, 'university_name', 'University')
        dept_name = _get_dept_value(dept, 'department_name', 'Department')
        logo_path = _get_dept_value(dept, 'logo_path', None)

        # ─── Logo with EXE support ──────────────────────────────────────
        if logo_path:
            if getattr(sys, 'frozen', False):
                logo_path = get_resource_path(logo_path)
            
            if os.path.exists(logo_path):
                try:
                    logo = Image(logo_path, width=1.5*cm, height=1.5*cm)
                    story.append(logo)
                    story.append(Spacer(1, 0.15*cm))
                except Exception as e:
                    logger.warning(f"Could not load logo: {e}")
            else:
                logger.warning(f"Logo file not found: {logo_path}")

        # ─── HEADER ──────────────────────────────────────────────────────
        story.append(Paragraph(uni_name.upper(), ParagraphStyle(
            'uni_name',
            parent=styles['Normal'],
            fontSize=13,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=0,
            textColor=colors.HexColor('#0d1117')
        )))
        story.append(Spacer(1, 0.10*cm))

        story.append(Paragraph(f"Dept. of {dept_name}", ParagraphStyle(
            'dept_name',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            alignment=TA_CENTER,
            spaceAfter=6,
            textColor=colors.HexColor('#333333')
        )))

        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1a73e8")))
        story.append(Spacer(1, 0.15*cm))

        story.append(Paragraph("PAYMENT RECEIPT", ParagraphStyle(
            'receipt_title',
            parent=styles['Normal'],
            fontSize=12,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=6,
            textColor=colors.HexColor("#1a73e8")
        )))
        story.append(Spacer(1, 0.15*cm))

        # ─── RECEIPT INFO ──────────────────────────────────────────────────
        semester = payment.get("semester", "")
        section = payment.get("section", "")
        shift = payment.get("shift", "")

        student_details = ""
        if semester:
            student_details = f"Semester: {semester}"
            if section:
                student_details += f", Section: {section}"
            if shift:
                student_details += f", {shift}"

        data_rows = [
            ["Receipt No:", payment.get("receipt_number", ""), "Date:", format_date(payment.get("payment_date", ""))],
            ["Student:", payment.get("student_name", ""), "Roll No:", payment.get("roll_number", "")],
            ["Details:", student_details, "", ""],
            ["Campaign:", payment.get("campaign_name", ""), "Method:", payment.get("payment_method", "Cash")],
            ["Received By:", payment.get("received_by", ""), "", ""],
        ]
        
        tbl = Table(data_rows, colWidths=[2.5*cm, 4.5*cm, 2.2*cm, 3.5*cm])
        tbl.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.HexColor("#f8f9fa"), colors.white]),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 0.2*cm))

        # ─── AMOUNT ──────────────────────────────────────────────────────
        story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
        story.append(Spacer(1, 0.15*cm))
        story.append(Paragraph(f"Amount Paid: {format_currency(payment.get('amount', 0))}", 
                               ParagraphStyle('amount_small', parent=st["amount"], fontSize=12)))
        story.append(Spacer(1, 0.15*cm))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))

        # ─── QR CODE ──────────────────────────────────────────────────────
        if qr_path and os.path.exists(qr_path):
            story.append(Spacer(1, 0.2*cm))
            qr_img = Image(qr_path, width=2.2*cm, height=2.2*cm)
            story.append(qr_img)

        # ─── FOOTER ──────────────────────────────────────────────────────
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph("Computer-generated receipt", st["footer"]))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%d-%b-%Y %I:%M %p')}", st["footer"]))

        doc.build(story)
        logger.info(f"Receipt generated: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Receipt PDF error: {e}")
        return None


def generate_collection_report_pdf(campaigns_data, dept):
    """Generate collection report PDF with proper header and spacers"""
    try:
        filepath = os.path.join(get_export_dir(), f"collection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm,
                                topMargin=1.5*cm, bottomMargin=1.5*cm)
        story = []
        st = _get_receipt_style()
        
        uni_name = _get_dept_value(dept, 'university_name', 'University')
        dept_name = _get_dept_value(dept, 'department_name', 'Department')
        
        # ─── HEADER ──────────────────────────────────────────────────────
        # University Name
        story.append(Paragraph(uni_name.upper(), ParagraphStyle(
            'report_uni',
            parent=styles['Normal'],
            fontSize=18,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=0,
            textColor=colors.HexColor('#1a237e')
        )))
        story.append(Spacer(1, 0.20*cm))  # ← Spacer between university and department
        
        # Department Name
        story.append(Paragraph(f"Department of {dept_name}", ParagraphStyle(
            'report_dept',
            parent=styles['Normal'],
            fontSize=13,
            fontName='Helvetica',
            alignment=TA_CENTER,
            spaceAfter=0,
            textColor=colors.HexColor('#333333')
        )))
        story.append(Spacer(1, 0.5*cm))  # ← Spacer before separator
        
        # Separator Line
        story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#1a73e8")))
        story.append(Spacer(1, 0.3*cm))  # ← Spacer after separator
        
        # Report Title
        story.append(Paragraph("COLLECTION REPORT", ParagraphStyle(
            'report_title',
            parent=styles['Normal'],
            fontSize=16,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=0,
            textColor=colors.HexColor("#1a73e8")
        )))
        story.append(Spacer(1, 0.5*cm))  # ← Spacer before table

        # ─── TABLE ──────────────────────────────────────────────────────
        headers = ["Campaign", "Fund", "Eligible", "Paid", "Pending", "Collected"]
        rows = [headers]
        total_collected = 0
        total_eligible = 0
        
        for c in campaigns_data:
            amount = c.get("total_collected", 0)
            eligible = c.get("total_eligible", 0)
            rows.append([
                c.get("campaign_name", ""),
                c.get("fund_name", ""),
                str(eligible),
                str(c.get("total_paid", 0)),
                str(c.get("total_pending", 0)),
                format_currency(amount),
            ])
            total_collected += amount
            total_eligible += eligible

        rows.append(["", "", "TOTAL", "", "", format_currency(total_collected)])

        tbl = Table(rows, colWidths=[5*cm, 3.5*cm, 2.5*cm, 2*cm, 2.5*cm, 3*cm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a73e8")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#f0f4ff")]),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e8f0fe")),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("ALIGN", (2, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(tbl)
        
        # ─── FOOTER ──────────────────────────────────────────────────────
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%d-%b-%Y %I:%M %p')}", 
                               ParagraphStyle('report_footer', parent=styles['Normal'], 
                                             fontSize=8, alignment=TA_CENTER, textColor=colors.grey)))

        doc.build(story)
        return filepath
    except Exception as e:
        logger.error(f"Collection report error: {e}")
        return None


def generate_student_report_pdf(students_data, dept):
    """Generate student list report PDF with proper header and spacers"""
    try:
        filepath = os.path.join(get_export_dir(), f"student_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm,
                                topMargin=1.5*cm, bottomMargin=1.5*cm)
        story = []
        st = _get_receipt_style()
        
        uni_name = _get_dept_value(dept, 'university_name', 'University')
        dept_name = _get_dept_value(dept, 'department_name', 'Department')
        
        # ─── HEADER ──────────────────────────────────────────────────────
        # University Name
        story.append(Paragraph(uni_name.upper(), ParagraphStyle(
            'report_uni',
            parent=styles['Normal'],
            fontSize=18,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=0,
            textColor=colors.HexColor('#1a237e')
        )))
        story.append(Spacer(1, 0.20*cm))  # ← Spacer between university and department
        
        # Department Name
        story.append(Paragraph(f"Department of {dept_name}", ParagraphStyle(
            'report_dept',
            parent=styles['Normal'],
            fontSize=13,
            fontName='Helvetica',
            alignment=TA_CENTER,
            spaceAfter=0,
            textColor=colors.HexColor('#333333')
        )))
        story.append(Spacer(1, 0.3*cm))  # ← Spacer before separator
        
        # Separator Line
        story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#1a73e8")))
        story.append(Spacer(1, 0.3*cm))  # ← Spacer after separator
        
        # Report Title
        story.append(Paragraph("STUDENT REPORT", ParagraphStyle(
            'report_title',
            parent=styles['Normal'],
            fontSize=16,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=0,
            textColor=colors.HexColor("#1a73e8")
        )))
        story.append(Spacer(1, 0.5*cm))  # ← Spacer before table

        # ─── TABLE ──────────────────────────────────────────────────────
        headers = ["Roll No", "Name", "Program", "Semester", "Section"]
        rows = [headers]
        for s in students_data:
            rows.append([
                s.get("roll_number", ""),
                s.get("student_name", ""),
                s.get("program_name", ""),
                str(s.get("semester", "")),
                s.get("section_name", ""),
            ])

        tbl = Table(rows, colWidths=[3*cm, 4*cm, 3.5*cm, 2*cm, 2*cm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a73e8")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4ff")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(tbl)
        
        # ─── FOOTER ──────────────────────────────────────────────────────
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%d-%b-%Y %I:%M %p')}", 
                               ParagraphStyle('report_footer', parent=styles['Normal'], 
                                             fontSize=8, alignment=TA_CENTER, textColor=colors.grey)))

        doc.build(story)
        return filepath
    except Exception as e:
        logger.error(f"Student report error: {e}")
        return None


def generate_expense_report_pdf(expenses_data, dept):
    """Generate expense report PDF with proper header and spacers"""
    try:
        filepath = os.path.join(get_export_dir(), f"expense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm,
                                topMargin=1.5*cm, bottomMargin=1.5*cm)
        story = []
        st = _get_receipt_style()
        
        uni_name = _get_dept_value(dept, 'university_name', 'University')
        dept_name = _get_dept_value(dept, 'department_name', 'Department')
        
        # ─── HEADER ──────────────────────────────────────────────────────
        # University Name
        story.append(Paragraph(uni_name.upper(), ParagraphStyle(
            'report_uni',
            parent=styles['Normal'],
            fontSize=18,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=0,
            textColor=colors.HexColor('#1a237e')
        )))
        story.append(Spacer(1, 0.20*cm))  # ← Spacer between university and department
        
        # Department Name
        story.append(Paragraph(f"Department of {dept_name}", ParagraphStyle(
            'report_dept',
            parent=styles['Normal'],
            fontSize=13,
            fontName='Helvetica',
            alignment=TA_CENTER,
            spaceAfter=0,
            textColor=colors.HexColor('#333333')
        )))
        story.append(Spacer(1, 0.5*cm))  # ← Spacer before separator
        
        # Separator Line
        story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#1a73e8")))
        story.append(Spacer(1, 0.3*cm))  # ← Spacer after separator
        
        # Report Title
        story.append(Paragraph("EXPENSE REPORT", ParagraphStyle(
            'report_title',
            parent=styles['Normal'],
            fontSize=16,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=0,
            textColor=colors.HexColor("#1a73e8")
        )))
        story.append(Spacer(1, 0.5*cm))  # ← Spacer before table

        # ─── TABLE ──────────────────────────────────────────────────────
        headers = ["Title", "Fund", "Amount", "Date", "Created By"]
        rows = [headers]
        total = 0
        for e in expenses_data:
            amount = e.get("amount", 0)
            rows.append([
                e.get("expense_title", ""),
                e.get("fund_name", ""),
                format_currency(amount),
                format_date(e.get("expense_date", "")),
                e.get("created_by", ""),
            ])
            total += amount

        rows.append(["", "", format_currency(total), "", ""])

        tbl = Table(rows, colWidths=[4*cm, 3.5*cm, 2.5*cm, 2.5*cm, 3*cm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a73e8")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#f0f4ff")]),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e8f0fe")),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("ALIGN", (2, 0), (2, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(tbl)
        
        # ─── FOOTER ──────────────────────────────────────────────────────
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%d-%b-%Y %I:%M %p')}", 
                               ParagraphStyle('report_footer', parent=styles['Normal'], 
                                             fontSize=8, alignment=TA_CENTER, textColor=colors.grey)))

        doc.build(story)
        return filepath
    except Exception as e:
        logger.error(f"Expense report error: {e}")
        return None