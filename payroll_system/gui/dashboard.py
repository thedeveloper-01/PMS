"""
Dashboard Widget
UI FIXED – clean cards, no bleed, theme-safe
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QGridLayout, QFrame, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt
from payroll_system.models.employee import Employee
from payroll_system.repository.employee_repository import EmployeeRepository
from payroll_system.repository.master_data_repository import MasterDataRepository


class DashboardWidget(QWidget):

    def __init__(self, employee: Employee):
        super().__init__()
        self.employee = employee
        self.employee_repo = EmployeeRepository()
        self.master_repo = MasterDataRepository()
        self.init_ui()
        self.load_statistics()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        content.setAttribute(Qt.WA_TranslucentBackground, True)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)

        # ---------- Header Card ----------
        header = QFrame()
        header.setObjectName("Card")
        header.setAttribute(Qt.WA_StyledBackground, True)

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 16, 20, 16)
        header_layout.setSpacing(4)

        title = QLabel("Dashboard Overview")
        title.setObjectName("PageTitle")
        title.setAttribute(Qt.WA_TranslucentBackground, True)

        subtitle = QLabel("Company-wide statistics and system overview")
        subtitle.setObjectName("PageSubtitle")
        subtitle.setAttribute(Qt.WA_TranslucentBackground, True)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        layout.addWidget(header)

        # ---------- Statistics Grid ----------
        grid = QGridLayout()
        grid.setSpacing(20)

        self.employee_card = self.create_stat_card("👥 Total Employees", "0")
        self.department_card = self.create_stat_card("🏢 Departments", "0")
        self.designation_card = self.create_stat_card("🎓 Designations", "0")
        self.branch_card = self.create_stat_card("🏬 Branches", "0")
        self.shift_card = self.create_stat_card("⏰ Active Shifts", "0")
        self.holiday_card = self.create_stat_card("🎉 Upcoming Holidays", "0")

        grid.addWidget(self.employee_card, 0, 0)
        grid.addWidget(self.department_card, 0, 1)
        grid.addWidget(self.designation_card, 0, 2)
        grid.addWidget(self.branch_card, 1, 0)
        grid.addWidget(self.shift_card, 1, 1)
        grid.addWidget(self.holiday_card, 1, 2)

        layout.addLayout(grid)
        layout.addStretch()

        scroll.setWidget(content)
        root.addWidget(scroll)

    # ===============================================================

    def create_stat_card(self, title_text: str, value_text: str) -> QFrame:
        card = QFrame()
        card.setObjectName("StatCard")
        card.setAttribute(Qt.WA_StyledBackground, True)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        card.setMinimumHeight(130)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel(title_text)
        title.setObjectName("CardTitle")
        title.setAttribute(Qt.WA_TranslucentBackground, True)

        value = QLabel(value_text)
        value.setObjectName("CardValue")
        value.setAlignment(Qt.AlignLeft)
        value.setAttribute(Qt.WA_TranslucentBackground, True)

        layout.addWidget(title)
        layout.addWidget(value)

        return card

    # ===============================================================

    def load_statistics(self):
        try:
            employees = self.employee_repo.get_all(status=1)
            departments = self.master_repo.get_all_departments()
            designations = self.master_repo.get_all_designations()
            branches = self.master_repo.get_all_branches()
            shifts = self.master_repo.get_all_shifts()
            holidays = self.master_repo.get_all_holidays()

            self.update_card(self.employee_card, len(employees))
            self.update_card(self.department_card, len(departments))
            self.update_card(self.designation_card, len(designations))
            self.update_card(self.branch_card, len(branches))
            self.update_card(self.shift_card, len(shifts))
            self.update_card(self.holiday_card, len(holidays))

        except Exception as e:
            print(f"Dashboard load error: {e}")

    def update_card(self, card: QFrame, value: int):
        layout = card.layout()
        value_label = layout.itemAt(1).widget()
        value_label.setText(str(value))
