"""
Employee service for business logic
"""
from typing import List, Optional, Tuple
from payroll_system.models.employee import Employee
from payroll_system.repository.employee_repository import EmployeeRepository
from payroll_system.utils.validators import validate_email, validate_phone, validate_bank_account, calculate_pt
from payroll_system.config import ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE
import logging

logger = logging.getLogger(__name__)

class EmployeeService:
    """Service for employee business logic"""
    
    def __init__(self):
        self.repository = EmployeeRepository()
    
    def create_employee(self, employee_data: dict) -> Tuple[bool, str]:
        """Create a new employee with validation"""
        try:
            # Validate email
            if not validate_email(employee_data.get('email', '')):
                return False, "Invalid email format"
            
            # Check if email already exists
            existing = self.repository.get_by_email(employee_data['email'])
            if existing:
                return False, "Email already exists"
            
            # Validate phone
            if employee_data.get('mobile_number') and not validate_phone(employee_data['mobile_number']):
                return False, "Invalid phone number"
            
            # Validate bank account
            if employee_data.get('bank_account_number') and not validate_bank_account(employee_data['bank_account_number']):
                return False, "Invalid bank account number"
            
            # Calculate PT based on basic salary
            basic_salary = float(employee_data.get('basic_salary', 0))
            pt = calculate_pt(basic_salary)
            employee_data['pt'] = pt
            
            # Create employee
            employee = Employee(**employee_data)
            success = self.repository.create(employee)
            
            if success:
                return True, "Employee created successfully"
            else:
                return False, "Failed to create employee"
        except Exception as e:
            logger.error(f"Error creating employee: {e}")
            return False, f"Error: {str(e)}"
    
    def get_employee(self, employee_id: str) -> Optional[Employee]:
        """Get employee by ID"""
        return self.repository.get_by_id(employee_id)
    
    def get_all_employees(self, status: Optional[int] = 1) -> List[Employee]:
        """Get all active employees"""
        return self.repository.get_all(status)
    
    def update_employee(self, employee_id: str, employee_data: dict) -> Tuple[bool, str]:
        """Update employee"""
        try:
            employee = self.repository.get_by_id(employee_id)
            if not employee:
                return False, "Employee not found"
            
            # Update fields
            for key, value in employee_data.items():
                if hasattr(employee, key):
                    setattr(employee, key, value)
            
            # Recalculate PT if basic salary changed
            if 'basic_salary' in employee_data:
                employee.pt = calculate_pt(employee.basic_salary)
            
            success = self.repository.update(employee)
            if success:
                return True, "Employee updated successfully"
            else:
                return False, "Failed to update employee"
        except Exception as e:
            logger.error(f"Error updating employee: {e}")
            return False, f"Error: {str(e)}"
    
    def delete_employee(self, employee_id: str) -> Tuple[bool, str]:
        """Delete employee (soft delete)"""
        try:
            success = self.repository.delete(employee_id)
            if success:
                return True, "Employee deleted successfully"
            else:
                return False, "Failed to delete employee"
        except Exception as e:
            logger.error(f"Error deleting employee: {e}")
            return False, f"Error: {str(e)}"
    
    def search_employees(self, search_term: str) -> List[Employee]:
        """Search employees"""
        return self.repository.search(search_term)
    
    def get_by_email(self, email: str) -> Optional[Employee]:
        """Get employee by email"""
        return self.repository.get_by_email(email)
    
    def authenticate(self, email: str, password: str) -> Tuple[Optional[Employee], str]:
        """Authenticate employee login"""
        try:
            employee = self.repository.get_by_email(email)
            if not employee:
                return None, "Invalid email or password"
            
            if employee.password != password:
                return None, "Invalid email or password"
            
            if employee.status != 1:
                return None, "Employee account is inactive"
            
            return employee, "Login successful"
        except Exception as e:
            logger.error(f"Error authenticating: {e}")
            return None, f"Error: {str(e)}"

    def ensure_default_admin(self, *, email: str, password: str, employee_id: str = "ADMIN001") -> Tuple[bool, str]:
        """
        Ensure a default admin user exists.

        If an admin with this email doesn't exist, it is created.
        If it exists and RESET_DEFAULT_ADMIN is enabled, the password is reset.
        """
        try:
            from payroll_system.config import ROLE_ADMIN, RESET_DEFAULT_ADMIN

            existing = self.repository.get_by_email(email)
            if not existing:
                admin_data = {
                    "employee_id": employee_id,
                    "employee_name": "System Administrator",
                    "email": email,
                    "password": password,
                    "role": ROLE_ADMIN,
                    "basic_salary": 0,
                    "status": 1,
                }
                ok, msg = self.create_employee(admin_data)
                return ok, f"Default admin created: {msg}"

            if RESET_DEFAULT_ADMIN and existing.password != password:
                existing.password = password
                updated = self.repository.update(existing)
                if updated:
                    return True, "Default admin password reset"
                return False, "Failed to reset default admin password"

            return True, "Default admin already exists"
        except Exception as e:
            logger.error(f"Error ensuring default admin: {e}")
            return False, f"Error: {str(e)}"

