"""
Payslip PDF generator using ReportLab
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from payroll_system.models.payroll import Payroll
from payroll_system.models.employee import Employee
from payroll_system.repository.master_data_repository import MasterDataRepository
from payroll_system.config import PAYSLIPS_DIR
from datetime import datetime
import os

class PayslipGenerator:
    """Generate payslip PDF using ReportLab"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CompanyName',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#5C7EB5'),
            alignment=TA_CENTER,
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.white,
            backColor=colors.HexColor('#5C7EB5'),
            alignment=TA_CENTER,
            spaceAfter=6
        ))
    
    def generate_payslip(self, employee: Employee, payroll: Payroll, 
                        branch_name: str = "Company Branch") -> str:
        """Generate payslip PDF and return file path"""
        try:
            # Create filename
            filename = f"payslip_{employee.employee_id}_{payroll.year}_{payroll.month:02d}.pdf"
            filepath = PAYSLIPS_DIR / filename
            
            # Create PDF document
            doc = SimpleDocTemplate(str(filepath), pagesize=A4)
            story = []
            
            # Company Header
            story.append(Paragraph(branch_name, self.styles['CompanyName']))
            story.append(Paragraph("Salary Slip", self.styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Employee Information
            emp_data = [
                ['Name', employee.employee_name],
                ['Employee ID', employee.employee_id],
                ['Designation', self._get_designation_name(employee.designation_id)],
                ['Bank Account', employee.bank_account_number or 'N/A']
            ]
            
            emp_table = Table(emp_data, colWidths=[2*inch, 4*inch])
            emp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#5C7EB5')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (1, 0), (1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(emp_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Earnings Section
            earnings_data = [
                ['Description', 'Amount'],
                ['Basic Salary', f"₹{payroll.basic_salary:.2f}"],
                ['HRA', f"₹{payroll.hra:.2f}"],
                ['DA', f"₹{payroll.da:.2f}"],
                ['Allowances', f"₹{payroll.allowances:.2f}"],
                ['Bonus', f"₹{payroll.bonus:.2f}"],
                ['Overtime Pay', f"₹{payroll.overtime_pay:.2f}"],
                ['Gross Salary', f"₹{payroll.gross_salary:.2f}"]
            ]
            
            earnings_table = Table(earnings_data, colWidths=[3.5*inch, 2.5*inch])
            earnings_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5C7EB5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8E8E8')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold')
            ]))
            story.append(earnings_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Deductions Section
            deductions_data = [
                ['Description', 'Amount'],
                ['PF', f"₹{payroll.pf:.2f}"],
                ['ESI', f"₹{payroll.esi:.2f}"],
                ['Professional Tax', f"₹{payroll.pt:.2f}"],
                ['LOP Deduction', f"₹{payroll.lop_deduction:.2f}"],
                ['Total Deductions', f"₹{payroll.total_deductions:.2f}"]
            ]
            
            deductions_table = Table(deductions_data, colWidths=[3.5*inch, 2.5*inch])
            deductions_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5C7EB5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8E8E8')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold')
            ]))
            story.append(deductions_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Net Salary
            net_salary_data = [
                ['Net Salary', f"₹{payroll.net_salary:.2f}"]
            ]
            
            net_table = Table(net_salary_data, colWidths=[6*inch])
            net_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#5C7EB5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12)
            ]))
            story.append(net_table)
            
            # Attendance Summary
            story.append(Spacer(1, 0.3*inch))
            att_data = [
                ['Present Days', str(payroll.present_days)],
                ['Working Days', str(payroll.working_days)],
                ['LOP Days', str(payroll.lop_days)],
                ['Overtime Hours', f"{payroll.overtime_hours:.2f}"]
            ]
            
            att_table = Table(att_data, colWidths=[3*inch, 3*inch])
            att_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5C7EB5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(att_table)
            
            # Build PDF
            doc.build(story)
            
            return str(filepath)
        except Exception as e:
            raise Exception(f"Error generating payslip: {str(e)}")
    
    def _get_designation_name(self, designation_id):
        """Get designation name by ID"""
        try:
            master_repo = MasterDataRepository()
            designations = master_repo.get_all_designations()
            for des in designations:
                if des.designation_id == designation_id:
                    return des.designation_name
            return "N/A"
        except:
            return "N/A"

