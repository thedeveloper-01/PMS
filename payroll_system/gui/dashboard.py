"""
Dashboard widget showing statistics and overview
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QGridLayout, QFrame)
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
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Dashboard")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Statistics grid
        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(15)
        
        # Create stat cards
        self.employee_card = self.create_stat_card("Employees", "0", "#3498db")
        self.department_card = self.create_stat_card("Departments", "0", "#2ecc71")
        self.designation_card = self.create_stat_card("Designations", "0", "#e74c3c")
        self.branch_card = self.create_stat_card("Branches", "0", "#f39c12")
        self.shift_card = self.create_stat_card("Shifts", "0", "#9b59b6")
        self.holiday_card = self.create_stat_card("Holidays", "0", "#1abc9c")
        
        self.stats_grid.addWidget(self.employee_card, 0, 0)
        self.stats_grid.addWidget(self.department_card, 0, 1)
        self.stats_grid.addWidget(self.designation_card, 0, 2)
        self.stats_grid.addWidget(self.branch_card, 1, 0)
        self.stats_grid.addWidget(self.shift_card, 1, 1)
        self.stats_grid.addWidget(self.holiday_card, 1, 2)
        
        layout.addLayout(self.stats_grid)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def create_stat_card(self, title: str, value: str, color: str) -> QFrame:
        """Create a statistics card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 10px;
                padding: 20px;
                min-width: 200px;
                min-height: 120px;
            }}
            QLabel {{
                color: white;
            }}
        """)
        
        card_layout = QVBoxLayout()
        card_layout.setSpacing(10)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        card_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        card_layout.addWidget(value_label)
        
        card.setLayout(card_layout)
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
            if value_label:
                value_label.setText(value)

