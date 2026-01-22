
"""
Dashboard widget showing statistics and overview
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QGridLayout, QFrame, QScrollArea, QSizePolicy,
                               QSpacerItem)
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
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                width: 8px;
                background: transparent;
            }
            QScrollBar::handle:vertical {
                background: #4a5568;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #718096;
            }
        """)
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(30)
        content_layout.setContentsMargins(40, 30, 40, 40)
        
        # Welcome section
        welcome_section = self.create_welcome_section()
        content_layout.addWidget(welcome_section)
        
        # Statistics section
        stats_section = self.create_statistics_section()
        content_layout.addWidget(stats_section)
        
        content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
    
    def create_welcome_section(self):
        """Create welcome section"""
        section = QFrame()
        section.setObjectName("Card")
        
        layout = QVBoxLayout(section)
        layout.setSpacing(10)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Welcome message
        welcome_label = QLabel(f"👋 Welcome back, {self.employee.employee_name}!")
        welcome_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 700;
                color: #ffffff;
            }
        """)
        layout.addWidget(welcome_label)
        
        # Date
        date_label = QLabel(datetime.now().strftime("%A, %B %d, %Y"))
        date_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #a0aec0;
                margin-top: 5px;
            }
        """)
        layout.addWidget(date_label)
        
        return section
    
    def create_statistics_section(self):
        """Create statistics section"""
        section = QFrame()
        
        layout = QVBoxLayout(section)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Section title
        title = QLabel("System Statistics")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #ffffff;
            }
        """)
        layout.addWidget(title)
        
        # Statistics grid
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)
        
        # Create stat cards
        self.employee_card = self.create_stat_card("Total Employees", "1", "#3b82f6")
        self.department_card = self.create_stat_card("Departments", "1", "#10b981")
        self.designation_card = self.create_stat_card("Designations", "0", "#a855f7")
        self.branch_card = self.create_stat_card("Branches", "1", "#f97316")
        self.shift_card = self.create_stat_card("Active Shifts", "1", "#06b6d4")
        self.holiday_card = self.create_stat_card("Upcoming Holidays", "0", "#f59e0b")
        
        # Add to grid (2 columns, 3 rows)
        grid.addWidget(self.employee_card, 0, 0)
        grid.addWidget(self.department_card, 0, 1)
        grid.addWidget(self.designation_card, 1, 0)
        grid.addWidget(self.branch_card, 1, 1)
        grid.addWidget(self.shift_card, 2, 0)
        grid.addWidget(self.holiday_card, 2, 1)
        
        layout.addLayout(grid)
        
        return section
    
    def create_stat_card(self, title: str, value: str, color: str):
        """Create a statistics card"""
        card = QFrame()
        card.setObjectName("Card")
        card.setMinimumHeight(120)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: #a0aec0;
                font-weight: 600;
            }}
        """)
        layout.addWidget(title_label)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 32px;
                color: {color};
                font-weight: 800;
            }}
        """)
        layout.addWidget(value_label)
        
        layout.addStretch()
        
        return card
    
    def load_statistics(self):
        """Load and display statistics"""
        try:
            # Count employees
            employees = self.employee_repo.get_all(status=1)
            self.update_stat_card(self.employee_card, str(len(employees)))
            
            # Count departments
            departments = self.master_repo.get_all_departments()
            self.update_stat_card(self.department_card, str(len(departments)))
            
            # Count designations
            designations = self.master_repo.get_all_designations()
            self.update_stat_card(self.designation_card, str(len(designations)))
            
            # Count branches
            branches = self.master_repo.get_all_branches()
            self.update_stat_card(self.branch_card, str(len(branches)))
            
            # Count shifts
            shifts = self.master_repo.get_all_shifts()
            self.update_stat_card(self.shift_card, str(len(shifts)))
            
            # Count holidays
            holidays = self.master_repo.get_all_holidays()
            self.update_stat_card(self.holiday_card, str(len(holidays)))
            
        except Exception as e:
            print(f"Error loading statistics: {e}")
    
    def update_stat_card(self, card: QFrame, value: str):
        """Update stat card value"""
        layout = card.layout()
        if layout and layout.count() > 1:
            value_label = layout.itemAt(1).widget()
            if value_label and isinstance(value_label, QLabel):
                value_label.setText(value)
