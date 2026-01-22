
"""
Dashboard widget showing statistics and overview
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QGridLayout, QFrame, QScrollArea, QSizePolicy,
                               QSpacerItem, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
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
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(24)
        content_layout.setContentsMargins(32, 24, 32, 24)
        
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
        # section.setObjectName("Surface") # Removed to blend with background
        
        layout = QVBoxLayout(section)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 10)
        
        # Welcome message
        welcome_label = QLabel(f"Welcome back, {self.employee.employee_name}")
        welcome_label.setObjectName("PageTitle")
        layout.addWidget(welcome_label)
        
        # Date
        date_label = QLabel(datetime.now().strftime("%A, %B %d, %Y"))
        date_label.setObjectName("PageSubtitle")
        layout.addWidget(date_label)
        
        return section
    
    def create_statistics_section(self):
        """Create statistics section"""
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Section title
        title = QLabel("Overview")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)
        
        # Statistics grid
        grid = QGridLayout()
        grid.setSpacing(16)
        grid.setContentsMargins(0, 0, 0, 0)
        
        # Create stat cards
        self.employee_card = self.create_stat_card("Total Employees", "...", "#3b82f6", "👥")
        self.department_card = self.create_stat_card("Departments", "...", "#10b981", "🏢")
        self.designation_card = self.create_stat_card("Designations", "...", "#a855f7", "💼")
        self.branch_card = self.create_stat_card("Branches", "...", "#f97316", "📍")
        self.shift_card = self.create_stat_card("Active Shifts", "...", "#06b6d4", "🕒")
        self.holiday_card = self.create_stat_card("Holidays", "...", "#f59e0b", "📅")
        
        # Add to grid (3 columns, 2 rows)
        grid.addWidget(self.employee_card, 0, 0)
        grid.addWidget(self.department_card, 0, 1)
        grid.addWidget(self.designation_card, 0, 2)
        grid.addWidget(self.branch_card, 1, 0)
        grid.addWidget(self.shift_card, 1, 1)
        grid.addWidget(self.holiday_card, 1, 2)
        
        layout.addLayout(grid)
        
        return section
    
    def create_stat_card(self, title: str, value: str, color: str, icon_name: str = ""):
        """Create a statistics card"""
        card = QFrame()
        card.setObjectName("StatCard")
        card.setMinimumHeight(130)
        
        # Apply shadow
        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 60))
        card.setGraphicsEffect(shadow)
        
        # Use inline style to set the side border color dynamically
        card.setStyleSheet(f"""
            QFrame#StatCard {{
                border-left: 4px solid {color};
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Top row (Title + Icon)
        top_row = QHBoxLayout()
        top_row.setSpacing(10)
        
        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")
        top_row.addWidget(title_label)
        
        top_row.addStretch()
        
        # Icon
        icon_label = QLabel(icon_name)
        icon_label.setStyleSheet(f"font-size: 24px; color: {color};")
        top_row.addWidget(icon_label)
        
        layout.addLayout(top_row)
        
        # Spacer
        layout.addStretch()
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName("CardValue")
        # value_label.setStyleSheet(f"color: {color};") # Remove specific color override to use theme
        layout.addWidget(value_label)
        
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
        value_label = card.findChild(QLabel, "CardValue")
        if value_label:
            value_label.setText(value)

    def refresh_data(self):
        """Refresh data when tab is active"""
        self.load_statistics()
