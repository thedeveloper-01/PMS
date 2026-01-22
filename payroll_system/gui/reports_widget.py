"""
Reports widget
UI FIXED: no background bleed, proper card, theme-consistent
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from payroll_system.services.employee_service import EmployeeService
from payroll_system.reports.excel_export import ExcelExporter


class ReportsWidget(QWidget):
    """Reports widget"""

    def __init__(self):
        super().__init__()
        self.employee_service = EmployeeService()
        self.excel_exporter = ExcelExporter()
        self.init_ui()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(24)
        root.setContentsMargins(32, 24, 32, 24)

        # ---------- Card ----------
        reports_card = QWidget()
        reports_card.setObjectName("Card")
        reports_card.setAttribute(Qt.WA_StyledBackground, True)

        card_layout = QVBoxLayout(reports_card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)

        # ---------- Title ----------
        section_title = QLabel("Export Reports")
        section_title.setObjectName("SectionTitle")
        section_title.setAttribute(Qt.WA_TranslucentBackground, True)

        card_layout.addWidget(section_title)

        # ---------- Button ----------
        employee_list_btn = QPushButton("📊 Export Employee List to Excel")
        employee_list_btn.setObjectName("PrimaryButton")
        employee_list_btn.setMinimumHeight(48)
        employee_list_btn.clicked.connect(self.export_employee_list)

        card_layout.addWidget(employee_list_btn)

        root.addWidget(reports_card)
        root.addStretch()

    def export_employee_list(self):
        """Export employee list to Excel"""
        try:
            employees = self.employee_service.get_all_employees(status=1)

            if not employees:
                QMessageBox.warning(self, "Warning", "No employees found")
                return

            filepath = self.excel_exporter.export_employee_list(employees)
            QMessageBox.information(
                self,
                "Success",
                f"Employee list exported to:\n{filepath}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
