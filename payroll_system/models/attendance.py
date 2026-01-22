"""
Attendance data model
"""
from datetime import datetime, date, time
from typing import Optional

class Attendance:
    """Attendance model"""
    
    def __init__(self, employee_id: str, date: date, 
                 checkin_time: Optional[time] = None,
                 checkout_time: Optional[time] = None,
                 **kwargs):
        self.attendance_id = kwargs.get('attendance_id', None)
        self.employee_id = employee_id
        self.date = date
        self.checkin_time = checkin_time
        self.checkout_time = checkout_time
        self.status = kwargs.get('status', 'present' if checkin_time else 'absent')
        self.overtime_hours = kwargs.get('overtime_hours', 0.0)
        self.lop = kwargs.get('lop', False)  # Loss of Pay
    
    def to_dict(self):
        """Convert attendance to dictionary for MongoDB storage"""
        return {
            'attendance_id': self.attendance_id,
            'employee_id': self.employee_id,
            'date': self.date.isoformat() if isinstance(self.date, date) else str(self.date),
            'checkin_time': self.checkin_time.isoformat() if self.checkin_time else None,
            'checkout_time': self.checkout_time.isoformat() if self.checkout_time else None,
            'status': self.status,
            'overtime_hours': self.overtime_hours,
            'lop': self.lop
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create attendance from dictionary"""
        from datetime import datetime as dt
        
        # Parse date
        att_date = None
        if data.get('date'):
            if isinstance(data['date'], str):
                att_date = dt.strptime(data['date'], '%Y-%m-%d').date()
            else:
                att_date = data['date']
        
        # Parse times
        checkin = None
        if data.get('checkin_time'):
            if isinstance(data['checkin_time'], str):
                checkin = dt.strptime(data['checkin_time'], '%H:%M:%S').time()
            else:
                checkin = data['checkin_time']
        
        checkout = None
        if data.get('checkout_time'):
            if isinstance(data['checkout_time'], str):
                checkout = dt.strptime(data['checkout_time'], '%H:%M:%S').time()
            else:
                checkout = data['checkout_time']
        
        return cls(
            employee_id=data['employee_id'],
            date=att_date,
            checkin_time=checkin,
            checkout_time=checkout,
            attendance_id=data.get('attendance_id'),
            status=data.get('status', 'present'),
            overtime_hours=data.get('overtime_hours', 0.0),
            lop=data.get('lop', False)
        )

