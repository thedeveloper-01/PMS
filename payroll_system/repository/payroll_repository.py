"""
Payroll repository for database operations
"""
from typing import List, Optional
from payroll_system.models.payroll import Payroll
from payroll_system.utils.database import db
import logging

logger = logging.getLogger(__name__)

class PayrollRepository:
    """Repository for payroll data operations"""
    
    def __init__(self):
        self.collection = db.get_db().payrolls
    
    def create(self, payroll: Payroll) -> bool:
        """Create payroll record"""
        try:
            payroll_dict = payroll.to_dict()
            result = self.collection.insert_one(payroll_dict)
            logger.info(f"Created payroll for employee: {payroll.employee_id}")
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"Error creating payroll: {e}")
            return False
    
    def get_by_employee_month(self, employee_id: str, month: int, year: int) -> Optional[Payroll]:
        """Get payroll by employee, month, and year"""
        try:
            data = self.collection.find_one({
                'employee_id': employee_id,
                'month': month,
                'year': year
            })
            if data:
                return Payroll.from_dict(data)
            return None
        except Exception as e:
            logger.error(f"Error getting payroll: {e}")
            return None
    
    def get_all_by_month(self, month: int, year: int) -> List[Payroll]:
        """Get all payrolls for a month"""
        try:
            payrolls = []
            for data in self.collection.find({'month': month, 'year': year}):
                payrolls.append(Payroll.from_dict(data))
            return payrolls
        except Exception as e:
            logger.error(f"Error getting monthly payrolls: {e}")
            return []
    
    def update(self, payroll: Payroll) -> bool:
        """Update payroll record"""
        try:
            payroll_dict = payroll.to_dict()
            result = self.collection.update_one(
                {
                    'employee_id': payroll.employee_id,
                    'month': payroll.month,
                    'year': payroll.year
                },
                {'$set': payroll_dict}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating payroll: {e}")
            return False
    
    def get_all_by_employee(self, employee_id: str) -> List[Payroll]:
        """Get all payrolls for an employee"""
        try:
            payrolls = []
            for data in self.collection.find({'employee_id': employee_id}).sort([('year', -1), ('month', -1)]):
                payrolls.append(Payroll.from_dict(data))
            return payrolls
        except Exception as e:
            logger.error(f"Error getting employee payrolls: {e}")
    def delete(self, employee_id: str, month: int, year: int) -> bool:
        """Delete payroll record"""
        try:
            result = self.collection.delete_one({
                'employee_id': employee_id,
                'month': month,
                'year': year
            })
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting payroll: {e}")
            return False

