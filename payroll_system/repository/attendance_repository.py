"""
Attendance repository for database operations
"""
from typing import List, Optional
from datetime import date, datetime
from payroll_system.models.attendance import Attendance
from payroll_system.utils.database import db
import logging

logger = logging.getLogger(__name__)

class AttendanceRepository:
    """Repository for attendance data operations"""
    
    def __init__(self):
        self.collection = db.get_db().attendance
    
    def create(self, attendance: Attendance) -> bool:
        """Create attendance record"""
        try:
            attendance_dict = attendance.to_dict()
            result = self.collection.insert_one(attendance_dict)
            logger.info(f"Created attendance for employee: {attendance.employee_id}")
            return result.inserted_id is not None
        except Exception as e:
            logger.error(f"Error creating attendance: {e}")
            return False
    
    def get_by_employee_and_date(self, employee_id: str, att_date: date) -> Optional[Attendance]:
        """Get attendance by employee ID and date"""
        try:
            data = self.collection.find_one({
                'employee_id': employee_id,
                'date': att_date.isoformat() if isinstance(att_date, date) else str(att_date)
            })
            if data:
                return Attendance.from_dict(data)
            return None
        except Exception as e:
            logger.error(f"Error getting attendance: {e}")
            return None
    
    def get_by_employee_month(self, employee_id: str, month: int, year: int) -> List[Attendance]:
        """Get all attendance records for an employee in a month"""
        try:
            start_date = f"{year}-{month:02d}-01"
            if month == 12:
                end_date = f"{year + 1}-01-01"
            else:
                end_date = f"{year}-{month + 1:02d}-01"
            
            attendances = []
            for data in self.collection.find({
                'employee_id': employee_id,
                'date': {'$gte': start_date, '$lt': end_date}
            }):
                attendances.append(Attendance.from_dict(data))
            return attendances
        except Exception as e:
            logger.error(f"Error getting monthly attendance: {e}")
            return []
    
    def update(self, attendance: Attendance) -> bool:
        """Update attendance record"""
        try:
            attendance_dict = attendance.to_dict()
            result = self.collection.update_one(
                {
                    'employee_id': attendance.employee_id,
                    'date': attendance.date.isoformat() if isinstance(attendance.date, date) else str(attendance.date)
                },
                {'$set': attendance_dict}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating attendance: {e}")
            return False
    
    def get_all_by_employee(self, employee_id: str) -> List[Attendance]:
        """Get all attendance records for an employee"""
        try:
            attendances = []
            for data in self.collection.find({'employee_id': employee_id}).sort('date', -1):
                attendances.append(Attendance.from_dict(data))
            return attendances
        except Exception as e:
            logger.error(f"Error getting employee attendance: {e}")
            return []

