# src/utils/validators.py
"""Input validation utilities"""
import re


def validate_email(email):
    """Validate email address (optional field)"""
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """Validate phone number (optional field)"""
    if not phone:
        return True
    pattern = r'^\+?[\d\s\-]{7,15}$'
    return bool(re.match(pattern, phone))


def validate_amount(amount):
    """Validate amount is a positive number"""
    try:
        val = float(amount)
        return val >= 0
    except (ValueError, TypeError):
        return False


def validate_roll_number(roll):
    """Validate roll number format: PROGRAM-SESSION-001"""
    if not roll:
        return False
    pattern = r'^[A-Z]+-\d{4}-\d{3,}$'
    return bool(re.match(pattern, roll))


def validate_required(value, field_name="Field"):
    """Validate that a field is not empty"""
    if not value or str(value).strip() == "":
        return False, f"{field_name} is required"
    return True, ""


def validate_semester(semester):
    """Validate semester is between 1 and 8"""
    try:
        sem = int(semester)
        return 1 <= sem <= 8
    except (ValueError, TypeError):
        return False


def validate_program_code(code):
    """Validate program code is uppercase letters only"""
    if not code:
        return False
    return bool(re.match(r'^[A-Z]{2,5}$', code.strip().upper()))


def validate_student_name(name):
    """Validate student name (minimum 2 characters)"""
    if not name:
        return False
    clean = name.strip()
    return len(clean) >= 2 and len(clean) <= 100


def validate_campaign_name(name):
    """Validate campaign name (minimum 3 characters)"""
    if not name:
        return False
    clean = name.strip()
    return len(clean) >= 3 and len(clean) <= 100


def validate_fund_name(name):
    """Validate fund name (minimum 3 characters)"""
    if not name:
        return False
    clean = name.strip()
    return len(clean) >= 3 and len(clean) <= 50


def validate_receipt_prefix(prefix):
    """Validate receipt prefix is 2-5 uppercase letters"""
    if not prefix:
        return False
    return bool(re.match(r'^[A-Z]{2,5}$', prefix.strip().upper()))


def validate_session_name(session):
    """Validate session name (e.g., 2022, 2023)"""
    if not session:
        return False
    return bool(re.match(r'^\d{4}$', session.strip()))


def validate_section_name(section):
    """Validate section name (single letter or number)"""
    if not section:
        return False
    return bool(re.match(r'^[A-Z0-9]{1,2}$', section.strip().upper()))


def validate_shift_name(shift):
    """Validate shift name (minimum 3 characters)"""
    if not shift:
        return False
    return len(shift.strip()) >= 3


def get_validation_errors(data, rules):
    """
    Validate data against rules.
    Rules format: {'field_name': [validator_function, ...]}
    Returns dict of field: error_message
    """
    errors = {}
    for field, validators in rules.items():
        value = data.get(field)
        for validator in validators:
            if callable(validator):
                result = validator(value)
                if isinstance(result, tuple):
                    is_valid, message = result
                    if not is_valid:
                        errors[field] = message
                        break
                elif not result:
                    errors[field] = f"{field} is invalid"
                    break
    return errors


def is_valid(data, rules):
    """Check if data passes all validation rules"""
    errors = get_validation_errors(data, rules)
    return len(errors) == 0, errors


# ─── Common validation rule sets ───────────────────────────

STUDENT_RULES = {
    'student_name': [validate_required, validate_student_name],
    'program_id': [validate_required],
    'session_id': [validate_required],
    'semester': [validate_required, validate_semester],
    'email': [validate_email],
    'phone': [validate_phone]
}

CAMPAIGN_RULES = {
    'campaign_name': [validate_required, validate_campaign_name],
    'fund_id': [validate_required],
    'required_amount': [validate_required, validate_amount]
}

FUND_RULES = {
    'fund_name': [validate_required, validate_fund_name]
}

DEPARTMENT_RULES = {
    'department_name': [validate_required],
    'university_name': [validate_required],
    'receipt_prefix': [validate_required, validate_receipt_prefix],
    'email': [validate_email],
    'phone': [validate_phone]
}