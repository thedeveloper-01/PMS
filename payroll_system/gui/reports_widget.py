
"""
Reports widget
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QMessageBox, QFileDialog, QGridLayout,
                              QFrame, QComboBox, QSpinBox, QDateEdit)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from payroll_system.services.employee_service import EmployeeService
from payroll_system.services.payroll_service import PayrollService
from payroll_system.services.attendance_service import AttendanceService
from payroll_system.reports.excel_export import ExcelExporter
from datetime import datetime

class ReportsWidget(QWidget):
    """Reports widget"""
    
    def __init__(self):
        super().__init__()
        self.employee_service = EmployeeService()
        self.payroll_service = PayrollService()
        self.attendance_service = AttendanceService()
        self.excel_exporter = ExcelExporter()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setSpacing(24)
        layout.setContentsMargins(32, 24, 32, 24)
        
        # Header
        header = QLabel("Reports & Analytics")
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # Reports grid
        grid = QGridLayout()
        grid.setSpacing(20)
        
        # Employee List Report Card
        employee_card = self.create_report_card(
            "📊 Employee List",
            "Export complete employee directory with all details",
            "Export to Excel",
            self.export_employee_list
        )
        grid.addWidget(employee_card, 0, 0)
        
        # Payroll Report Card
        payroll_card = self.create_report_card(
            "💰 Payroll Report",
            "Generate payroll report for selected month",
            "Export Payroll",
            self.export_payroll_report
        )
        grid.addWidget(payroll_card, 0, 1)
        
        # Attendance Report Card
        attendance_card = self.create_report_card(
            "✓ Attendance Report",
            "Export monthly attendance records",
            "Export Attendance",
            self.export_attendance_report
        )
        grid.addWidget(attendance_card, 1, 0)
        
        # Salary Summary Card
        summary_card = self.create_report_card(
            "📈 Salary Summary",
            "Annual salary summary and analytics",
            "Generate Summary",
            self.generate_salary_summary
        )
        grid.addWidget(summary_card, 1, 1)
        
        layout.addLayout(grid)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def create_report_card(self, title: str, description: str, button_text: str, callback):
        """Create a report card"""
        card = QFrame()
        card.setObjectName("Card")
        card.setMinimumHeight(180)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title with icon
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 700;
                color: #ffffff;
            }
        """)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #92a4c9;
                line-height: 1.4;
            }
        """)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        # Button
        btn = QPushButton(button_text)
        btn.setObjectName("PrimaryButton")
        btn.clicked.connect(callback)
        layout.addWidget(btn)
        
        card.setLayout(layout)
        return card
    
    def export_employee_list(self):
        """Export employee list to Excel"""
        try:
            employees = self.employee_service.get_all_employees(status=1)
            if not employees:
                QMessageBox.warning(self, "Warning", "No employees found")
                return
            
            filepath, _ = QFileDialog.getSaveFileName(
                self, "Save Employee List",
                f"employee_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "Excel Files (*.xlsx)"
            )
            
            if filepath:
                self.excel_exporter.export_employee_list(employees, filepath)
                QMessageBox.information(self, "Success", f"Employee list exported to:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exporting: {str(e)}")
    
    def export_payroll_report(self):
        """Export payroll report"""
        try:
            # Create a simple dialog for month/year selection
            from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout
            
            dialog = QDialog(self)
            dialog.setWindowTitle("Select Period")
            layout = QFormLayout(dialog)
            
            month_spin = QSpinBox()
            month_spin.setMinimum(1)
            month_spin.setMaximum(12)
            month_spin.setValue(datetime.now().month)
            
            year_spin = QSpinBox()
            year_spin.setMinimum(2020)
            year_spin.setMaximum(2100)
            year_spin.setValue(datetime.now().year)
            
            layout.addRow("Month:", month_spin)
            layout.addRow("Year:", year_spin)
            
            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addRow(buttons)
            
            if dialog.exec() == QDialog.Accepted:
                month = month_spin.value()
                year = year_spin.value()
                
                payrolls = self.payroll_service.get_all_payrolls(month, year)
                if not payrolls:
                    QMessageBox.warning(self, "Warning", f"No payrolls found for {month}/{year}")
                    return
                
                filepath, _ = QFileDialog.getSaveFileName(
                    self, "Save Payroll Report",
                    f"payroll_report_{year}_{month:02d}.xlsx",
                    "Excel Files (*.xlsx)"
                )
                
                if filepath:
                    self.excel_exporter.export_payroll_report(payrolls, month, year, filepath)
                    QMessageBox.information(self, "Success", f"Payroll report exported to:\n{filepath}")
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exporting: {str(e)}")
    
    def export_attendance_report(self):
        """Export attendance report"""
        QMessageBox.information(self, "Info", "Attendance report export functionality can be extended here")
    
    def generate_salary_summary(self):
        """Generate salary summary"""
        QMessageBox.information(self, "Info", "Salary summary functionality can be extended here")
