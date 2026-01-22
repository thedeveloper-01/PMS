"""
Employee Management Widget
UI FIXED – no bleed, no ghost backgrounds, theme-safe
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from payroll_system.services.employee_service import EmployeeService


class EmployeeManagementWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.employee_service = EmployeeService()
        self.init_ui()
        self.load_employees()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 24, 32, 24)
        root.setSpacing(24)

        # ---------- Header ----------
        header = QLabel("Employee Management")
        header.setObjectName("PageTitle")
        header.setAttribute(Qt.WA_TranslucentBackground, True)
        root.addWidget(header)

        # ---------- Toolbar Card ----------
        toolbar = QFrame()
        toolbar.setObjectName("Card")
        toolbar.setAttribute(Qt.WA_StyledBackground, True)

        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(16, 16, 16, 16)
        toolbar_layout.setSpacing(12)

        add_btn = QPushButton("➕ Add Employee")
        add_btn.setObjectName("PrimaryButton")
        add_btn.clicked.connect(self.add_employee)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_employees)

        toolbar_layout.addWidget(add_btn)
        toolbar_layout.addWidget(refresh_btn)
        toolbar_layout.addStretch()

        root.addWidget(toolbar)

        # ---------- Table Card ----------
        table_card = QFrame()
        table_card.setObjectName("Card")
        table_card.setAttribute(Qt.WA_StyledBackground, True)

        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Employee ID",
            "Name",
            "Department",
            "Designation",
            "Status",
            "Action"
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)

        table_layout.addWidget(self.table)
        root.addWidget(table_card)

    # ===============================================================

    def load_employees(self):
        try:
            employees = self.employee_service.get_all_employees(status=1)
            self.table.setRowCount(len(employees))

            for row, emp in enumerate(employees):
                self.table.setItem(row, 0, QTableWidgetItem(str(emp.employee_id)))
                self.table.setItem(row, 1, QTableWidgetItem(emp.employee_name))
                self.table.setItem(row, 2, QTableWidgetItem(emp.department))
                self.table.setItem(row, 3, QTableWidgetItem(emp.designation))
                self.table.setItem(row, 4, QTableWidgetItem("Active"))

                delete_btn = QPushButton("🗑 Delete")
                delete_btn.setObjectName("DangerButton")
                delete_btn.clicked.connect(
                    lambda _, eid=emp.employee_id: self.delete_employee(eid)
                )

                self.table.setCellWidget(row, 5, delete_btn)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def add_employee(self):
        QMessageBox.information(
            self,
            "Not Implemented",
            "Employee creation form will be added here."
        )

    def delete_employee(self, employee_id):
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this employee?"
        )

        if confirm != QMessageBox.Yes:
            return

        try:
            self.employee_service.delete_employee(employee_id)
            self.load_employees()
            QMessageBox.information(self, "Deleted", "Employee deleted successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
