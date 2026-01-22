"""
Payroll Management Widget
UI FIXED – no bleed, no ghost backgrounds, theme-safe
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QComboBox, QFrame
)
from PySide6.QtCore import Qt
from payroll_system.services.payroll_service import PayrollService
from payroll_system.services.employee_service import EmployeeService


class PayrollManagementWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.payroll_service = PayrollService()
        self.employee_service = EmployeeService()
        self.init_ui()
        self.load_employees()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 24, 32, 24)
        root.setSpacing(24)

        # ---------- Header ----------
        header = QLabel("Payroll Management")
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

        emp_label = QLabel("Employee")
        emp_label.setAttribute(Qt.WA_TranslucentBackground, True)

        self.employee_combo = QComboBox()
        self.employee_combo.setMinimumWidth(240)

        generate_btn = QPushButton("💰 Generate Payroll")
        generate_btn.setObjectName("PrimaryButton")
        generate_btn.clicked.connect(self.generate_payroll)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_table)

        toolbar_layout.addWidget(emp_label)
        toolbar_layout.addWidget(self.employee_combo)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(refresh_btn)
        toolbar_layout.addWidget(generate_btn)

        root.addWidget(toolbar)

        # ---------- Table Card ----------
        table_card = QFrame()
        table_card.setObjectName("Card")
        table_card.setAttribute(Qt.WA_StyledBackground, True)

        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Employee",
            "Month",
            "Gross",
            "PF",
            "ESI",
            "Net Salary",
            "Status"
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)

        table_layout.addWidget(self.table)
        root.addWidget(table_card)

    # ===============================================================

    def load_employees(self):
        self.employee_combo.clear()
        self.employee_combo.addItem("Select Employee", None)

        for emp in self.employee_service.get_all_employees(status=1):
            self.employee_combo.addItem(
                f"{emp.employee_id} – {emp.employee_name}",
                emp.employee_id
            )

    def generate_payroll(self):
        employee_id = self.employee_combo.currentData()

        if not employee_id:
            QMessageBox.warning(
                self,
                "Required",
                "Please select an employee."
            )
            return

        try:
            payroll = self.payroll_service.generate_payroll(employee_id)

            QMessageBox.information(
                self,
                "Success",
                f"Payroll generated successfully.\nNet Salary: ₹{payroll.net_salary}"
            )

            self.refresh_table()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def refresh_table(self):
        try:
            payrolls = self.payroll_service.get_all_payrolls()
            self.table.setRowCount(len(payrolls))

            for row, p in enumerate(payrolls):
                self.table.setItem(row, 0, QTableWidgetItem(p.employee_name))
                self.table.setItem(row, 1, QTableWidgetItem(p.month))
                self.table.setItem(row, 2, QTableWidgetItem(f"₹{p.gross}"))
                self.table.setItem(row, 3, QTableWidgetItem(f"₹{p.pf}"))
                self.table.setItem(row, 4, QTableWidgetItem(f"₹{p.esi}"))
                self.table.setItem(row, 5, QTableWidgetItem(f"₹{p.net_salary}"))
                self.table.setItem(row, 6, QTableWidgetItem("Generated"))

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
