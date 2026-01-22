"""
Attendance service for business logic
"""
from typing import List, Optional
from datetime import date, time, datetime
from payroll_system.models.attendance import Attendance
from payroll_system.repository.attendance_repository import AttendanceRepository
import logging

logger = logging.getLogger(__name__)

class AttendanceService:
    """Service for attendance business logic"""
    
    def __init__(self):
        self.repository = AttendanceRepository()
    
    def mark_attendance(self, employee_id: str, att_date: date, 
                       checkin_time: Optional[time] = None,
                       checkout_time: Optional[time] = None) -> bool:
        """Mark attendance for an employee"""
        try:
            # Check if attendance already exists
            existing = self.repository.get_by_employee_and_date(employee_id, att_date)
            
            if existing:
                # Update existing attendance
                existing.checkin_time = checkin_time
                existing.checkout_time = checkout_time
                existing.status = 'present' if checkin_time else 'absent'
                return self.repository.update(existing)
            else:
                # Create new attendance
                attendance = Attendance(
                    employee_id=employee_id,
                    date=att_date,
                    checkin_time=checkin_time,
                    checkout_time=checkout_time
                )
                return self.repository.create(attendance)
        except Exception as e:
            logger.error(f"Error marking attendance: {e}")
            return False
    
    def get_attendance(self, employee_id: str, att_date: date) -> Optional[Attendance]:
        """Get attendance for a specific date"""
        return self.repository.get_by_employee_and_date(employee_id, att_date)
    
    def get_monthly_attendance(self, employee_id: str, month: int, year: int) -> List[Attendance]:
        """Get all attendance records for a month"""
        return self.repository.get_by_employee_month(employee_id, month, year)
    
    def mark_lop(self, employee_id: str, att_date: date) -> bool:
        """Mark Loss of Pay for an employee"""
        try:
            attendance = self.repository.get_by_employee_and_date(employee_id, att_date)
            if not attendance:
                attendance = Attendance(employee_id=employee_id, date=att_date)
            
            attendance.lop = True
            attendance.status = 'lop'
            return self.repository.update(attendance) if attendance.attendance_id else self.repository.create(attendance)
        except Exception as e:
            logger.error(f"Error marking LOP: {e}")
            return False
    
    def calculate_attendance_summary(self, employee_id: str, month: int, year: int) -> dict:
        """Calculate attendance summary for a month"""
        attendances = self.get_monthly_attendance(employee_id, month, year)
        
        present_days = sum(1 for att in attendances if att.status == 'present')
        absent_days = sum(1 for att in attendances if att.status == 'absent')
        lop_days = sum(1 for att in attendances if att.lop)
        total_overtime = sum(att.overtime_hours for att in attendances)
        
        return {
            'present_days': present_days,
            'absent_days': absent_days,
            'lop_days': lop_days,
            'total_overtime': total_overtime,
            'total_days': len(attendances)
        }

