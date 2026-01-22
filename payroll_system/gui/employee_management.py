
"""
Employee management widget
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox, QDialog, QFormLayout,
    QComboBox, QDateEdit, QDoubleSpinBox, QHeaderView,
    QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor
from payroll_system.services.employee_service import EmployeeService
from payroll_system.repository.master_data_repository import MasterDataRepository
from payroll_system.models.employee import Employee
from payroll_system.config import ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE
import re

class EmployeeManagementWidget(QWidget):
    """Employee management widget"""

    def __init__(self):
        super().__init__()
        self.employee_service = EmployeeService()
        self.master_repo = MasterDataRepository()
        self.init_ui()
        self.load_employees()

    def refresh_data(self):
        """Refresh data when tab is active"""
        self.load_employees()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 25, 30, 25)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Employee Directory")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #ffffff;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Search bar
        search_frame = QFrame()
        search_frame.setStyleSheet("""
            QFrame {
                background: #0f172a;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
            }
        """)
        search_frame.setFixedHeight(50)
        
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(15, 0, 15, 0)
        
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("font-size: 16px; color: #cbd5e1;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, email, or ID...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: #ffffff;
                font-size: 14px;
                padding: 8px;
            }
            QLineEdit::placeholder {
                color: #a0aec0;
            }
        """)
        self.search_input.textChanged.connect(self.search_employees)
        
        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input)
        search_layout.addStretch()
        
        layout.addWidget(search_frame)
        
        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)
        
        toolbar.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("SecondaryButton")
        refresh_btn.clicked.connect(self.load_employees)
        toolbar.addWidget(refresh_btn)
        
        add_btn = QPushButton("➕ Add Employee")
        add_btn.setObjectName("PrimaryButton")
        add_btn.clicked.connect(self.add_employee)
        toolbar.addWidget(add_btn)
        
        layout.addLayout(toolbar)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Employee ID", "Name", "Email", "Mobile",
            "Department", "Designation", "Role", "Basic Salary", "Actions"
        ])
        
        # Table styling
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(70)  # Increase row height to 70px
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        # Header styling
        header = self.table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignLeft)
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #2d3748;
                color: #a0aec0;
                padding: 12px 15px;
                border: none;
                font-weight: 600;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        """)
        
        # Set column widths
        self.table.setColumnWidth(0, 120)  # Employee ID
        self.table.setColumnWidth(1, 180)  # Name
        self.table.setColumnWidth(2, 200)  # Email
        self.table.setColumnWidth(3, 130)  # Mobile
        self.table.setColumnWidth(4, 130)  # Department
        self.table.setColumnWidth(5, 130)  # Designation
        self.table.setColumnWidth(6, 100)  # Role
        self.table.setColumnWidth(7, 120)  # Basic Salary
        self.table.setColumnWidth(8, 220)  # Actions
        
        layout.addWidget(self.table, 1)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #a0aec0; font-size: 12px;")
        layout.addWidget(self.status_label)

    def load_employees(self):
        try:
            employees = self.employee_service.get_all_employees(status=1)
            self.table.setRowCount(len(employees))
            
            for row, employee in enumerate(employees):
                # Employee ID
                id_item = QTableWidgetItem(employee.employee_id)
                id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 0, id_item)
                
                # Name
                name_item = QTableWidgetItem(employee.employee_name)
                name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 1, name_item)
                
                # Email
                email_item = QTableWidgetItem(employee.email)
                email_item.setFlags(email_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 2, email_item)
                
                # Mobile
                mobile_item = QTableWidgetItem(str(employee.mobile_number))
                mobile_item.setFlags(mobile_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 3, mobile_item)
                
                # Get department and designation names
                dept_name = "N/A"
                desig_name = "N/A"
                if employee.department_id:
                    dept = self.master_repo.get_department(employee.department_id)
                    dept_name = dept.department_name if dept else "N/A"
                if employee.designation_id:
                    desig = self.master_repo.get_designation(employee.designation_id)
                    desig_name = desig.designation_name if desig else "N/A"
                
                # Department
                dept_item = QTableWidgetItem(dept_name)
                dept_item.setFlags(dept_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 4, dept_item)
                
                # Designation
                desig_item = QTableWidgetItem(desig_name)
                desig_item.setFlags(desig_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 5, desig_item)
                
                # Role
                role_text = "Employee"
                if employee.role == ROLE_HR:
                    role_text = "HR"
                elif employee.role == ROLE_ADMIN:
                    role_text = "Admin"
                role_item = QTableWidgetItem(role_text)
                role_item.setFlags(role_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 6, role_item)
                
                # Basic Salary
                salary_item = QTableWidgetItem(f"₹{employee.basic_salary:,.2f}")
                salary_item.setFlags(salary_item.flags() & ~Qt.ItemIsEditable)
                salary_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row, 7, salary_item)
                
                # Actions
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(5, 0, 5, 0)
                actions_layout.setSpacing(12)
                actions_layout.setAlignment(Qt.AlignCenter)
                
                # Edit button
                edit_btn = QPushButton("Edit")
                edit_btn.setFixedSize(75, 32)
                edit_btn.setCursor(Qt.PointingHandCursor)
                edit_btn.setObjectName("InfoButton")
                edit_btn.clicked.connect(lambda _, e=employee: self.edit_employee(e))
                
                # Delete button
                delete_btn = QPushButton("Delete")
                delete_btn.setFixedSize(75, 32)
                delete_btn.setCursor(Qt.PointingHandCursor)
                delete_btn.setObjectName("DangerButton")
                delete_btn.clicked.connect(lambda _, e=employee: self.delete_employee(e))
                
                actions_layout.addWidget(edit_btn)
                actions_layout.addWidget(delete_btn)
                
                self.table.setCellWidget(row, 8, actions_widget)
            
            # Update status
            self.status_label.setText(f"Showing {len(employees)} employees")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def search_employees(self):
        term = self.search_input.text().strip()
        if not term:
            self.load_employees()
            return

        try:
            employees = self.employee_service.search_employees(term)
            self.table.setRowCount(len(employees))

            for row, employee in enumerate(employees):
                self.table.setItem(row, 0, QTableWidgetItem(employee.employee_id))
                self.table.setItem(row, 1, QTableWidgetItem(employee.employee_name))
                self.table.setItem(row, 2, QTableWidgetItem(employee.email))
                self.table.setItem(row, 3, QTableWidgetItem(str(employee.mobile_number)))
                
                # Get department and designation names
                dept_name = "N/A"
                desig_name = "N/A"
                if employee.department_id:
                    dept = self.master_repo.get_department(employee.department_id)
                    dept_name = dept.department_name if dept else "N/A"
                if employee.designation_id:
                    desig = self.master_repo.get_designation(employee.designation_id)
                    desig_name = desig.designation_name if desig else "N/A"
                
                self.table.setItem(row, 4, QTableWidgetItem(dept_name))
                self.table.setItem(row, 5, QTableWidgetItem(desig_name))
                
                # Role
                role_text = "Employee"
                if employee.role == ROLE_HR:
                    role_text = "HR"
                elif employee.role == ROLE_ADMIN:
                    role_text = "Admin"
                self.table.setItem(row, 6, QTableWidgetItem(role_text))
                
                self.table.setItem(row, 7, QTableWidgetItem(f"₹{employee.basic_salary:,.2f}"))

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def add_employee(self):
        dialog = EmployeeDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.load_employees()

    def edit_employee(self, employee: Employee):
        dialog = EmployeeDialog(self, employee)
        if dialog.exec() == QDialog.Accepted:
            self.load_employees()

    def delete_employee(self, employee: Employee):
        reply = QMessageBox.question(
            self, "Delete Employee",
            f"Are you sure you want to delete {employee.employee_name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            success, msg = self.employee_service.delete_employee(employee.employee_id)
            if success:
                QMessageBox.information(self, "Success", f"Employee {employee.employee_name} deleted")
                self.load_employees()
            else:
                QMessageBox.critical(self, "Error", msg)

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
        self.setWindowTitle("Add Employee" if not self.employee else "Edit Employee")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setSpacing(10)

        self.employee_id_input = QLineEdit()
        if self.employee:
            self.employee_id_input.setEnabled(False)
        form.addRow("Employee ID:", self.employee_id_input)

        self.name_input = QLineEdit()
        form.addRow("Name:", self.name_input)

        self.email_input = QLineEdit()
        form.addRow("Email:", self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        if self.employee:
            self.password_input.setPlaceholderText("Leave empty to keep current password")
        form.addRow("Password:", self.password_input)

        self.mobile_input = QLineEdit()
        form.addRow("Mobile:", self.mobile_input)

        self.salary_input = QDoubleSpinBox()
        self.salary_input.setMaximum(9999999)
        self.salary_input.setPrefix("₹ ")
        form.addRow("Basic Salary:", self.salary_input)

        self.dept_combo = QComboBox()
        self.dept_combo.addItem("Select Department", None)
        for d in self.master_repo.get_all_departments():
            self.dept_combo.addItem(d.department_name, d.department_id)
        form.addRow("Department:", self.dept_combo)

        self.designation_combo = QComboBox()
        self.designation_combo.addItem("Select Designation", None)
        for d in self.master_repo.get_all_designations():
            self.designation_combo.addItem(d.designation_name, d.designation_id)
        form.addRow("Designation:", self.designation_combo)

        self.branch_combo = QComboBox()
        self.branch_combo.addItem("Select Branch", None)
        for b in self.master_repo.get_all_branches():
            self.branch_combo.addItem(b.name, b.branch_id)
        form.addRow("Branch:", self.branch_combo)

        self.role_combo = QComboBox()
        self.role_combo.addItem("Employee", ROLE_EMPLOYEE)
        self.role_combo.addItem("HR", ROLE_HR)
        self.role_combo.addItem("Admin", ROLE_ADMIN)
        form.addRow("Role:", self.role_combo)

        layout.addLayout(form)

        # Buttons
        buttons = QHBoxLayout()
        buttons.addStretch()

        save_btn = QPushButton("💾 Save")
        save_btn.setObjectName("PrimaryButton")
        save_btn.clicked.connect(self.save_employee)
        buttons.addWidget(save_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(cancel_btn)

        layout.addLayout(buttons)

    def load_employee_data(self):
        self.employee_id_input.setText(self.employee.employee_id)
        self.name_input.setText(self.employee.employee_name)
        self.email_input.setText(self.employee.email)
        self.mobile_input.setText(str(self.employee.mobile_number))
        self.salary_input.setValue(self.employee.basic_salary)

        self.dept_combo.setCurrentIndex(
            self.dept_combo.findData(self.employee.department_id)
        )
        self.designation_combo.setCurrentIndex(
            self.designation_combo.findData(self.employee.designation_id)
        )
        self.branch_combo.setCurrentIndex(
            self.branch_combo.findData(self.employee.branch_id)
        )
        self.role_combo.setCurrentIndex(
            self.role_combo.findData(self.employee.role)
        )

    def save_employee(self):
        data = {
            'employee_id': self.employee_id_input.text().strip(),
            'employee_name': self.name_input.text().strip(),
            'email': self.email_input.text().strip(),
            'password': self.password_input.text().strip() or (
                self.employee.password if self.employee else ''
            ),
            'mobile_number': self.mobile_input.text().strip(),
            'basic_salary': self.salary_input.value(),
            'department_id': self.dept_combo.currentData(),
            'designation_id': self.designation_combo.currentData(),
            'branch_id': self.branch_combo.currentData(),
            'role': self.role_combo.currentData(),
        }

        # Validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            QMessageBox.warning(self, "Validation Error", "Please enter a valid email address.")
            return

        if not re.match(r"^\d{10}$", data['mobile_number']):
            QMessageBox.warning(self, "Validation Error", "Mobile number must be exactly 10 digits.")
            return

        if not self.employee:
            success, msg = self.employee_service.create_employee(data)
        else:
            success, msg = self.employee_service.update_employee(
                self.employee.employee_id, data
            )

        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", msg)
