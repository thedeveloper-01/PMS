"""
Attendance management widget
UI FIXED – no bleed, no ghost backgrounds, theme-safe
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QDateEdit, QComboBox, QMessageBox, QDialog,
    QFormLayout, QTimeEdit, QFrame
)
from PySide6.QtCore import Qt, QDate
from datetime import date
from payroll_system.services.attendance_service import AttendanceService
from payroll_system.services.employee_service import EmployeeService


class AttendanceManagementWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.attendance_service = AttendanceService()
        self.employee_service = EmployeeService()
        self.init_ui()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 24, 32, 24)
        root.setSpacing(20)

        # ---------- Toolbar Card ----------
        toolbar_card = QFrame()
        toolbar_card.setObjectName("Card")
        toolbar_card.setAttribute(Qt.WA_StyledBackground, True)

        toolbar_layout = QHBoxLayout(toolbar_card)
        toolbar_layout.setContentsMargins(16, 16, 16, 16)
        toolbar_layout.setSpacing(12)

        emp_label = QLabel("Employee")
        emp_label.setAttribute(Qt.WA_TranslucentBackground, True)

        self.employee_combo = QComboBox()
        self.employee_combo.setMinimumWidth(220)
        self.load_employees()

        date_label = QLabel("Date")
        date_label.setAttribute(Qt.WA_TranslucentBackground, True)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setMinimumWidth(160)

        toolbar_layout.addWidget(emp_label)
        toolbar_layout.addWidget(self.employee_combo)
        toolbar_layout.addWidget(date_label)
        toolbar_layout.addWidget(self.date_input)
        toolbar_layout.addStretch()

        view_btn = QPushButton("📊 View Attendance")
        view_btn.clicked.connect(self.view_attendance)

        mark_btn = QPushButton("✓ Mark Attendance")
        mark_btn.setObjectName("PrimaryButton")
        mark_btn.clicked.connect(self.mark_attendance)

        toolbar_layout.addWidget(view_btn)
        toolbar_layout.addWidget(mark_btn)

        root.addWidget(toolbar_card)

        # ---------- Table Card ----------
        table_card = QFrame()
        table_card.setObjectName("Card")
        table_card.setAttribute(Qt.WA_StyledBackground, True)

        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Date", "Check-in", "Check-out", "Status", "Action"]
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)

        table_layout.addWidget(self.table)
        root.addWidget(table_card)

    # ---------- Data ----------
    def load_employees(self):
        self.employee_combo.clear()
        self.employee_combo.addItem("Select Employee", None)

        for emp in self.employee_service.get_all_employees(status=1):
            self.employee_combo.addItem(
                f"{emp.employee_id} – {emp.employee_name}", emp.employee_id
            )

    def view_attendance(self):
        employee_id = self.employee_combo.currentData()
        if not employee_id:
            QMessageBox.warning(self, "Required", "Please select an employee.")
            return

        selected_date = self.date_input.date().toPython()
        month, year = selected_date.month, selected_date.year

        try:
            records = self.attendance_service.get_monthly_attendance(
                employee_id, month, year
            )

            self.table.setRowCount(len(records))

            for row, att in enumerate(records):
                self.table.setItem(row, 0, QTableWidgetItem(str(att.date)))
                self.table.setItem(row, 1, QTableWidgetItem(str(att.checkin_time or "—")))
                self.table.setItem(row, 2, QTableWidgetItem(str(att.checkout_time or "—")))
                self.table.setItem(row, 3, QTableWidgetItem(att.status))

                lop_btn = QPushButton("❌ Mark LOP")
                lop_btn.setObjectName("DangerButton")
                lop_btn.clicked.connect(
                    lambda _, d=att.date: self.mark_lop(employee_id, d)
                )
                self.table.setCellWidget(row, 4, lop_btn)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def mark_attendance(self):
        employee_id = self.employee_combo.currentData()
        if not employee_id:
            QMessageBox.warning(self, "Required", "Please select an employee.")
            return

        dialog = MarkAttendanceDialog(
            self, employee_id, self.date_input.date().toPython()
        )
        if dialog.exec() == QDialog.Accepted:
            self.view_attendance()

    def mark_lop(self, employee_id: str, att_date: date):
        if self.attendance_service.mark_lop(employee_id, att_date):
            QMessageBox.information(self, "Success", "LOP marked successfully.")
            self.view_attendance()
        else:
            QMessageBox.critical(self, "Failed", "Unable to mark LOP.")


# ===================================================================

class MarkAttendanceDialog(QDialog):

    def __init__(self, parent, employee_id: str, att_date: date):
        super().__init__(parent)
        self.employee_id = employee_id
        self.att_date = att_date
        self.attendance_service = AttendanceService()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("✓ Mark Attendance")
        self.setMinimumWidth(360)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)

        self.checkin = QTimeEdit()
        self.checkout = QTimeEdit()

        form.addRow("Check-in Time", self.checkin)
        form.addRow("Check-out Time", self.checkout)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btns.addStretch()

        save = QPushButton("💾 Save")
        save.setObjectName("PrimaryButton")
        save.clicked.connect(self.save)

        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)

        btns.addWidget(save)
        btns.addWidget(cancel)

        layout.addLayout(btns)

    def save(self):
        success = self.attendance_service.mark_attendance(
            self.employee_id,
            self.att_date,
            self.checkin.time().toPython(),
            self.checkout.time().toPython(),
        )
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to save attendance.")
