"""
Input validation utilities
"""
import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number (10-15 digits)"""
    pattern = r'^\d{10,15}$'
    return re.match(pattern, str(phone)) is not None

def validate_bank_account(account):
    """Validate bank account number (10-18 digits)"""
    pattern = r'^\d{10,18}$'
    return re.match(pattern, str(account)) is not None

def validate_date(date_string):
    """Validate date string format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_salary(salary):
    """Validate salary is a positive number"""
    try:
        amount = float(salary)
        return amount >= 0
    except (ValueError, TypeError):
        return False

def validate_password(password):
    """Validate password strength (min 6 characters)"""
    return len(password) >= 6

def calculate_pt(basic_salary):
    """Calculate Professional Tax based on salary slabs"""
    from payroll_system.config import PT_SLABS
    
    basic = float(basic_salary)
    for (min_sal, max_sal), pt_amount in PT_SLABS.items():
        if min_sal <= basic <= max_sal:
            return pt_amount
    return 0

