"""
Main Application Window
UI FIXED – sidebar, navigation, stacking, theme-safe
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFrame
)
from PySide6.QtCore import Qt

from payroll_system.gui.dashboard import DashboardWidget
from payroll_system.gui.employee_management import EmployeeManagementWidget
from payroll_system.gui.attendance_management import AttendanceManagementWidget
from payroll_system.gui.payroll_management import PayrollManagementWidget
from payroll_system.gui.master_data_widgets import MasterDataWidget
from payroll_system.gui.reports_widget import ReportsWidget


class MainWindow(QMainWindow):

    def __init__(self, employee):
        super().__init__()
        self.employee = employee
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PayMaster")
        self.setMinimumSize(1200, 700)

        # ---------- Central Surface ----------
        surface = QWidget()
        surface.setObjectName("Surface")
        surface.setAttribute(Qt.WA_StyledBackground, True)

        root = QHBoxLayout(surface)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ======================================================
        # Sidebar
        # ======================================================
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setObjectName("Surface")
        sidebar.setAttribute(Qt.WA_StyledBackground, True)

        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(16, 20, 16, 20)
        side_layout.setSpacing(12)

        # ---------- App Title ----------
        title = QLabel("💼 PayMaster")
        title.setAlignment(Qt.AlignLeft)
        title.setAttribute(Qt.WA_TranslucentBackground, True)
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 800;
            }
        """)

        side_layout.addWidget(title)
        side_layout.addSpacing(8)

        # ---------- Nav Buttons ----------
        self.btn_dashboard = self.nav_button("📊 Dashboard")
        self.btn_employees = self.nav_button("👥 Employees")
        self.btn_attendance = self.nav_button("🕒 Attendance")
        self.btn_payroll = self.nav_button("💰 Payroll")
        self.btn_master = self.nav_button("⚙ Master Data")
        self.btn_reports = self.nav_button("📁 Reports")

        side_layout.addWidget(self.btn_dashboard)
        side_layout.addWidget(self.btn_employees)
        side_layout.addWidget(self.btn_attendance)
        side_layout.addWidget(self.btn_payroll)
        side_layout.addWidget(self.btn_master)
        side_layout.addWidget(self.btn_reports)

        side_layout.addStretch()

        # ---------- User Footer ----------
        footer = QLabel(f"Logged in as\n{self.employee.employee_name}")
        footer.setAttribute(Qt.WA_TranslucentBackground, True)
        footer.setStyleSheet("""
            QLabel {
                color: #94a3b8;
                font-size: 12px;
                padding-top: 12px;
            }
        """)
        side_layout.addWidget(footer)

        # ======================================================
        # Content Area
        # ======================================================
        self.stack = QStackedWidget()
        self.stack.setAttribute(Qt.WA_StyledBackground, True)

        self.page_dashboard = DashboardWidget(self.employee)
        self.page_employees = EmployeeManagementWidget()
        self.page_attendance = AttendanceManagementWidget()
        self.page_payroll = PayrollManagementWidget()
        self.page_master = MasterDataWidget()
        self.page_reports = ReportsWidget()

        self.stack.addWidget(self.page_dashboard)
        self.stack.addWidget(self.page_employees)
        self.stack.addWidget(self.page_attendance)
        self.stack.addWidget(self.page_payroll)
        self.stack.addWidget(self.page_master)
        self.stack.addWidget(self.page_reports)

        # ---------- Navigation ----------
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0))
        self.btn_employees.clicked.connect(lambda: self.switch_page(1))
        self.btn_attendance.clicked.connect(lambda: self.switch_page(2))
        self.btn_payroll.clicked.connect(lambda: self.switch_page(3))
        self.btn_master.clicked.connect(lambda: self.switch_page(4))
        self.btn_reports.clicked.connect(lambda: self.switch_page(5))

        self.set_active(self.btn_dashboard)
        self.stack.setCurrentIndex(0)

        # ---------- Assemble ----------
        root.addWidget(sidebar)
        root.addWidget(self.stack)
        self.setCentralWidget(surface)

    # ======================================================
    # Helpers
    # ======================================================
    def nav_button(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        btn.setFixedHeight(44)
        btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding-left: 14px;
                border-radius: 10px;
                font-weight: 600;
            }
            QPushButton:checked {
                background: rgba(19,91,236,0.18);
                border: 1px solid rgba(19,91,236,0.45);
            }
        """)
        return btn

    def set_active(self, btn: QPushButton):
        btn.setChecked(True)

    def switch_page(self, index: int):
        self.stack.setCurrentIndex(index)
