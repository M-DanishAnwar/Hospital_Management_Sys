"""
Helper functions for the Hospital Management System
"""

import datetime
import re
from tkinter import messagebox

def format_date(date_str):
    """Format date string to YYYY-MM-DD format"""
    if not date_str:
        return None
    try:
        # Try to parse different date formats
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        try:
            date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            return None

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    pattern = r'^[0-9+\s\-()]{10,15}$'
    return re.match(pattern, phone) is not None

def show_success(message):
    """Show success message dialog"""
    messagebox.showinfo("Success", message)

def show_error(message):
    """Show error message dialog"""
    messagebox.showerror("Error", message)

def show_warning(message):
    """Show warning message dialog"""
    messagebox.showwarning("Warning", message)

def validate_required_fields(fields):
    """
    Validate that required fields are not empty
    fields: dict of {field_name: field_value}
    """
    for name, value in fields.items():
        if not value or str(value).strip() == '':
            show_error(f"{name} is required")
            return False
    return True

def format_currency(amount):
    """Format amount as currency"""
    try:
        return f"${float(amount):,.2f}"
    except (ValueError, TypeError):
        return "$0.00"

def get_current_date():
    """Get current date in YYYY-MM-DD format"""
    return datetime.datetime.now().strftime('%Y-%m-%d')