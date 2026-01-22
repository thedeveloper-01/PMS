"""
Payroll management widget
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QComboBox, QSpinBox, QDoubleSpinBox, QMessageBox,
                              QFileDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from payroll_system.services.payroll_service import PayrollService
from payroll_system.services.employee_service import EmployeeService
from payroll_system.reports.payslip_generator import PayslipGenerator
from payroll_system.reports.excel_export import ExcelExporter
from datetime import datetime

class PayrollManagementWidget(QWidget):
    """Payroll management widget"""
    
    def __init__(self):
        super().__init__()
        self.payroll_service = PayrollService()
        self.employee_service = EmployeeService()
        self.payslip_generator = PayslipGenerator()
        self.excel_exporter = ExcelExporter()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Payroll Management")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Employee:"))
        self.employee_combo = QComboBox()
        self.load_employees()
        controls_layout.addWidget(self.employee_combo)
        
        controls_layout.addWidget(QLabel("Month:"))
        self.month_spin = QSpinBox()
        self.month_spin.setMinimum(1)
        self.month_spin.setMaximum(12)
        self.month_spin.setValue(datetime.now().month)
        controls_layout.addWidget(self.month_spin)
        
        controls_layout.addWidget(QLabel("Year:"))
        self.year_spin = QSpinBox()
        self.year_spin.setMinimum(2020)
        self.year_spin.setMaximum(2100)
        self.year_spin.setValue(datetime.now().year)
        controls_layout.addWidget(self.year_spin)
        
        controls_layout.addWidget(QLabel("Bonus:"))
        self.bonus_spin = QDoubleSpinBox()
        self.bonus_spin.setMaximum(999999)
        self.bonus_spin.setValue(0)
        controls_layout.addWidget(self.bonus_spin)
        
        generate_btn = QPushButton("Generate Payroll")
        generate_btn.clicked.connect(self.generate_payroll)
        controls_layout.addWidget(generate_btn)
        
        view_btn = QPushButton("View Payroll")
        view_btn.clicked.connect(self.view_payroll)
        controls_layout.addWidget(view_btn)
        
        export_btn = QPushButton("Export to Excel")
        export_btn.clicked.connect(self.export_payroll)
        controls_layout.addWidget(export_btn)
        
        header_layout.addLayout(controls_layout)
        layout.addLayout(header_layout)
        
        # Payroll details table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Employee ID", "Month", "Year", "Gross Salary", "Deductions", "Net Salary"
        ])
        layout.addWidget(self.table)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        payslip_btn = QPushButton("Generate Payslip PDF")
        payslip_btn.clicked.connect(self.generate_payslip)
        action_layout.addWidget(payslip_btn)
        
        layout.addLayout(action_layout)
        
        self.setLayout(layout)
    
    def load_employees(self):
        """Load employees"""
        employees = self.employee_service.get_all_employees(status=1)
        self.employee_combo.clear()
        self.employee_combo.addItem("Select Employee", None)
        for emp in employees:
            self.employee_combo.addItem(f"{emp.employee_id} - {emp.employee_name}", emp.employee_id)
    
    def generate_payroll(self):
        """Generate payroll"""
        employee_id = self.employee_combo.currentData()
        if not employee_id:
            QMessageBox.warning(self, "Warning", "Please select an employee")
            return
        
        month = self.month_spin.value()
        year = self.year_spin.value()
        bonus = self.bonus_spin.value()
        
        success, payroll, message = self.payroll_service.generate_payroll(
            employee_id, month, year, bonus
        )
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.view_payroll()
        else:
            QMessageBox.critical(self, "Error", message)
    
    def view_payroll(self):
        """View payroll"""
        employee_id = self.employee_combo.currentData()
        if not employee_id:
            QMessageBox.warning(self, "Warning", "Please select an employee")
            return
        
        month = self.month_spin.value()
        year = self.year_spin.value()
        
        try:
            payroll = self.payroll_service.get_payroll(employee_id, month, year)
            if not payroll:
                QMessageBox.information(self, "Info", "No payroll found for selected period")
                self.table.setRowCount(0)
                return
            
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem(payroll.employee_id))
            self.table.setItem(0, 1, QTableWidgetItem(str(payroll.month)))
            self.table.setItem(0, 2, QTableWidgetItem(str(payroll.year)))
            self.table.setItem(0, 3, QTableWidgetItem(f"₹{payroll.gross_salary:.2f}"))
            self.table.setItem(0, 4, QTableWidgetItem(f"₹{payroll.total_deductions:.2f}"))
            self.table.setItem(0, 5, QTableWidgetItem(f"₹{payroll.net_salary:.2f}"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading payroll: {str(e)}")
    
    def generate_payslip(self):
        """Generate payslip PDF"""
        employee_id = self.employee_combo.currentData()
        if not employee_id:
            QMessageBox.warning(self, "Warning", "Please select an employee")
            return
        
        month = self.month_spin.value()
        year = self.year_spin.value()
        
        try:
            employee = self.employee_service.get_employee(employee_id)
            payroll = self.payroll_service.get_payroll(employee_id, month, year)
            
            if not payroll:
                QMessageBox.warning(self, "Warning", "No payroll found for selected period")
                return
            
            filepath = self.payslip_generator.generate_payslip(employee, payroll)
            QMessageBox.information(self, "Success", f"Payslip generated:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating payslip: {str(e)}")
    
    def export_payroll(self):
        """Export payroll to Excel"""
        month = self.month_spin.value()
        year = self.year_spin.value()
        
        try:
            payrolls = self.payroll_service.get_all_payrolls(month, year)
            if not payrolls:
                QMessageBox.warning(self, "Warning", "No payrolls found for selected period")
                return
            
            filepath = self.excel_exporter.export_payroll_report(payrolls, month, year)
            QMessageBox.information(self, "Success", f"Payroll exported to:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exporting: {str(e)}")

