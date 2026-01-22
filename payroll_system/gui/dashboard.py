"""
Dashboard widget showing statistics and overview
"""
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QFrame,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from payroll_system.models.employee import Employee
from payroll_system.repository.employee_repository import EmployeeRepository
from payroll_system.repository.master_data_repository import MasterDataRepository
from datetime import datetime

class DashboardWidget(QWidget):
    """Dashboard widget"""
    
    def __init__(self, employee: Employee):
        super().__init__()
        self.employee = employee
        self.employee_repo = EmployeeRepository()
        self.master_repo = MasterDataRepository()
        self.init_ui()
        self.load_statistics()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        # Page header (matches screenshot style)
        header = QFrame()
        header.setObjectName("Surface")
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 8)
        header_layout.setSpacing(4)

        title = QLabel("Dashboard Overview")
        title.setObjectName("PageTitle")
        subtitle = QLabel("Key metrics and quick actions.")
        subtitle.setObjectName("PageSubtitle")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header.setLayout(header_layout)
        layout.addWidget(header)

        # KPI cards row (3 across like screenshot)
        kpi_grid = QGridLayout()
        kpi_grid.setHorizontalSpacing(16)
        kpi_grid.setVerticalSpacing(16)

        self.kpi_employees = self._kpi_card("Total Employees", "0", "↑ +0%")
        self.kpi_payroll_cost = self._kpi_card("Monthly Payroll Cost", "$0", "vs last month")
        self.kpi_next_holiday = self._kpi_card("Next Holiday", "—", "0 days left")

        kpi_grid.addWidget(self.kpi_employees, 0, 0)
        kpi_grid.addWidget(self.kpi_payroll_cost, 0, 1)
        kpi_grid.addWidget(self.kpi_next_holiday, 0, 2)

        layout.addLayout(kpi_grid)

        # Charts + table area (placeholders to match layout)
        mid_grid = QGridLayout()
        mid_grid.setHorizontalSpacing(16)
        mid_grid.setVerticalSpacing(16)

        self.chart_left = self._panel(
            "Departmental Distribution",
            "Payroll allocation by department",
            body_text="(Chart placeholder – can be upgraded to QtCharts later)",
        )
        self.chart_right = self._panel(
            "Cost Trends",
            "Last 6 months expenditure",
            body_text="(Chart placeholder – can be upgraded to QtCharts later)",
        )

        mid_grid.addWidget(self.chart_left, 0, 0)
        mid_grid.addWidget(self.chart_right, 0, 1)

        layout.addLayout(mid_grid)

        bottom_grid = QGridLayout()
        bottom_grid.setHorizontalSpacing(16)
        bottom_grid.setVerticalSpacing(16)

        # Quick actions (left)
        actions = QFrame()
        actions.setObjectName("Card")
        actions_l = QVBoxLayout()
        actions_l.setContentsMargins(16, 16, 16, 16)
        actions_l.setSpacing(10)
        h = QLabel("Quick Actions")
        h.setStyleSheet("font-size: 16px; font-weight: 800;")
        actions_l.addWidget(h)
        btn_run = QPushButton("Run Payroll")
        btn_run.setObjectName("PrimaryButton")
        btn_add = QPushButton("Add Employee")
        btn_reports = QPushButton("Download Reports")
        actions_l.addWidget(btn_run)
        actions_l.addWidget(btn_add)
        actions_l.addWidget(btn_reports)
        actions_l.addStretch()
        actions.setLayout(actions_l)

        # Recent payroll runs (right)
        recent = QFrame()
        recent.setObjectName("Card")
        recent_l = QVBoxLayout()
        recent_l.setContentsMargins(16, 16, 16, 16)
        recent_l.setSpacing(10)
        head_row = QHBoxLayout()
        hh = QLabel("Recent Payroll Runs")
        hh.setStyleSheet("font-size: 16px; font-weight: 800;")
        head_row.addWidget(hh)
        head_row.addStretch()
        view_all = QPushButton("View All")
        head_row.addWidget(view_all)
        recent_l.addLayout(head_row)

        self.recent_table = QTableWidget()
        self.recent_table.setColumnCount(4)
        self.recent_table.setHorizontalHeaderLabels(["Batch ID", "Period", "Employees", "Status"])
        self.recent_table.setRowCount(2)
        self.recent_table.setItem(0, 0, QTableWidgetItem("#PY-2023-09"))
        self.recent_table.setItem(0, 1, QTableWidgetItem("Sep 01 - Sep 30"))
        self.recent_table.setItem(0, 2, QTableWidgetItem("—"))
        self.recent_table.setItem(0, 3, QTableWidgetItem("Completed"))
        self.recent_table.setItem(1, 0, QTableWidgetItem("#PY-2023-08"))
        self.recent_table.setItem(1, 1, QTableWidgetItem("Aug 01 - Aug 31"))
        self.recent_table.setItem(1, 2, QTableWidgetItem("—"))
        self.recent_table.setItem(1, 3, QTableWidgetItem("Completed"))
        self.recent_table.horizontalHeader().setStretchLastSection(True)
        self.recent_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        recent_l.addWidget(self.recent_table)
        recent.setLayout(recent_l)

        bottom_grid.addWidget(actions, 0, 0)
        bottom_grid.addWidget(recent, 0, 1)

        layout.addLayout(bottom_grid)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def _kpi_card(self, title: str, value: str, badge: str) -> QFrame:
        card = QFrame()
        card.setObjectName("Card")
        l = QVBoxLayout()
        l.setContentsMargins(16, 16, 16, 16)
        l.setSpacing(8)

        top = QHBoxLayout()
        t = QLabel(title)
        t.setStyleSheet("color: #92a4c9; font-size: 12px; font-weight: 700;")
        top.addWidget(t)
        top.addStretch()
        b = QLabel(badge)
        b.setStyleSheet("color: #92a4c9; font-size: 11px; font-weight: 700;")
        top.addWidget(b)
        l.addLayout(top)

        v = QLabel(value)
        v.setObjectName("KpiValue")
        v.setStyleSheet("font-size: 34px; font-weight: 900;")
        l.addWidget(v)
        l.addStretch()

        card.setLayout(l)
        return card

    def _panel(self, title: str, subtitle: str, body_text: str) -> QFrame:
        card = QFrame()
        card.setObjectName("Card")
        l = QVBoxLayout()
        l.setContentsMargins(16, 16, 16, 16)
        l.setSpacing(6)
        t = QLabel(title)
        t.setStyleSheet("font-size: 16px; font-weight: 800;")
        s = QLabel(subtitle)
        s.setStyleSheet("color: #92a4c9; font-size: 12px; font-weight: 600;")
        body = QLabel(body_text)
        body.setStyleSheet("color: #92a4c9; font-size: 11px;")
        body.setWordWrap(True)
        l.addWidget(t)
        l.addWidget(s)
        l.addSpacing(10)
        l.addWidget(body)
        l.addStretch()
        card.setLayout(l)
        return card
    
    def load_statistics(self):
        """Load and display statistics"""
        try:
            # Count employees
            employees = self.employee_repo.get_all(status=1)
            self._set_kpi_value(self.kpi_employees, str(len(employees)))
            
            # Count departments
            departments = self.master_repo.get_all_departments()
            # We don't show this in KPI row, but could be used for charts later.
            
            # Count designations
            designations = self.master_repo.get_all_designations()
            
            # Count branches
            branches = self.master_repo.get_all_branches()
            
            # Count shifts
            shifts = self.master_repo.get_all_shifts()
            
            # Count holidays
            holidays = self.master_repo.get_all_holidays()
            if holidays:
                # nearest upcoming holiday
                today = datetime.now().date()
                upcoming = sorted([h for h in holidays if h.holiday_date and h.holiday_date >= today], key=lambda h: h.holiday_date)
                if upcoming:
                    self._set_kpi_value(self.kpi_next_holiday, upcoming[0].holiday_name)
        except Exception as e:
            print(f"Error loading statistics: {e}")
    
    def _set_kpi_value(self, card: QFrame, value: str) -> None:
        # KPI value is the second widget in the layout (after the top row)
        lay = card.layout()
        if not lay:
            return
        for i in range(lay.count()):
            w = lay.itemAt(i).widget()
            if isinstance(w, QLabel) and w.objectName() == "KpiValue":
                w.setText(value)
                return

