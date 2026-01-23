"""
Payslip PDF generator using ReportLab
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from payroll_system.models.payroll import Payroll
from payroll_system.models.employee import Employee
from payroll_system.repository.master_data_repository import MasterDataRepository
from payroll_system.config import PAYSLIPS_DIR, get_resource_path
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
                        branch_name: str = "PayMaster Solutions") -> str:
        """Generate professional payslip PDF and return file path"""
        try:
            # Create filename
            filename = f"payslip_{employee.employee_id}_{payroll.year}_{payroll.month:02d}.pdf"
            filepath = PAYSLIPS_DIR / filename
            
            # --- Font Registration (Windows) ---
            # We need a TTF font to support the Rupee symbol (₹). Helvetica (standard PDF font) doesn't support it.
            # Arial is standard on Windows.
            try:
                pdfmetrics.registerFont(TTFont('Arial', 'C:\\Windows\\Fonts\\arial.ttf'))
                pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:\\Windows\\Fonts\\arialbd.ttf'))
                font_regular = 'Arial'
                font_bold = 'Arial-Bold'
            except:
                # Fallback if font not found (e.g. Linux/Mac), though user is on Windows
                font_regular = 'Helvetica'
                font_bold = 'Helvetica-Bold'
            
            # Create PDF document
            doc = SimpleDocTemplate(
                str(filepath), 
                pagesize=A4,
                rightMargin=40, leftMargin=40, 
                topMargin=40, bottomMargin=40
            )
            story = []
            
            # --- Colors ---
            primary_color = colors.HexColor('#0f172a')  # Dark Blue
            secondary_color = colors.HexColor('#3b82f6') # Brand Blue
            light_bg = colors.HexColor('#f1f5f9')
            
            # --- Header Section (Logo + Company Info) ---
            # Try to load logo
            logo_path = get_resource_path("resources/app_icon.png")
            if os.path.exists(logo_path):
                logo = Image(logo_path, width=40, height=40)
            else:
                logo = Spacer(40, 40) # Fallback

            # Note: Using fontName explicitly in Paragraph styles if using custom font
            self.styles['Normal'].fontName = font_regular
            self.styles['Heading2'].fontName = font_bold
            
            company_info = [
                [logo, Paragraph(f"<b>{branch_name}</b><br/><font size=9>Excellence in Payroll Management</font>", self.styles['Normal'])],
            ]
            
            header_table = Table(company_info, colWidths=[50, 400])
            header_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(header_table)
            story.append(Spacer(1, 0.2*inch))
            
            # Title
            month_name = datetime(payroll.year, payroll.month, 1).strftime("%B %Y")
            story.append(Paragraph(f"PAYSLIP FOR THE PERIOD OF {month_name.upper()}", 
                                 ParagraphStyle('Title', parent=self.styles['Heading2'], alignment=TA_CENTER, textColor=primary_color, fontName=font_bold)))
            story.append(Spacer(1, 0.2*inch))
            
            # --- Employee Info Section (Grid Layout) ---
            emp_data = [
                [Paragraph('<b>Employee Name</b>', self.styles['Normal']), employee.employee_name,
                 Paragraph('<b>Designation</b>', self.styles['Normal']), self._get_designation_name(employee.designation_id)],
                [Paragraph('<b>Employee ID</b>', self.styles['Normal']), employee.employee_id,
                 Paragraph('<b>Bank Account</b>', self.styles['Normal']), employee.bank_account_number or 'N/A'],
                [Paragraph('<b>Department</b>', self.styles['Normal']), self._get_department_name(employee.department_id),
                 Paragraph('<b>PAN</b>', self.styles['Normal']), getattr(employee, 'pan_number', 'N/A') or 'N/A'],
                [Paragraph('<b>Location</b>', self.styles['Normal']), "Bangalore", # Placeholder
                 Paragraph('<b>UAN</b>', self.styles['Normal']), getattr(employee, 'uan_number', 'N/A') or 'N/A'],
            ]
            
            emp_table = Table(emp_data, colWidths=[1.3*inch, 2.2*inch, 1.3*inch, 2.2*inch])
            emp_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), light_bg),
                ('GRID', (0,0), (-1,-1), 0.5, colors.white),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('PADDING', (0,0), (-1,-1), 6),
                ('FONTNAME', (0,0), (-1,-1), font_regular),
            ]))
            story.append(emp_table)
            story.append(Spacer(1, 0.3*inch))
            
            # --- Financials (Side by Side) ---
            # Earnings Data
            earnings_data = [['EARNINGS', 'AMOUNT']]
            earnings_list = [
                ('Basic Salary', payroll.basic_salary),
                ('HRA', payroll.hra),
                ('Conveyance', payroll.da), # Mapping DA/Conveyance generally
                ('Special Allowance', payroll.allowances),
                ('Bonus', payroll.bonus),
                ('Overtime', payroll.overtime_pay),
            ]
            for desc, amt in earnings_list:
                if amt > 0:
                    earnings_data.append([desc, f"₹{amt:,.2f}"])
            
            # Always ensure at least some rows for alignment
            while len(earnings_data) < 8:
                earnings_data.append(['', ''])
                
            earnings_data.append(['Gross Earnings', f"₹{payroll.gross_salary:,.2f}"])

            # Deductions Data
            deductions_data = [['DEDUCTIONS', 'AMOUNT']]
            deductions_list = [
                ('Provident Fund', payroll.pf),
                ('Professional Tax', payroll.pt),
                ('ESI', payroll.esi),
                ('Income Tax', 0.00), # Placeholder
                ('Loan Recovery', 0.00),
                ('LOP Deduction', payroll.lop_deduction),
            ]
            for desc, amt in deductions_list:
                if amt > 0:
                    deductions_data.append([desc, f"₹{amt:,.2f}"])
            
            while len(deductions_data) < len(earnings_data) - 1:
                deductions_data.append(['', ''])
            
            deductions_data.append(['Total Deductions', f"₹{payroll.total_deductions:,.2f}"])

            # Construct Side-by-Side Table
            combined_data = []
            rows = max(len(earnings_data), len(deductions_data))
            
            for i in range(rows):
                # Earning Part
                e_desc = earnings_data[i][0] if i < len(earnings_data) else ""
                e_amt = earnings_data[i][1] if i < len(earnings_data) else ""
                
                # Deduction Part
                d_desc = deductions_data[i][0] if i < len(deductions_data) else ""
                d_amt = deductions_data[i][1] if i < len(deductions_data) else ""
                
                combined_data.append([e_desc, e_amt, '', d_desc, d_amt])

            # Adjust the last row to be the Totals
            combined_data[-1] = [
                'Gross Earnings', f"₹{payroll.gross_salary:,.2f}", 
                '', 
                'Total Deductions', f"₹{payroll.total_deductions:,.2f}"
            ]
            
            # Table Style
            fin_table = Table(combined_data, colWidths=[2.2*inch, 1.2*inch, 0.2*inch, 2.2*inch, 1.2*inch])
            
            # Base Style
            fin_style = [
                ('BACKGROUND', (0,0), (1,0), secondary_color), # Earnings Header
                ('BACKGROUND', (3,0), (4,0), secondary_color), # Deductions Header
                ('TEXTCOLOR', (0,0), (1,0), colors.white),
                ('TEXTCOLOR', (3,0), (4,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), font_bold),
                ('ALIGN', (1,0), (1,-1), 'RIGHT'),
                ('ALIGN', (4,0), (4,-1), 'RIGHT'),
                ('PADDING', (0,0), (-1,-1), 8),
                ('GRID', (0,0), (1,-1), 0.5, colors.lightgrey), # Grid for earnings
                ('GRID', (3,0), (4,-1), 0.5, colors.lightgrey), # Grid for deductions
                
                # Content Font is Regular Arial
                ('FONTNAME', (0,1), (-1,-2), font_regular),

                # Totals Row (Distinct styling)
                ('FONTNAME', (0,-1), (-1,-1), font_bold),
                ('BACKGROUND', (0,-1), (1,-1), colors.HexColor('#e2e8f0')), # Slate 200
                ('BACKGROUND', (3,-1), (4,-1), colors.HexColor('#e2e8f0')), 
                
                # Clean borders for totals (Top and Bottom only to separate)
                ('LINEABOVE', (0,-1), (1,-1), 1, colors.black),
                ('LINEBELOW', (0,-1), (1,-1), 1, colors.black),
                ('LINEBEFORE', (0,-1), (0,-1), 1, colors.black),
                ('LINEAFTER', (1,-1), (1,-1), 1, colors.black),
                
                ('LINEABOVE', (3,-1), (4,-1), 1, colors.black),
                ('LINEBELOW', (3,-1), (4,-1), 1, colors.black),
                ('LINEBEFORE', (3,-1), (3,-1), 1, colors.black),
                ('LINEAFTER', (4,-1), (4,-1), 1, colors.black),
            ]
            
            fin_table.setStyle(TableStyle(fin_style))
            story.append(fin_table)
            story.append(Spacer(1, 0.3*inch))
            
            # --- Net Pay & Words ---
            # Using Paragraph for Net Pay to handle font size and leading better than passing string to Table
            net_pay_text = Paragraph(f"Net Payable:  ₹{payroll.net_salary:,.2f}", 
                                   ParagraphStyle('NetPay', parent=self.styles['Normal'], 
                                                alignment=TA_CENTER, textColor=colors.white, 
                                                fontSize=18, fontName=font_bold, leading=22))
            
            net_pay_data = [[net_pay_text]]
            
            net_table = Table(net_pay_data, colWidths=[7*inch])
            net_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), primary_color),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 15), 
                ('TOPPADDING', (0,0), (-1,-1), 15),
            ]))
            story.append(net_table)
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph(f"<font size=9>Amount in words: {self._number_to_words(payroll.net_salary)} Only</font>", 
                                 ParagraphStyle('Words', alignment=TA_CENTER, textColor=colors.grey, fontName=font_regular)))
            
            story.append(Spacer(1, 0.4*inch))
            
            # --- Attendance & Leave Summary ---
            att_data = [[
                Paragraph(f"<b>Attendance Details</b><br/>Present: {payroll.present_days} | LOP: {payroll.lop_days}", self.styles['Normal']),
                Paragraph(f"<b>Leave Balance</b><br/>CL: 1 | SL: 0 | PL: 4", self.styles['Normal']) # Placeholder
            ]]
            att_table = Table(att_data, colWidths=[3.5*inch, 3.5*inch])
            att_table.setStyle(TableStyle([
                ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('PADDING', (0,0), (-1,-1), 8),
                ('FONTNAME', (0,0), (-1,-1), font_regular),
            ]))
            story.append(att_table)
            
            story.append(Spacer(1, 0.6*inch))
            
            # --- Footer ---
            footer = Paragraph("This is a computer generated payslip and does not require a signature.", 
                             ParagraphStyle('Footer', alignment=TA_CENTER, fontSize=8, textColor=colors.grey, fontName=font_regular))
            story.append(footer)

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

    def _get_department_name(self, dept_id):
        """Get department name by ID"""
        try:
            master_repo = MasterDataRepository()
            depts = master_repo.get_all_departments()
            for d in depts:
                if d.department_id == dept_id:
                    return d.department_name
            return "N/A"
        except:
            return "N/A"

    def _number_to_words(self, amount):
        """Convert amount to words (Simplified)"""
        try:
            # Basic implementation - for full features need separate library like num2words
            # But we can do a simple version for now
            return f"{int(amount)} Rupees" 
        except:
            return ""

