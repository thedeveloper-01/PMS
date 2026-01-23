
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
        header.setObjectName("PageTitle")
        layout.addWidget(header)
        
        # Filter Layout (Row 1)
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        
        # Employee filter
        filter_layout.addWidget(QLabel("Employee:"))
        self.employee_combo = QComboBox()
        self.load_employees()
        self.employee_combo.setMinimumWidth(250)
        filter_layout.addWidget(self.employee_combo, 1) # Give it stretch factor
        
        # Month filter
        filter_layout.addWidget(QLabel("Month:"))
        self.month_combo = QComboBox()
        import calendar
        # distinct month names (skip index 0)
        self.month_names = list(calendar.month_name)[1:]
        self.month_combo.addItems(self.month_names)
        # Set current month
        self.month_combo.setCurrentIndex(datetime.now().month - 1)
        self.month_combo.setFixedWidth(120)
        filter_layout.addWidget(self.month_combo)
        
        # Year filter
        filter_layout.addWidget(QLabel("Year:"))
        self.year_spin = QSpinBox()
        self.year_spin.setMinimum(2020)
        self.year_spin.setMaximum(2100)
        self.year_spin.setValue(datetime.now().year)
        self.year_spin.setFixedWidth(80)
        filter_layout.addWidget(self.year_spin)
        
        layout.addLayout(filter_layout)

        # Actions Layout (Row 2)
        action_row = QHBoxLayout()
        action_row.setSpacing(15)

        # Bonus input
        action_row.addWidget(QLabel("Bonus:"))
        self.bonus_spin = QDoubleSpinBox()
        self.bonus_spin.setMaximum(999999)
        self.bonus_spin.setValue(0)
        self.bonus_spin.setPrefix("₹ ")
        self.bonus_spin.setFixedWidth(120)
        action_row.addWidget(self.bonus_spin)
        
        action_row.addStretch()
        
        # Action buttons
        view_btn = QPushButton("📊 View Payroll")
        view_btn.clicked.connect(self.view_payroll)
        action_row.addWidget(view_btn)
        
        export_btn = QPushButton("📥 Export Excel")
        export_btn.clicked.connect(self.export_payroll)
        action_row.addWidget(export_btn)
        
        generate_btn = QPushButton("💰 Generate Payroll")
        generate_btn.setObjectName("PrimaryButton")
        generate_btn.clicked.connect(self.generate_payroll)
        action_row.addWidget(generate_btn)
        
        layout.addLayout(action_row)
        
        # Payroll details table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Employee ID", "Name", "Month", "Year", "Gross Salary", "Deductions", "Net Salary", "Actions"
        ])
        
        # Table styling
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(70)  # Increase row height to 70px
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Set column widths
        self.table.setColumnWidth(0, 100)  # Employee ID
        self.table.setColumnWidth(1, 150)  # Name
        self.table.setColumnWidth(2, 80)   # Month
        self.table.setColumnWidth(3, 80)   # Year
        self.table.setColumnWidth(4, 120)  # Gross Salary
        self.table.setColumnWidth(5, 120)  # Deductions
        
        # Action column fixed width
        # self.table.setColumnWidth(7, 180) 
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.Fixed)
        self.table.setColumnWidth(7, 80)
        
        layout.addWidget(self.table)
        
        # Bottom Buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        payslip_btn = QPushButton("📄 Generate Payslip PDF")
        payslip_btn.setObjectName("PrimaryButton")
        payslip_btn.clicked.connect(self.generate_payslip)
        bottom_layout.addWidget(payslip_btn)
        
        layout.addLayout(bottom_layout)
        
        self.setLayout(layout)
    
    def load_employees(self):
        """Load employees"""
        current_id = self.employee_combo.currentData()
        employees = self.employee_service.get_all_employees(status=1)
        self.employee_combo.clear()
        self.employee_combo.addItem("Select Employee", None)
        
        index_to_set = 0
        for i, emp in enumerate(employees):
            self.employee_combo.addItem(f"{emp.employee_id} - {emp.employee_name}", emp.employee_id)
            if current_id and emp.employee_id == current_id:
                index_to_set = i + 1
        
        if index_to_set > 0:
            self.employee_combo.setCurrentIndex(index_to_set)
    
    def generate_payroll(self):
        """Generate payroll"""
        employee_id = self.employee_combo.currentData()
        if not employee_id:
            QMessageBox.warning(self, "Warning", "Please select an employee")
            return
        
        month = self.month_combo.currentIndex() + 1
        year = self.year_spin.value()
        bonus = self.bonus_spin.value()
        
        month_name = self.month_combo.currentText()
        
        reply = QMessageBox.question(
            self, "Generate Payroll",
            f"Generate payroll for {self.employee_combo.currentText()} for {month_name} {year}?\nBonus: ₹{bonus:,.2f}",
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
        
        month = self.month_combo.currentIndex() + 1
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

            # Action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(6)
            actions_layout.setAlignment(Qt.AlignCenter)
            
            # Delete button
            delete_btn = QPushButton("Del")
            delete_btn.setToolTip("Delete Record")
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(239, 68, 68, 0.2); 
                    color: #ef4444;
                    border: 1px solid rgba(239, 68, 68, 0.5);
                    border-radius: 4px;
                    padding: 0px;
                    font-weight: 600;
                    font-size: 11px;
                    min-height: 24px;
                    max-width: 40px;
                    width: 40px;
                }
                QPushButton:hover {
                    background-color: rgba(239, 68, 68, 0.8);
                    color: white;
                }
            """)
            delete_btn.clicked.connect(lambda checked: self.delete_payroll())
            
            actions_layout.addWidget(delete_btn)
            
            self.table.setCellWidget(0, 7, actions_widget)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading payroll: {str(e)}")

    def delete_payroll(self):
        """Delete current payroll record"""
        employee_id = self.employee_combo.currentData()
        if not employee_id:
            return
            
        month = self.month_combo.currentIndex() + 1
        year = self.year_spin.value()
        month_name = self.month_combo.currentText()
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete the payroll record for {month_name} {year}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                success = self.payroll_service.delete_payroll(employee_id, month, year)
                if success:
                    QMessageBox.information(self, "Success", "Payroll record deleted successfully")
                    self.view_payroll() # Refresh view (should be empty now)
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete payroll record")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error deleting record: {str(e)}")
    
    def generate_payslip(self):
        """Generate payslip PDF"""
        employee_id = self.employee_combo.currentData()
        if not employee_id:
            QMessageBox.warning(self, "Warning", "Please select an employee")
            return
        
        month = self.month_combo.currentIndex() + 1
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
        month = self.month_combo.currentIndex() + 1
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

    def refresh_data(self):
        """Refresh data when tab is active"""
        self.load_employees()
