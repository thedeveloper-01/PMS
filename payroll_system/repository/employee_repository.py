"""
Employee repository for database operations
"""
from typing import List, Optional
from payroll_system.models.employee import Employee
from payroll_system.utils.database import db
import logging

logger = logging.getLogger(__name__)

class EmployeeRepository:
    """Repository for employee data operations"""
    
    def __init__(self):
        self.collection = db.get_db().employees
    
    def create(self, employee: Employee) -> bool:
        """Create a new employee"""
        try:
            employee_dict = employee.to_dict()
            result = self.collection.insert_one(employee_dict)
            logger.info(f"Created employee: {employee.employee_id}")
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"Error creating employee: {e}")
            return False
    
    def get_by_id(self, employee_id: str) -> Optional[Employee]:
        """Get employee by ID"""
        try:
            data = self.collection.find_one({'employee_id': employee_id})
            if data:
                return Employee.from_dict(data)
            return None
        except Exception as e:
            logger.error(f"Error getting employee by ID: {e}")
            return None
    
    def get_by_email(self, email: str) -> Optional[Employee]:
        """Get employee by email"""
        try:
            data = self.collection.find_one({'email': email})
            if data:
                return Employee.from_dict(data)
            return None
        except Exception as e:
            logger.error(f"Error getting employee by email: {e}")
            return None
    
    def get_all(self, status: Optional[int] = None) -> List[Employee]:
        """Get all employees, optionally filtered by status"""
        try:
            query = {}
            if status is not None:
                query['status'] = status
            
            employees = []
            for data in self.collection.find(query):
                employees.append(Employee.from_dict(data))
            return employees
        except Exception as e:
            logger.error(f"Error getting all employees: {e}")
            return []
    
    def update(self, employee: Employee) -> bool:
        """Update employee"""
        try:
            employee_dict = employee.to_dict()
            result = self.collection.update_one(
                {'employee_id': employee.employee_id},
                {'$set': employee_dict}
            )
            logger.info(f"Updated employee: {employee.employee_id}")
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating employee: {e}")
            return False
    
    def delete(self, employee_id: str) -> bool:
        """Delete employee (soft delete by setting status to 0)"""
        try:
            result = self.collection.update_one(
                {'employee_id': employee_id},
                {'$set': {'status': 0}}
            )
            logger.info(f"Deleted employee: {employee_id}")
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error deleting employee: {e}")
            return False
    
    def search(self, search_term: str) -> List[Employee]:
        """Search employees by name or email"""
        try:
            query = {
                '$or': [
                    {'employee_name': {'$regex': search_term, '$options': 'i'}},
                    {'email': {'$regex': search_term, '$options': 'i'}},
                    {'employee_id': {'$regex': search_term, '$options': 'i'}}
                ]
            }
            employees = []
            for data in self.collection.find(query):
                employees.append(Employee.from_dict(data))
            return employees
        except Exception as e:
            logger.error(f"Error searching employees: {e}")
            return []

