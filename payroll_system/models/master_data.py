"""
Master data models (Department, Designation, Branch, Shift, Holiday)
"""
from datetime import datetime, date

class Department:
    """Department model"""
    
    def __init__(self, department_id: str, department_name: str, **kwargs):
        self.department_id = department_id
        self.department_name = department_name
        self.created_date = kwargs.get('created_date', datetime.now().date())
        self.modified_date = kwargs.get('modified_date', datetime.now().date())
        self.status = kwargs.get('status', 1)
    
    def to_dict(self):
        return {
            'department_id': self.department_id,
            'department_name': self.department_name,
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, date) else str(self.created_date),
            'modified_date': self.modified_date.isoformat() if isinstance(self.modified_date, date) else str(self.modified_date),
            'status': self.status
        }

class Designation:
    """Designation model"""
    
    def __init__(self, designation_id: str, designation_name: str, 
                 department_id: str, **kwargs):
        self.designation_id = designation_id
        self.designation_name = designation_name
        self.department_id = department_id
        self.created_date = kwargs.get('created_date', datetime.now().date())
        self.modified_date = kwargs.get('modified_date', datetime.now().date())
        self.status = kwargs.get('status', 1)
    
    def to_dict(self):
        return {
            'designation_id': self.designation_id,
            'designation_name': self.designation_name,
            'department_id': self.department_id,
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, date) else str(self.created_date),
            'modified_date': self.modified_date.isoformat() if isinstance(self.modified_date, date) else str(self.modified_date),
            'status': self.status
        }

class Branch:
    """Branch model"""
    
    def __init__(self, branch_id: str, name: str, branch_address: str,
                 phone_number: str, email: str, **kwargs):
        self.branch_id = branch_id
        self.name = name
        self.branch_address = branch_address
        self.phone_number = phone_number
        self.email = email
        self.establishment_date = kwargs.get('establishment_date', datetime.now().date())
        self.created_by = kwargs.get('created_by', '')
        self.created_date = kwargs.get('created_date', datetime.now().date())
        self.modified_date = kwargs.get('modified_date', datetime.now().date())
        self.status = kwargs.get('status', 1)
    
    def to_dict(self):
        return {
            'branch_id': self.branch_id,
            'name': self.name,
            'branch_address': self.branch_address,
            'phone_number': self.phone_number,
            'email': self.email,
            'establishment_date': self.establishment_date.isoformat() if isinstance(self.establishment_date, date) else str(self.establishment_date),
            'created_by': self.created_by,
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, date) else str(self.created_date),
            'modified_date': self.modified_date.isoformat() if isinstance(self.modified_date, date) else str(self.modified_date),
            'status': self.status
        }

class Shift:
    """Shift model"""
    
    def __init__(self, shift_id: str, shift_name: str, in_time: str,
                 out_time: str, **kwargs):
        self.shift_id = shift_id
        self.shift_name = shift_name
        self.in_time = in_time  # Format: "HH:MM:SS"
        self.out_time = out_time
        self.created_date = kwargs.get('created_date', datetime.now().date())
        self.modified_date = kwargs.get('modified_date', datetime.now().date())
        self.status = kwargs.get('status', 1)
    
    def to_dict(self):
        return {
            'shift_id': self.shift_id,
            'shift_name': self.shift_name,
            'in_time': self.in_time,
            'out_time': self.out_time,
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, date) else str(self.created_date),
            'modified_date': self.modified_date.isoformat() if isinstance(self.modified_date, date) else str(self.modified_date),
            'status': self.status
        }

class Holiday:
    """Holiday model"""
    
    def __init__(self, holiday_id: str, holiday_name: str, 
                 holiday_date: date, **kwargs):
        self.holiday_id = holiday_id
        self.holiday_name = holiday_name
        self.holiday_description = kwargs.get('holiday_description', '')
        self.holiday_date = holiday_date
        self.created_date = kwargs.get('created_date', datetime.now().date())
        self.modified_date = kwargs.get('modified_date', datetime.now().date())
        self.status = kwargs.get('status', 1)
    
    def to_dict(self):
        return {
            'holiday_id': self.holiday_id,
            'holiday_name': self.holiday_name,
            'holiday_description': self.holiday_description,
            'holiday_date': self.holiday_date.isoformat() if isinstance(self.holiday_date, date) else str(self.holiday_date),
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, date) else str(self.created_date),
            'modified_date': self.modified_date.isoformat() if isinstance(self.modified_date, date) else str(self.modified_date),
            'status': self.status
        }

