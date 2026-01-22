"""
Login window for the Payroll Management System
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                                QLineEdit, QPushButton, QMessageBox, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon
from payroll_system.services.employee_service import EmployeeService
from payroll_system.config import ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE, ROLE_NAMES

class LoginWindow(QWidget):
    """Login window widget"""
    
    login_successful = Signal(object)  # Emits employee object on successful login
    
    def __init__(self):
        super().__init__()
        self.employee_service = EmployeeService()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI components"""
        self.setWindowTitle("Payroll Management System - Login")
        self.setFixedSize(450, 350)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("PAYROLL MANAGEMENT SYSTEM")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2196F3; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Login form frame
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Subtitle
        subtitle = QLabel("Sign in to start your session")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666; font-size: 12px; margin-bottom: 10px;")
        form_layout.addWidget(subtitle)
        
        # Email/Username field
        email_label = QLabel("Email/Username:")
        email_label.setStyleSheet("font-weight: bold;")
        form_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        form_layout.addWidget(self.email_input)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-weight: bold;")
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_input)
        
        # Login button
        login_btn = QPushButton("SIGN IN")
        login_btn.clicked.connect(self.handle_login)
        form_layout.addWidget(login_btn)
        
        # Allow Enter key to trigger login
        self.password_input.returnPressed.connect(self.handle_login)
        
        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        
        self.setLayout(layout)
        
        # Center window
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
    
    def handle_login(self):
        """Handle login button click"""
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        if not email or not password:
            QMessageBox.warning(self, "Login Failed", 
                              "Please enter both email and password")
            return
        
        employee, message = self.employee_service.authenticate(email, password)
        
        if employee:
            QMessageBox.information(self, "Login Successful", 
                                  f"Welcome, {employee.employee_name}!\n"
                                  f"Role: {ROLE_NAMES.get(employee.role, 'Employee')}")
            self.login_successful.emit(employee)
        else:
            QMessageBox.critical(self, "Login Failed", message)

