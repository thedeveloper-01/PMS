"""
Payroll service for business logic
"""
from typing import List, Optional, Tuple
from datetime import datetime, date
from calendar import monthrange
from payroll_system.models.payroll import Payroll
from payroll_system.repository.payroll_repository import PayrollRepository
from payroll_system.repository.attendance_repository import AttendanceRepository
from payroll_system.repository.employee_repository import EmployeeRepository
from payroll_system.repository.master_data_repository import MasterDataRepository
from payroll_system.services.attendance_service import AttendanceService
from payroll_system.services.payroll_calculator import PayrollCalculator
import logging

logger = logging.getLogger(__name__)

class PayrollService:
    """Service for payroll business logic"""
    
    def __init__(self):
        self.repository = PayrollRepository()
        self.attendance_repo = AttendanceRepository()
        self.employee_repo = EmployeeRepository()
        self.attendance_service = AttendanceService()
        self.calculator = PayrollCalculator()
    
    def generate_payroll(self, employee_id: str, month: int, year: int, 
                        bonus: float = 0.0) -> Tuple[bool, Optional[Payroll], str]:
        """Generate payroll for an employee for a specific month"""
        try:
            # Check if payroll already exists
            existing = self.repository.get_by_employee_month(employee_id, month, year)
            if existing:
                return False, existing, "Payroll already exists for this month"
            
            # Get employee
            employee = self.employee_repo.get_by_id(employee_id)
            if not employee:
                return False, None, "Employee not found"
            
            # Get attendance summary
            attendance_summary = self.attendance_service.calculate_attendance_summary(
                employee_id, month, year
            )
            
            # Calculate working days (excluding holidays)
            working_days = self._calculate_working_days(month, year)
            
            # Calculate payroll using calculator
            payroll = self.calculator.calculate_payroll(
                employee=employee,
                month=month,
                year=year,
                present_days=attendance_summary['present_days'],
                working_days=working_days,
                lop_days=attendance_summary['lop_days'],
                overtime_hours=attendance_summary['total_overtime'],
                bonus=bonus
            )
            
            # Save to database
            success = self.repository.create(payroll)
            if success:
                return True, payroll, "Payroll generated successfully"
            else:
                return False, None, "Failed to save payroll"
        except Exception as e:
            logger.error(f"Error generating payroll: {e}")
            return False, None, f"Error: {str(e)}"
    
    def _calculate_working_days(self, month: int, year: int) -> int:
        """Calculate working days excluding weekends and holidays"""
        # Get total days in month
        total_days = monthrange(year, month)[1]
        
        # Get holidays
        master_repo = MasterDataRepository()
        holidays = master_repo.get_all_holidays()
        
        # Count weekends (Saturdays and Sundays)
        weekend_count = 0
        holiday_count = 0
        
        for day in range(1, total_days + 1):
            date_obj = date(year, month, day)
            weekday = date_obj.weekday()  # 5 = Saturday, 6 = Sunday
            
            if weekday >= 5:  # Weekend
                weekend_count += 1
            else:
                # Check if it's a holiday
                for holiday in holidays:
                    if holiday.holiday_date == date_obj:
                        holiday_count += 1
                        break
        
        working_days = total_days - weekend_count - holiday_count
        return working_days
    
    def get_payroll(self, employee_id: str, month: int, year: int) -> Optional[Payroll]:
        """Get payroll for an employee"""
        return self.repository.get_by_employee_month(employee_id, month, year)
    
    def get_all_payrolls(self, month: int, year: int) -> List[Payroll]:
        """Get all payrolls for a month"""
        return self.repository.get_all_by_month(month, year)
    
    def update_payroll(self, payroll: Payroll) -> bool:
        """Update payroll"""
        return self.repository.update(payroll)

