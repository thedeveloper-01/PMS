"""
Employee management widget
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QLineEdit, QMessageBox, QDialog, QFormLayout,
                              QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from payroll_system.services.employee_service import EmployeeService
from payroll_system.repository.master_data_repository import MasterDataRepository
from payroll_system.models.employee import Employee
from payroll_system.config import ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE
from datetime import datetime

class EmployeeManagementWidget(QWidget):
    """Employee management widget"""
    
    def __init__(self):
        super().__init__()
        self.employee_service = EmployeeService()
        self.master_repo = MasterDataRepository()
        self.init_ui()
        self.load_employees()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Employee Management")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Buttons
        add_btn = QPushButton("Add Employee")
        add_btn.clicked.connect(self.add_employee)
        header_layout.addWidget(add_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_employees)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, email, or ID...")
        self.search_input.textChanged.connect(self.search_employees)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Employee ID", "Name", "Email", "Mobile", 
            "Department", "Designation", "Basic Salary", "Actions"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_employees(self):
        """Load employees into table"""
        try:
            employees = self.employee_service.get_all_employees(status=1)
            self.table.setRowCount(len(employees))
            
            for row, employee in enumerate(employees):
                self.table.setItem(row, 0, QTableWidgetItem(employee.employee_id))
                self.table.setItem(row, 1, QTableWidgetItem(employee.employee_name))
                self.table.setItem(row, 2, QTableWidgetItem(employee.email))
                self.table.setItem(row, 3, QTableWidgetItem(str(employee.mobile_number)))
                self.table.setItem(row, 4, QTableWidgetItem(str(employee.department_id or "N/A")))
                self.table.setItem(row, 5, QTableWidgetItem(str(employee.designation_id or "N/A")))
                self.table.setItem(row, 6, QTableWidgetItem(f"₹{employee.basic_salary:.2f}"))
                
                # Actions
                actions_widget = QWidget()
                actions_layout = QHBoxLayout()
                actions_layout.setContentsMargins(5, 5, 5, 5)
                
                edit_btn = QPushButton("Edit")
                edit_btn.clicked.connect(lambda checked, e=employee: self.edit_employee(e))
                actions_layout.addWidget(edit_btn)
                
                delete_btn = QPushButton("Delete")
                delete_btn.setStyleSheet("background-color: #e74c3c; color: white;")
                delete_btn.clicked.connect(lambda checked, e=employee: self.delete_employee(e))
                actions_layout.addWidget(delete_btn)
                
                actions_widget.setLayout(actions_layout)
                self.table.setCellWidget(row, 7, actions_widget)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading employees: {str(e)}")
    
    def search_employees(self):
        """Search employees"""
        search_term = self.search_input.text().strip()
        if not search_term:
            self.load_employees()
            return
        
        try:
            employees = self.employee_service.search_employees(search_term)
            self.table.setRowCount(len(employees))
            
            for row, employee in enumerate(employees):
                self.table.setItem(row, 0, QTableWidgetItem(employee.employee_id))
                self.table.setItem(row, 1, QTableWidgetItem(employee.employee_name))
                self.table.setItem(row, 2, QTableWidgetItem(employee.email))
                self.table.setItem(row, 3, QTableWidgetItem(str(employee.mobile_number)))
                self.table.setItem(row, 4, QTableWidgetItem(str(employee.department_id or "N/A")))
                self.table.setItem(row, 5, QTableWidgetItem(str(employee.designation_id or "N/A")))
                self.table.setItem(row, 6, QTableWidgetItem(f"₹{employee.basic_salary:.2f}"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error searching: {str(e)}")
    
    def add_employee(self):
        """Open add employee dialog"""
        dialog = EmployeeDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.load_employees()
    
    def edit_employee(self, employee: Employee):
        """Open edit employee dialog"""
        dialog = EmployeeDialog(self, employee)
        if dialog.exec() == QDialog.Accepted:
            self.load_employees()
    
    def delete_employee(self, employee: Employee):
        """Delete employee"""
        reply = QMessageBox.question(
            self, "Delete Employee",
            f"Are you sure you want to delete {employee.employee_name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.employee_service.delete_employee(employee.employee_id)
            if success:
                QMessageBox.information(self, "Success", message)
                self.load_employees()
            else:
                QMessageBox.critical(self, "Error", message)

class EmployeeDialog(QDialog):
    """Employee add/edit dialog"""
    
    def __init__(self, parent, employee: Employee = None):
        super().__init__(parent)
        self.employee = employee
        self.employee_service = EmployeeService()
        self.master_repo = MasterDataRepository()
        self.init_ui()
        
        if employee:
            self.load_employee_data()
    
    def init_ui(self):
        """Initialize dialog UI"""
        self.setWindowTitle("Add Employee" if not self.employee else "Edit Employee")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        form = QFormLayout()
        
        # Employee ID
        self.employee_id_input = QLineEdit()
        if self.employee:
            self.employee_id_input.setEnabled(False)
        form.addRow("Employee ID:", self.employee_id_input)
        
        # Name
        self.name_input = QLineEdit()
        form.addRow("Name:", self.name_input)
        
        # Email
        self.email_input = QLineEdit()
        form.addRow("Email:", self.email_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form.addRow("Password:", self.password_input)
        
        # Mobile
        self.mobile_input = QLineEdit()
        form.addRow("Mobile:", self.mobile_input)
        
        # Gender
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female"])
        form.addRow("Gender:", self.gender_combo)
        
        # DOB
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate.currentDate().addYears(-25))
        form.addRow("Date of Birth:", self.dob_input)
        
        # Basic Salary
        self.salary_input = QDoubleSpinBox()
        self.salary_input.setMaximum(9999999)
        self.salary_input.setValue(0)
        form.addRow("Basic Salary:", self.salary_input)
        
        # Department
        self.dept_combo = QComboBox()
        departments = self.master_repo.get_all_departments()
        self.dept_combo.addItem("Select Department", None)
        for dept in departments:
            self.dept_combo.addItem(dept.department_name, dept.department_id)
        form.addRow("Department:", self.dept_combo)
        
        # Designation
        self.designation_combo = QComboBox()
        designations = self.master_repo.get_all_designations()
        self.designation_combo.addItem("Select Designation", None)
        for des in designations:
            self.designation_combo.addItem(des.designation_name, des.designation_id)
        form.addRow("Designation:", self.designation_combo)
        
        # Branch
        self.branch_combo = QComboBox()
        branches = self.master_repo.get_all_branches()
        self.branch_combo.addItem("Select Branch", None)
        for branch in branches:
            self.branch_combo.addItem(branch.name, branch.branch_id)
        form.addRow("Branch:", self.branch_combo)
        
        # Shift
        self.shift_combo = QComboBox()
        shifts = self.master_repo.get_all_shifts()
        self.shift_combo.addItem("Select Shift", None)
        for shift in shifts:
            self.shift_combo.addItem(shift.shift_name, shift.shift_id)
        form.addRow("Shift:", self.shift_combo)
        
        # Role
        self.role_combo = QComboBox()
        self.role_combo.addItem("Employee", ROLE_EMPLOYEE)
        self.role_combo.addItem("HR", ROLE_HR)
        self.role_combo.addItem("Admin", ROLE_ADMIN)
        form.addRow("Role:", self.role_combo)
        
        layout.addLayout(form)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_employee)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_employee_data(self):
        """Load employee data into form"""
        if not self.employee:
            return
        
        self.employee_id_input.setText(self.employee.employee_id)
        self.name_input.setText(self.employee.employee_name)
        self.email_input.setText(self.employee.email)
        self.mobile_input.setText(str(self.employee.mobile_number))
        self.gender_combo.setCurrentText(self.employee.gender)
        if self.employee.dob:
            self.dob_input.setDate(QDate.fromString(self.employee.dob.isoformat(), "yyyy-MM-dd"))
        self.salary_input.setValue(self.employee.basic_salary)
        
        # Set combo boxes
        index = self.dept_combo.findData(self.employee.department_id)
        if index >= 0:
            self.dept_combo.setCurrentIndex(index)
        
        index = self.designation_combo.findData(self.employee.designation_id)
        if index >= 0:
            self.designation_combo.setCurrentIndex(index)
        
        index = self.branch_combo.findData(self.employee.branch_id)
        if index >= 0:
            self.branch_combo.setCurrentIndex(index)
        
        index = self.shift_combo.findData(self.employee.shift_id)
        if index >= 0:
            self.shift_combo.setCurrentIndex(index)
        
        index = self.role_combo.findData(self.employee.role)
        if index >= 0:
            self.role_combo.setCurrentIndex(index)
    
    def save_employee(self):
        """Save employee"""
        try:
            employee_data = {
                'employee_id': self.employee_id_input.text().strip(),
                'employee_name': self.name_input.text().strip(),
                'email': self.email_input.text().strip(),
                'password': self.password_input.text().strip() or (self.employee.password if self.employee else ''),
                'mobile_number': self.mobile_input.text().strip(),
                'gender': self.gender_combo.currentText(),
                'dob': self.dob_input.date().toPython(),
                'basic_salary': self.salary_input.value(),
                'department_id': self.dept_combo.currentData(),
                'designation_id': self.designation_combo.currentData(),
                'branch_id': self.branch_combo.currentData(),
                'shift_id': self.shift_combo.currentData(),
                'role': self.role_combo.currentData(),
            }
            
            if not self.employee:
                # Create new
                success, message = self.employee_service.create_employee(employee_data)
            else:
                # Update existing
                success, message = self.employee_service.update_employee(
                    self.employee.employee_id, employee_data
                )
            
            if success:
                QMessageBox.information(self, "Success", message)
                self.accept()
            else:
                QMessageBox.critical(self, "Error", message)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving employee: {str(e)}")

