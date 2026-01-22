"""
Main window with sidebar navigation
"""
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel, QStackedWidget, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon
from payroll_system.models.employee import Employee
from payroll_system.config import ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE, ROLE_NAMES
from payroll_system.gui.dashboard import DashboardWidget
from payroll_system.gui.employee_management import EmployeeManagementWidget
from payroll_system.gui.attendance_management import AttendanceManagementWidget
from payroll_system.gui.payroll_management import PayrollManagementWidget
from payroll_system.gui.reports_widget import ReportsWidget
from payroll_system.gui.master_data_widgets import MasterDataWidget

class MainWindow(QMainWindow):
    """Main application window with navigation"""
    
    def __init__(self, employee: Employee):
        super().__init__()
        self.current_employee = employee
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
        
        # Content area
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget, 1)
        
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
        
        central_widget.setLayout(main_layout)
        
        # Apply styles
        self.apply_styles()
    
    def create_sidebar(self):
        """Create sidebar navigation"""
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
            }
            QPushButton {
                background-color: #34495e;
                color: white;
                text-align: left;
                padding: 15px;
                border: none;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
            QLabel {
                color: white;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # User info
        user_info = QLabel(f"{self.current_employee.employee_name}\n"
                          f"{self.current_employee.email}\n"
                          f"Role: {ROLE_NAMES.get(self.current_employee.role, 'Employee')}")
        user_info.setStyleSheet("""
            QLabel {
                background-color: #34495e;
                padding: 15px;
                border-bottom: 2px solid #2c3e50;
            }
        """)
        layout.addWidget(user_info)
        
        # Navigation buttons
        nav_buttons = [
            ("Home", 0),
            ("Employee Management", 1),
            ("Attendance", 2),
            ("Payroll", 3),
            ("Reports", 4),
            ("Master Data", 5),
        ]
        
        # Show all buttons for Admin/HR, limited for Employee
        if self.current_employee.role in [ROLE_ADMIN, ROLE_HR]:
            for text, index in nav_buttons:
                btn = QPushButton(text)
                btn.clicked.connect(lambda checked, idx=index: self.navigate_to(idx))
                layout.addWidget(btn)
        else:
            # Employee can only see limited options
            limited_nav = [
                ("Home", 0),
                ("Attendance", 2),
                ("Payroll", 3),
            ]
            for text, index in limited_nav:
                btn = QPushButton(text)
                btn.clicked.connect(lambda checked, idx=index: self.navigate_to(idx))
                layout.addWidget(btn)
        
        layout.addStretch()
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
        
        sidebar.setLayout(layout)
        return sidebar
    
    def navigate_to(self, index):
        """Navigate to a specific page"""
        self.stacked_widget.setCurrentIndex(index)
    
    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
    
    def apply_styles(self):
        """Apply application-wide styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
        """)

