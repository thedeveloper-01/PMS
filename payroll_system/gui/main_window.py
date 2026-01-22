"""
Main window with sidebar navigation
"""
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QMessageBox,
    QFrame,
    QLineEdit,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from payroll_system.models.employee import Employee
from payroll_system.config import ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE, ROLE_NAMES
from payroll_system.gui.dashboard import DashboardWidget
from payroll_system.gui.employee_management import EmployeeManagementWidget
from payroll_system.gui.attendance_management import AttendanceManagementWidget
from payroll_system.gui.payroll_management import PayrollManagementWidget
from payroll_system.gui.reports_widget import ReportsWidget
from payroll_system.gui.master_data_widgets import MasterDataWidget

from typing import Dict, List, Tuple


class NavButton(QPushButton):
    """Sidebar navigation button with an 'active' property for QSS styling."""

    def __init__(self, text: str, parent: QWidget | None = None):
        super().__init__(text, parent)
        self.setObjectName("NavButton")
        self.setProperty("active", False)
        self.setCursor(Qt.PointingHandCursor)

    def set_active(self, active: bool) -> None:
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


class MainWindow(QMainWindow):
    """Main application window with navigation"""
    
    def __init__(self, employee: Employee):
        super().__init__()
        self.current_employee = employee
        self._nav_buttons: Dict[int, NavButton] = {}
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Payroll Management System")
        self.setMinimumSize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Right side (Topbar + content)
        right = QFrame()
        right.setObjectName("Surface")
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        topbar = self.create_topbar()
        right_layout.addWidget(topbar)

        content_wrap = QFrame()
        content_wrap.setObjectName("Surface")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(0)

        # Content area
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout.addWidget(self.stacked_widget)
        content_wrap.setLayout(content_layout)

        right_layout.addWidget(content_wrap, 1)
        right.setLayout(right_layout)
        main_layout.addWidget(right, 1)
        
        # Add widgets to stack
        self.dashboard = DashboardWidget(self.current_employee)
        self.employee_mgmt = EmployeeManagementWidget()
        self.attendance_mgmt = AttendanceManagementWidget()
        self.payroll_mgmt = PayrollManagementWidget()
        self.reports = ReportsWidget()
        self.master_data = MasterDataWidget()
        
        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.addWidget(self.employee_mgmt)
        self.stacked_widget.addWidget(self.attendance_mgmt)
        self.stacked_widget.addWidget(self.payroll_mgmt)
        self.stacked_widget.addWidget(self.reports)
        self.stacked_widget.addWidget(self.master_data)
        
        # Show dashboard by default
        self.stacked_widget.setCurrentIndex(0)
        self._set_active_nav(0)
        
        central_widget.setLayout(main_layout)
    
    def create_sidebar(self):
        """Create sidebar navigation"""
        sidebar = QFrame()
        sidebar.setObjectName("Surface")
        sidebar.setFixedWidth(280)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)
        
        # Brand / profile area (like screenshots)
        brand = QFrame()
        brand.setObjectName("Card")
        brand_layout = QVBoxLayout()
        brand_layout.setContentsMargins(14, 14, 14, 14)
        brand_layout.setSpacing(4)

        app_name = QLabel("PayMaster")
        app_name.setStyleSheet("font-size: 16px; font-weight: 800;")
        role = QLabel(ROLE_NAMES.get(self.current_employee.role, "Employee"))
        role.setStyleSheet("color: #92a4c9; font-size: 12px; font-weight: 600;")
        brand_layout.addWidget(app_name)
        brand_layout.addWidget(role)
        brand.setLayout(brand_layout)
        layout.addWidget(brand)
        
        # Navigation buttons
        nav_buttons: List[Tuple[str, int]] = [
            ("Dashboard", 0),
            ("Employees", 1),
            ("Attendance", 2),
            ("Payroll", 3),
            ("Reports", 4),
            ("Master Data", 5),
        ]
        
        # Show all buttons for Admin/HR, limited for Employee
        if self.current_employee.role in [ROLE_ADMIN, ROLE_HR]:
            for text, index in nav_buttons:
                btn = NavButton(text)
                btn.clicked.connect(lambda checked=False, idx=index: self.navigate_to(idx))
                layout.addWidget(btn)
                self._nav_buttons[index] = btn
        else:
            # Employee can only see limited options
            limited_nav = [
                ("Dashboard", 0),
                ("Attendance", 2),
                ("Payroll", 3),
            ]
            for text, index in limited_nav:
                btn = NavButton(text)
                btn.clicked.connect(lambda checked=False, idx=index: self.navigate_to(idx))
                layout.addWidget(btn)
                self._nav_buttons[index] = btn
        
        layout.addStretch()
        
        # Logout button
        logout_btn = QPushButton("Sign Out")
        logout_btn.setObjectName("DangerButton")
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
        
        sidebar.setLayout(layout)
        return sidebar

    def create_topbar(self) -> QFrame:
        """Top bar (title + search + user) similar to screenshots."""
        top = QFrame()
        top.setObjectName("Surface")
        top.setFixedHeight(72)
        lay = QHBoxLayout()
        lay.setContentsMargins(24, 12, 24, 12)
        lay.setSpacing(16)

        self.page_title = QLabel("Dashboard Overview")
        self.page_title.setStyleSheet("font-size: 18px; font-weight: 800;")
        lay.addWidget(self.page_title)

        lay.addStretch()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search employees...")
        self.search.setFixedWidth(320)
        lay.addWidget(self.search)

        user = QLabel(f"{self.current_employee.employee_name}  •  {ROLE_NAMES.get(self.current_employee.role,'Employee')}")
        user.setStyleSheet("color: #92a4c9; font-size: 12px; font-weight: 700;")
        lay.addWidget(user)

        top.setLayout(lay)
        return top
    
    def navigate_to(self, index):
        """Navigate to a specific page"""
        self.stacked_widget.setCurrentIndex(index)
        self._set_active_nav(index)
        self._set_title_for_index(index)

    def _set_active_nav(self, index: int) -> None:
        for idx, btn in self._nav_buttons.items():
            btn.set_active(idx == index)

    def _set_title_for_index(self, index: int) -> None:
        titles = {
            0: "Dashboard Overview",
            1: "Employee Directory",
            2: "Attendance Management",
            3: "Monthly Payroll Processing",
            4: "Reports & Analytics",
            5: "Master Data",
        }
        if hasattr(self, "page_title"):
            self.page_title.setText(titles.get(index, "Payroll System"))
    
    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

