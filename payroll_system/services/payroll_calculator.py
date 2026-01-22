"""
Payroll calculation engine with statutory deductions
"""
from payroll_system.models.payroll import Payroll
from payroll_system.models.employee import Employee
from payroll_system.config import PF_RATE, ESI_RATE, PT_SLABS
from payroll_system.utils.validators import calculate_pt
import logging

logger = logging.getLogger(__name__)

class PayrollCalculator:
    """Payroll calculation engine"""
    
    def calculate_payroll(self, employee: Employee, month: int, year: int,
                         present_days: int, working_days: int, lop_days: int,
                         overtime_hours: float = 0.0, bonus: float = 0.0) -> Payroll:
        """Calculate complete payroll with all deductions"""
        
        # Calculate daily salary
        daily_salary = employee.basic_salary / working_days if working_days > 0 else 0
        
        # Calculate basic salary for present days
        basic_salary = daily_salary * present_days
        
        # Calculate LOP deduction
        lop_deduction = daily_salary * lop_days
        
        # Calculate HRA (40% of basic salary)
        hra = basic_salary * 0.40
        
        # Calculate DA (20% of basic salary)
        da = basic_salary * 0.20
        
        # Calculate allowances (10% of basic salary)
        allowances = basic_salary * 0.10
        
        # Calculate overtime pay (1.5x hourly rate)
        hourly_rate = basic_salary / (working_days * 8) if working_days > 0 else 0
        overtime_pay = overtime_hours * hourly_rate * 1.5
        
        # Calculate gross salary
        gross_salary = basic_salary + hra + da + allowances + bonus + overtime_pay
        
        # Calculate statutory deductions
        
        # PF (12% of basic salary, capped at 1800)
        pf = min(basic_salary * PF_RATE, 1800)
        
        # ESI (0.75% of gross salary, if applicable - typically for salary < 21000)
        esi = 0.0
        if gross_salary < 21000:
            esi = gross_salary * ESI_RATE
        
        # Professional Tax (based on salary slabs)
        pt = calculate_pt(basic_salary)
        
        # Total deductions
        total_deductions = pf + esi + pt + lop_deduction
        
        # Net salary
        net_salary = gross_salary - total_deductions
        
        # Create payroll object
        payroll = Payroll(
            employee_id=employee.employee_id,
            month=month,
            year=year,
            present_days=present_days,
            working_days=working_days,
            absent_days=working_days - present_days - lop_days,
            leave_days=0,  # Can be calculated separately if needed
            lop_days=lop_days,
            overtime_hours=overtime_hours,
            basic_salary=basic_salary,
            hra=hra,
            da=da,
            allowances=allowances,
            bonus=bonus,
            overtime_pay=overtime_pay,
            gross_salary=gross_salary,
            pf=pf,
            esi=esi,
            pt=pt,
            lop_deduction=lop_deduction,
            other_deductions=0.0,
            total_deductions=total_deductions,
            net_salary=net_salary,
            status='processed'
        )
        
        return payroll

