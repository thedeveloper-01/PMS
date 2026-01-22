
"""
Payroll management widget
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QComboBox, QSpinBox, QDoubleSpinBox, QMessageBox,
                              QFileDialog, QHeaderView)
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
        layout.setSpacing(20)
        layout.setContentsMargins(32, 24, 32, 24)
        
        # Header
        header = QLabel("Payroll Management")
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(12)
        
        # Employee filter
        toolbar.addWidget(QLabel("Employee:"))
        self.employee_combo = QComboBox()
        self.load_employees()
        self.employee_combo.setMinimumWidth(250)
        toolbar.addWidget(self.employee_combo)
        
        # Month filter
        toolbar.addWidget(QLabel("Month:"))
        self.month_spin = QSpinBox()
        self.month_spin.setMinimum(1)
        self.month_spin.setMaximum(12)
        self.month_spin.setValue(datetime.now().month)
        self.month_spin.setFixedWidth(80)
        toolbar.addWidget(self.month_spin)
        
        # Year filter
        toolbar.addWidget(QLabel("Year:"))
        self.year_spin = QSpinBox()
        self.year_spin.setMinimum(2020)
        self.year_spin.setMaximum(2100)
        self.year_spin.setValue(datetime.now().year)
        self.year_spin.setFixedWidth(100)
        toolbar.addWidget(self.year_spin)
        
        # Bonus input
        toolbar.addWidget(QLabel("Bonus:"))
        self.bonus_spin = QDoubleSpinBox()
        self.bonus_spin.setMaximum(999999)
        self.bonus_spin.setValue(0)
        self.bonus_spin.setPrefix("₹ ")
        self.bonus_spin.setFixedWidth(120)
        toolbar.addWidget(self.bonus_spin)
        
        toolbar.addStretch()
        
        # Action buttons
        view_btn = QPushButton("📊 View Payroll")
        view_btn.clicked.connect(self.view_payroll)
        toolbar.addWidget(view_btn)
        
        export_btn = QPushButton("📥 Export Excel")
        export_btn.clicked.connect(self.export_payroll)
        toolbar.addWidget(export_btn)
        
        generate_btn = QPushButton("💰 Generate Payroll")
        generate_btn.setObjectName("PrimaryButton")
        generate_btn.clicked.connect(self.generate_payroll)
        toolbar.addWidget(generate_btn)
        
        layout.addLayout(toolbar)
        
        # Payroll details table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Employee ID", "Name", "Month", "Year", "Gross Salary", "Deductions", "Net Salary"
        ])
        
        # Table styling
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Set column widths
        self.table.setColumnWidth(0, 120)  # Employee ID
        self.table.setColumnWidth(1, 150)  # Name
        self.table.setColumnWidth(2, 80)   # Month
        self.table.setColumnWidth(3, 80)   # Year
        self.table.setColumnWidth(4, 120)  # Gross Salary
        self.table.setColumnWidth(5, 120)  # Deductions
        
        layout.addWidget(self.table)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        payslip_btn = QPushButton("📄 Generate Payslip PDF")
        payslip_btn.setObjectName("PrimaryButton")
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
        
        reply = QMessageBox.question(
            self, "Generate Payroll",
            f"Generate payroll for {self.employee_combo.currentText()} for {month}/{year}?\nBonus: ₹{bonus:,.2f}",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
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
            
            # Get employee details
            employee = self.employee_service.get_employee(employee_id)
            
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem(payroll.employee_id))
            self.table.setItem(0, 1, QTableWidgetItem(employee.employee_name if employee else "N/A"))
            self.table.setItem(0, 2, QTableWidgetItem(str(payroll.month)))
            self.table.setItem(0, 3, QTableWidgetItem(str(payroll.year)))
            self.table.setItem(0, 4, QTableWidgetItem(f"₹{payroll.gross_salary:,.2f}"))
            self.table.setItem(0, 5, QTableWidgetItem(f"₹{payroll.total_deductions:,.2f}"))
            self.table.setItem(0, 6, QTableWidgetItem(f"₹{payroll.net_salary:,.2f}"))
            
            # Color code net salary
            net_item = self.table.item(0, 6)
            net_item.setForeground(Qt.green)
            
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
