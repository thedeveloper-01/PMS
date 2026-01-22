"""
Master data management widgets
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTabWidget, QTableWidget,
                              QTableWidgetItem, QMessageBox, QDialog,
                              QFormLayout, QLineEdit, QDateEdit)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from payroll_system.repository.master_data_repository import MasterDataRepository
from payroll_system.models.master_data import Department, Designation, Branch, Shift, Holiday
from datetime import datetime

class MasterDataWidget(QWidget):
    """Master data management widget"""
    
    def __init__(self):
        super().__init__()
        self.master_repo = MasterDataRepository()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Master Data Management")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Tabs
        tabs = QTabWidget()
        
        # Department tab
        dept_widget = MasterDataTableWidget("Department", self.master_repo)
        tabs.addTab(dept_widget, "Departments")
        
        # Designation tab
        des_widget = MasterDataTableWidget("Designation", self.master_repo)
        tabs.addTab(des_widget, "Designations")
        
        # Branch tab
        branch_widget = MasterDataTableWidget("Branch", self.master_repo)
        tabs.addTab(branch_widget, "Branches")
        
        # Shift tab
        shift_widget = MasterDataTableWidget("Shift", self.master_repo)
        tabs.addTab(shift_widget, "Shifts")
        
        # Holiday tab
        holiday_widget = MasterDataTableWidget("Holiday", self.master_repo)
        tabs.addTab(holiday_widget, "Holidays")
        
        layout.addWidget(tabs)
        self.setLayout(layout)

class MasterDataTableWidget(QWidget):
    """Generic master data table widget"""
    
    def __init__(self, data_type: str, master_repo: MasterDataRepository):
        super().__init__()
        self.data_type = data_type
        self.master_repo = master_repo
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        
        add_btn = QPushButton(f"Add {self.data_type}")
        add_btn.clicked.connect(self.add_item)
        header_layout.addWidget(add_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_data)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        if self.data_type == "Department":
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(["ID", "Name"])
        elif self.data_type == "Designation":
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["ID", "Name", "Department"])
        elif self.data_type == "Branch":
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(["ID", "Name", "Address", "Phone"])
        elif self.data_type == "Shift":
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(["ID", "Name", "In Time", "Out Time"])
        elif self.data_type == "Holiday":
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["ID", "Name", "Date"])
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_data(self):
        """Load data into table"""
        try:
            if self.data_type == "Department":
                items = self.master_repo.get_all_departments()
                self.table.setRowCount(len(items))
                for row, item in enumerate(items):
                    self.table.setItem(row, 0, QTableWidgetItem(item.department_id))
                    self.table.setItem(row, 1, QTableWidgetItem(item.department_name))
            elif self.data_type == "Designation":
                items = self.master_repo.get_all_designations()
                self.table.setRowCount(len(items))
                for row, item in enumerate(items):
                    self.table.setItem(row, 0, QTableWidgetItem(item.designation_id))
                    self.table.setItem(row, 1, QTableWidgetItem(item.designation_name))
                    self.table.setItem(row, 2, QTableWidgetItem(item.department_name))
            elif self.data_type == "Branch":
                items = self.master_repo.get_all_branches()
                self.table.setRowCount(len(items))
                for row, item in enumerate(items):
                    self.table.setItem(row, 0, QTableWidgetItem(item.branch_id))
                    self.table.setItem(row, 1, QTableWidgetItem(item.name))
                    self.table.setItem(row, 2, QTableWidgetItem(item.branch_address))
                    self.table.setItem(row, 3, QTableWidgetItem(item.phone_number))
            elif self.data_type == "Shift":
                items = self.master_repo.get_all_shifts()
                self.table.setRowCount(len(items))
                for row, item in enumerate(items):
                    self.table.setItem(row, 0, QTableWidgetItem(item.shift_id))
                    self.table.setItem(row, 1, QTableWidgetItem(item.shift_name))
                    self.table.setItem(row, 2, QTableWidgetItem(item.in_time))
                    self.table.setItem(row, 3, QTableWidgetItem(item.out_time))
            elif self.data_type == "Holiday":
                items = self.master_repo.get_all_holidays()
                self.table.setRowCount(len(items))
                for row, item in enumerate(items):
                    self.table.setItem(row, 0, QTableWidgetItem(item.holiday_id))
                    self.table.setItem(row, 1, QTableWidgetItem(item.holiday_name))
                    date_str = item.holiday_date.isoformat() if hasattr(item.holiday_date, 'isoformat') else str(item.holiday_date)
                    self.table.setItem(row, 2, QTableWidgetItem(date_str))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading data: {str(e)}")
    
    def add_item(self):
        """Add new item"""
        QMessageBox.information(self, "Info", 
                               f"Add {self.data_type} functionality can be extended here")

