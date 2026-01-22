"""
Employee data model
"""
from datetime import datetime, date
from payroll_system.config import ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE

class Employee:
    """Employee model"""
    
    def __init__(self, employee_id: str, employee_name: str, email: str, 
                 password: str, role: int = ROLE_EMPLOYEE, **kwargs):
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.email = email
        self.password = password
        self.role = role
        
        # Personal Information
        self.current_address = kwargs.get('current_address', '')
        self.permanent_address = kwargs.get('permanent_address', '')
        self.mobile_number = kwargs.get('mobile_number', '')
        self.gender = kwargs.get('gender', 'Male')
        self.dob = kwargs.get('dob', None)
        self.qualification = kwargs.get('qualification', '')
        self.city = kwargs.get('city', '')
        
        # Employment Information
        self.joining_date = kwargs.get('joining_date', datetime.now().date())
        self.registration_date = kwargs.get('registration_date', datetime.now().date())
        self.department_id = kwargs.get('department_id', None)
        self.branch_id = kwargs.get('branch_id', None)
        self.designation_id = kwargs.get('designation_id', None)
        self.shift_id = kwargs.get('shift_id', None)
        
        # Financial Information
        self.basic_salary = float(kwargs.get('basic_salary', 0))
        self.bank_account_number = kwargs.get('bank_account_number', '')
        self.pt = float(kwargs.get('pt', 0))
        
        # Metadata
        self.created_date = kwargs.get('created_date', datetime.now().date())
        self.modified_date = kwargs.get('modified_date', datetime.now().date())
        self.status = kwargs.get('status', 1)  # 1 = Active, 0 = Inactive
    
    def to_dict(self):
        """Convert employee to dictionary for MongoDB storage"""
        return {
            'employee_id': self.employee_id,
            'employee_name': self.employee_name,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'current_address': self.current_address,
            'permanent_address': self.permanent_address,
            'mobile_number': self.mobile_number,
            'gender': self.gender,
            'dob': self.dob.isoformat() if self.dob else None,
            'qualification': self.qualification,
            'city': self.city,
            'joining_date': self.joining_date.isoformat() if isinstance(self.joining_date, date) else str(self.joining_date),
            'registration_date': self.registration_date.isoformat() if isinstance(self.registration_date, date) else str(self.registration_date),
            'department_id': self.department_id,
            'branch_id': self.branch_id,
            'designation_id': self.designation_id,
            'shift_id': self.shift_id,
            'basic_salary': self.basic_salary,
            'bank_account_number': self.bank_account_number,
            'pt': self.pt,
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, date) else str(self.created_date),
            'modified_date': self.modified_date.isoformat() if isinstance(self.modified_date, date) else str(self.modified_date),
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create employee from dictionary"""
        from datetime import datetime as dt
        
        # Parse dates
        dob = None
        if data.get('dob'):
            if isinstance(data['dob'], str):
                dob = dt.strptime(data['dob'], '%Y-%m-%d').date()
            else:
                dob = data['dob']
        
        joining_date = None
        if data.get('joining_date'):
            if isinstance(data['joining_date'], str):
                joining_date = dt.strptime(data['joining_date'], '%Y-%m-%d').date()
            else:
                joining_date = data['joining_date']
        
        registration_date = None
        if data.get('registration_date'):
            if isinstance(data['registration_date'], str):
                registration_date = dt.strptime(data['registration_date'], '%Y-%m-%d').date()
            else:
                registration_date = data['registration_date']
        
        return cls(
            employee_id=data['employee_id'],
            employee_name=data['employee_name'],
            email=data['email'],
            password=data.get('password', ''),
            role=data.get('role', ROLE_EMPLOYEE),
            current_address=data.get('current_address', ''),
            permanent_address=data.get('permanent_address', ''),
            mobile_number=data.get('mobile_number', ''),
            gender=data.get('gender', 'Male'),
            dob=dob,
            qualification=data.get('qualification', ''),
            city=data.get('city', ''),
            joining_date=joining_date,
            registration_date=registration_date,
            department_id=data.get('department_id'),
            branch_id=data.get('branch_id'),
            designation_id=data.get('designation_id'),
            shift_id=data.get('shift_id'),
            basic_salary=data.get('basic_salary', 0),
            bank_account_number=data.get('bank_account_number', ''),
            pt=data.get('pt', 0),
            created_date=data.get('created_date', datetime.now().date()),
            modified_date=data.get('modified_date', datetime.now().date()),
            status=data.get('status', 1)
        )

