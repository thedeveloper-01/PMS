"""
Payroll data model
"""
from datetime import datetime, date

class Payroll:
    """Payroll model"""
    
    def __init__(self, employee_id: str, month: int, year: int, **kwargs):
        self.payroll_id = kwargs.get('payroll_id', None)
        self.employee_id = employee_id
        self.month = month
        self.year = year
        
        # Attendance details
        self.present_days = kwargs.get('present_days', 0)
        self.working_days = kwargs.get('working_days', 0)
        self.absent_days = kwargs.get('absent_days', 0)
        self.leave_days = kwargs.get('leave_days', 0)
        self.lop_days = kwargs.get('lop_days', 0)
        self.overtime_hours = kwargs.get('overtime_hours', 0.0)
        
        # Earnings
        self.basic_salary = kwargs.get('basic_salary', 0.0)
        self.hra = kwargs.get('hra', 0.0)
        self.da = kwargs.get('da', 0.0)
        self.allowances = kwargs.get('allowances', 0.0)
        self.bonus = kwargs.get('bonus', 0.0)
        self.overtime_pay = kwargs.get('overtime_pay', 0.0)
        self.gross_salary = kwargs.get('gross_salary', 0.0)
        
        # Deductions
        self.pf = kwargs.get('pf', 0.0)
        self.esi = kwargs.get('esi', 0.0)
        self.pt = kwargs.get('pt', 0.0)
        self.lop_deduction = kwargs.get('lop_deduction', 0.0)
        self.other_deductions = kwargs.get('other_deductions', 0.0)
        self.total_deductions = kwargs.get('total_deductions', 0.0)
        
        # Net Salary
        self.net_salary = kwargs.get('net_salary', 0.0)
        
        # Metadata
        self.created_date = kwargs.get('created_date', datetime.now().date())
        self.status = kwargs.get('status', 'draft')  # draft, processed, paid
    
    def to_dict(self):
        """Convert payroll to dictionary for MongoDB storage"""
        return {
            'payroll_id': self.payroll_id,
            'employee_id': self.employee_id,
            'month': self.month,
            'year': self.year,
            'present_days': self.present_days,
            'working_days': self.working_days,
            'absent_days': self.absent_days,
            'leave_days': self.leave_days,
            'lop_days': self.lop_days,
            'overtime_hours': self.overtime_hours,
            'basic_salary': self.basic_salary,
            'hra': self.hra,
            'da': self.da,
            'allowances': self.allowances,
            'bonus': self.bonus,
            'overtime_pay': self.overtime_pay,
            'gross_salary': self.gross_salary,
            'pf': self.pf,
            'esi': self.esi,
            'pt': self.pt,
            'lop_deduction': self.lop_deduction,
            'other_deductions': self.other_deductions,
            'total_deductions': self.total_deductions,
            'net_salary': self.net_salary,
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, date) else str(self.created_date),
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create payroll from dictionary"""
        from datetime import datetime as dt
        
        created_date = None
        if data.get('created_date'):
            if isinstance(data['created_date'], str):
                created_date = dt.strptime(data['created_date'], '%Y-%m-%d').date()
            else:
                created_date = data['created_date']
        
        return cls(
            employee_id=data['employee_id'],
            month=data['month'],
            year=data['year'],
            payroll_id=data.get('payroll_id'),
            present_days=data.get('present_days', 0),
            working_days=data.get('working_days', 0),
            absent_days=data.get('absent_days', 0),
            leave_days=data.get('leave_days', 0),
            lop_days=data.get('lop_days', 0),
            overtime_hours=data.get('overtime_hours', 0.0),
            basic_salary=data.get('basic_salary', 0.0),
            hra=data.get('hra', 0.0),
            da=data.get('da', 0.0),
            allowances=data.get('allowances', 0.0),
            bonus=data.get('bonus', 0.0),
            overtime_pay=data.get('overtime_pay', 0.0),
            gross_salary=data.get('gross_salary', 0.0),
            pf=data.get('pf', 0.0),
            esi=data.get('esi', 0.0),
            pt=data.get('pt', 0.0),
            lop_deduction=data.get('lop_deduction', 0.0),
            other_deductions=data.get('other_deductions', 0.0),
            total_deductions=data.get('total_deductions', 0.0),
            net_salary=data.get('net_salary', 0.0),
            created_date=created_date,
            status=data.get('status', 'draft')
        )

