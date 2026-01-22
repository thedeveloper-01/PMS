
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
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon
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

    def __init__(self, text: str, icon: str = "", parent: QWidget | None = None):
        super().__init__(text, parent)
        self.setObjectName("NavButton")
        self.setProperty("active", False)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(False)
        
        # Set icon if provided
        if icon:
            self.setText(f"{icon}  {text}")

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
        self.setWindowTitle("PayMaster - Payroll Management System")
        self.setMinimumSize(1280, 800)
        
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
        content_layout.setContentsMargins(0, 0, 0, 0)
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
        self._set_title_for_index(0)
        
        central_widget.setLayout(main_layout)
    
    def create_sidebar(self):
        """Create sidebar navigation"""
        sidebar = QFrame()
        sidebar.setStyleSheet("""
            QFrame {
                background: #111827;
                border-right: 1px solid #374151;
            }
        """)
        sidebar.setFixedWidth(280)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Brand section
        brand_frame = QFrame()
        brand_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border-bottom: 1px solid #374151;
                padding: 20px;
            }
        """)
        brand_layout = QHBoxLayout(brand_frame)
        brand_layout.setContentsMargins(15, 15, 15, 15)
        brand_layout.setSpacing(15)
        
        # Logo/Icon
        logo_label = QLabel("💰")
        logo_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                background: rgba(59, 130, 246, 0.2);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        logo_label.setFixedSize(50, 50)
        logo_label.setAlignment(Qt.AlignCenter)
        
        # App name and role
        text_frame = QFrame()
        text_layout = QVBoxLayout(text_frame)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        
        app_label = QLabel("PayMaster")
        app_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 700;
                color: #ffffff;
            }
        """)
        
        role_label = QLabel(ROLE_NAMES.get(self.current_employee.role, "Employee"))
        role_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #9ca3af;
                font-weight: 500;
            }
        """)
        
        text_layout.addWidget(app_label)
        text_layout.addWidget(role_label)
        
        brand_layout.addWidget(logo_label)
        brand_layout.addWidget(text_frame)
        brand_layout.addStretch()
        
        layout.addWidget(brand_frame)
        
        # Navigation section
        nav_frame = QFrame()
        nav_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                padding: 20px 15px;
            }
        """)
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(10, 10, 10, 10)
        nav_layout.setSpacing(5)
        
        # Navigation buttons based on role
        if self.current_employee.role in [ROLE_ADMIN, ROLE_HR]:
            nav_items = [
                ("📊 Dashboard", 0),
                ("👥 Employees", 1),
                ("✓ Attendance", 2),
                ("💰 Payroll", 3),
                ("📈 Reports", 4),
                ("⚙️ Master Data", 5),
            ]
        else:
            # Employee can only see limited options
            nav_items = [
                ("📊 Dashboard", 0),
                ("✓ Attendance", 2),
                ("💰 Payroll", 3),
            ]
        
        for icon_text, index in nav_items:
            btn = NavButton(icon_text)
            btn.setFixedHeight(45)
            btn.clicked.connect(lambda checked=False, idx=index: self.navigate_to(idx))
            nav_layout.addWidget(btn)
            self._nav_buttons[index] = btn
        
        nav_layout.addStretch()
        layout.addWidget(nav_frame, 1)
        
        # Logout section
        logout_frame = QFrame()
        logout_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border-top: 1px solid #374151;
                padding: 15px;
            }
        """)
        logout_layout = QHBoxLayout(logout_frame)
        logout_layout.setContentsMargins(15, 10, 15, 10)
        
        logout_btn = QPushButton("🚪 Sign Out")
        logout_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                text-align: left;
                color: #9ca3af;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.1);
                color: #fca5a5;
            }
        """)
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.clicked.connect(self.logout)
        logout_layout.addWidget(logout_btn)
        logout_layout.addStretch()
        
        layout.addWidget(logout_frame)
        
        sidebar.setLayout(layout)
        return sidebar

    def create_topbar(self) -> QFrame:
        """Top bar (title + search + user)"""
        top = QFrame()
        top.setStyleSheet("""
            QFrame {
                background: #1f2937;
                border-bottom: 1px solid #374151;
            }
        """)
        top.setFixedHeight(70)
        lay = QHBoxLayout()
        lay.setContentsMargins(25, 0, 25, 0)
        lay.setSpacing(20)

        # Page title
        self.page_title = QLabel("Dashboard Overview")
        self.page_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 700;
                color: #ffffff;
            }
        """)
        lay.addWidget(self.page_title)

        lay.addStretch()

        # Search bar
        search_frame = QFrame()
        search_frame.setObjectName("CardAlt")
        search_frame.setFixedHeight(40)
        
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(12, 0, 12, 0)
        
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("color: #9ca3af; font-size: 14px;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search employees...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: #ffffff;
                font-size: 14px;
                padding: 8px;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
        """)
        self.search_input.setFixedWidth(250)
        
        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input)
        lay.addWidget(search_frame)

        # User info
        user_frame = QFrame()
        user_frame.setStyleSheet("background: transparent;")
        
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(0, 0, 0, 0)
        user_layout.setSpacing(2)
        
        user_name = QLabel(self.current_employee.employee_name)
        user_name.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: 600;")
        
        user_role = QLabel(ROLE_NAMES.get(self.current_employee.role, 'Employee'))
        user_role.setStyleSheet("color: #9ca3af; font-size: 12px;")
        
        user_layout.addWidget(user_name)
        user_layout.addWidget(user_role)
        lay.addWidget(user_frame)

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
            5: "Master Data Management",
        }
        self.page_title.setText(titles.get(index, "PayMaster"))
    
    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self, "Logout", 
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()
