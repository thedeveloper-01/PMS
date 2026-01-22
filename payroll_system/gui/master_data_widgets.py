
"""
Master data management widgets
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTabWidget, QTableWidget,
                              QTableWidgetItem, QMessageBox, QDialog,
                              QFormLayout, QLineEdit, QDateEdit, QTimeEdit,
                              QDialogButtonBox, QHBoxLayout, QVBoxLayout,
                              QComboBox, QHeaderView)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from payroll_system.repository.master_data_repository import MasterDataRepository
from payroll_system.models.master_data import Department, Designation, Branch, Shift, Holiday
from datetime import datetime, time

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
        title.setObjectName("PageTitle")
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
    def refresh_data(self):
        """Refresh data for all tabs"""
        # Iterate through all tabs and refresh if they have the method
        for i in range(self.findChild(QTabWidget).count()):
            widget = self.findChild(QTabWidget).widget(i)
            if hasattr(widget, 'load_data'):
                widget.load_data()
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
        
        title = QLabel(f"{self.data_type} Management")
        title.setObjectName("SectionTitle") # or Subtitle/CardTitle
        # Actually PageTitle is 24px, SectionTitle I might need to check theme.py
        # theme.py has PageTitle (24px bold)
        # It doesn't seem to have SectionTitle. 
        # I'll use CardTitle (18px bold) or just standard style.
        # Original was 14px bold. 14px is small for a title.
        # I'll use "CardTitle" which is usually 16-18px.
        title.setObjectName("CardTitle")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        add_btn = QPushButton(f"➕ Add {self.data_type}")
        add_btn.setObjectName("PrimaryButton")
        add_btn.clicked.connect(self.add_item)
        header_layout.addWidget(add_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_data)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(70)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        if self.data_type == "Department":
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["ID", "Name", "Actions"])
        elif self.data_type == "Designation":
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(["ID", "Name", "Department", "Actions"])
        elif self.data_type == "Branch":
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(["ID", "Name", "Address", "Phone", "Actions"])
        elif self.data_type == "Shift":
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(["ID", "Name", "In Time", "Out Time", "Actions"])
        elif self.data_type == "Holiday":
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(["ID", "Name", "Date", "Actions"])
        
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
                    
                    # Action buttons
                    actions_widget = QWidget()
                    actions_layout = QHBoxLayout(actions_widget)
                    actions_layout.setContentsMargins(0, 0, 0, 0)
                    
                    delete_btn = QPushButton("🗑️")
                    delete_btn.setToolTip("Delete")
                    delete_btn.setObjectName("DangerButton")
                    delete_btn.setFixedSize(40, 40)
                    delete_btn.clicked.connect(lambda checked, item_id=item.department_id: 
                                              self.delete_item(item_id))
                    actions_layout.addWidget(delete_btn)
                    
                    self.table.setCellWidget(row, 2, actions_widget)
                    
            elif self.data_type == "Designation":
                items = self.master_repo.get_all_designations()
                self.table.setRowCount(len(items))
                for row, item in enumerate(items):
                    self.table.setItem(row, 0, QTableWidgetItem(item.designation_id))
                    self.table.setItem(row, 1, QTableWidgetItem(item.designation_name))
                    self.table.setItem(row, 2, QTableWidgetItem(item.department_name))
                    
                    # Action buttons
                    actions_widget = QWidget()
                    actions_layout = QHBoxLayout(actions_widget)
                    actions_layout.setContentsMargins(0, 0, 0, 0)
                    
                    delete_btn = QPushButton("🗑️")
                    delete_btn.setToolTip("Delete")
                    delete_btn.setObjectName("DangerButton")
                    delete_btn.setFixedSize(40, 40)
                    delete_btn.clicked.connect(lambda checked, item_id=item.designation_id: 
                                              self.delete_item(item_id))
                    actions_layout.addWidget(delete_btn)
                    
                    self.table.setCellWidget(row, 3, actions_widget)
                    
            elif self.data_type == "Branch":
                items = self.master_repo.get_all_branches()
                self.table.setRowCount(len(items))
                for row, item in enumerate(items):
                    self.table.setItem(row, 0, QTableWidgetItem(item.branch_id))
                    self.table.setItem(row, 1, QTableWidgetItem(item.name))
                    self.table.setItem(row, 2, QTableWidgetItem(item.branch_address))
                    self.table.setItem(row, 3, QTableWidgetItem(item.phone_number))
                    
                    # Action buttons
                    actions_widget = QWidget()
                    actions_layout = QHBoxLayout(actions_widget)
                    actions_layout.setContentsMargins(0, 0, 0, 0)
                    
                    delete_btn = QPushButton("🗑️")
                    delete_btn.setToolTip("Delete")
                    delete_btn.setObjectName("DangerButton")
                    delete_btn.setFixedSize(40, 40)
                    delete_btn.clicked.connect(lambda checked, item_id=item.branch_id: 
                                              self.delete_item(item_id))
                    actions_layout.addWidget(delete_btn)
                    
                    self.table.setCellWidget(row, 4, actions_widget)
                    
            elif self.data_type == "Shift":
                items = self.master_repo.get_all_shifts()
                self.table.setRowCount(len(items))
                for row, item in enumerate(items):
                    self.table.setItem(row, 0, QTableWidgetItem(item.shift_id))
                    self.table.setItem(row, 1, QTableWidgetItem(item.shift_name))
                    self.table.setItem(row, 2, QTableWidgetItem(item.in_time))
                    self.table.setItem(row, 3, QTableWidgetItem(item.out_time))
                    
                    # Action buttons
                    actions_widget = QWidget()
                    actions_layout = QHBoxLayout(actions_widget)
                    actions_layout.setContentsMargins(0, 0, 0, 0)
                    
                    delete_btn = QPushButton("🗑️")
                    delete_btn.setToolTip("Delete")
                    delete_btn.setObjectName("DangerButton")
                    delete_btn.setFixedSize(40, 40)
                    delete_btn.clicked.connect(lambda checked, item_id=item.shift_id: 
                                              self.delete_item(item_id))
                    actions_layout.addWidget(delete_btn)
                    
                    self.table.setCellWidget(row, 4, actions_widget)
                    
            elif self.data_type == "Holiday":
                items = self.master_repo.get_all_holidays()
                self.table.setRowCount(len(items))
                for row, item in enumerate(items):
                    self.table.setItem(row, 0, QTableWidgetItem(item.holiday_id))
                    self.table.setItem(row, 1, QTableWidgetItem(item.holiday_name))
                    date_str = item.holiday_date.isoformat() if hasattr(item.holiday_date, 'isoformat') else str(item.holiday_date)
                    self.table.setItem(row, 2, QTableWidgetItem(date_str))
                    
                    # Action buttons
                    actions_widget = QWidget()
                    actions_layout = QHBoxLayout(actions_widget)
                    actions_layout.setContentsMargins(0, 0, 0, 0)
                    
                    delete_btn = QPushButton("🗑️")
                    delete_btn.setToolTip("Delete")
                    delete_btn.setObjectName("DangerButton")
                    delete_btn.setFixedSize(40, 40)
                    delete_btn.clicked.connect(lambda checked, item_id=item.holiday_id: 
                                              self.delete_item(item_id))
                    actions_layout.addWidget(delete_btn)
                    
                    self.table.setCellWidget(row, 3, actions_widget)
            
            # self.table.resizeColumnsToContents()
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading data: {str(e)}")
    
    def add_item(self):
        """Add new item dialog"""
        dialog = MasterDataDialog(self.data_type, self.master_repo, self)
        if dialog.exec() == QDialog.Accepted:
            self.load_data()
    
    def delete_item(self, item_id: str):
        """Delete item"""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete this {self.data_type.lower()}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                if self.data_type == "Department":
                    success = self.master_repo.delete_department(item_id)
                elif self.data_type == "Designation":
                    success = self.master_repo.delete_designation(item_id)
                elif self.data_type == "Branch":
                    success = self.master_repo.delete_branch(item_id)
                elif self.data_type == "Shift":
                    success = self.master_repo.delete_shift(item_id)
                elif self.data_type == "Holiday":
                    success = self.master_repo.delete_holiday(item_id)
                else:
                    success = False
                
                if success:
                    QMessageBox.information(self, "Success", f"{self.data_type} deleted successfully")
                    self.load_data()
                else:
                    QMessageBox.warning(self, "Error", f"Failed to delete {self.data_type.lower()}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error deleting item: {str(e)}")

class MasterDataDialog(QDialog):
    """Dialog for adding master data items"""
    
    def __init__(self, data_type: str, master_repo: MasterDataRepository, parent=None):
        super().__init__(parent)
        self.data_type = data_type
        self.master_repo = master_repo
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog UI"""
        self.setWindowTitle(f"Add {self.data_type}")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        if self.data_type == "Department":
            self.id_input = QLineEdit()
            self.name_input = QLineEdit()
            
            form_layout.addRow("Department ID:", self.id_input)
            form_layout.addRow("Department Name:", self.name_input)
            
        elif self.data_type == "Designation":
            self.id_input = QLineEdit()
            self.name_input = QLineEdit()
            self.dept_combo = QComboBox()
            
            # Load departments
            departments = self.master_repo.get_all_departments()
            self.dept_combo.addItem("Select Department", None)
            for dept in departments:
                self.dept_combo.addItem(dept.department_name, dept.department_id)
            
            form_layout.addRow("Designation ID:", self.id_input)
            form_layout.addRow("Designation Name:", self.name_input)
            form_layout.addRow("Department:", self.dept_combo)
            
        elif self.data_type == "Branch":
            self.id_input = QLineEdit()
            self.name_input = QLineEdit()
            self.address_input = QLineEdit()
            self.phone_input = QLineEdit()
            
            form_layout.addRow("Branch ID:", self.id_input)
            form_layout.addRow("Branch Name:", self.name_input)
            form_layout.addRow("Address:", self.address_input)
            form_layout.addRow("Phone:", self.phone_input)
            
        elif self.data_type == "Shift":
            self.id_input = QLineEdit()
            self.name_input = QLineEdit()
            self.in_time_input = QTimeEdit()
            self.out_time_input = QTimeEdit()
            
            self.in_time_input.setDisplayFormat("HH:mm")
            self.out_time_input.setDisplayFormat("HH:mm")
            self.in_time_input.setTime(time(9, 0))  # Default 9:00 AM
            self.out_time_input.setTime(time(18, 0))  # Default 6:00 PM
            
            form_layout.addRow("Shift ID:", self.id_input)
            form_layout.addRow("Shift Name:", self.name_input)
            form_layout.addRow("In Time:", self.in_time_input)
            form_layout.addRow("Out Time:", self.out_time_input)
            
        elif self.data_type == "Holiday":
            self.id_input = QLineEdit()
            self.name_input = QLineEdit()
            self.date_input = QDateEdit()
            
            self.date_input.setDate(QDate.currentDate())
            self.date_input.setCalendarPopup(True)
            
            form_layout.addRow("Holiday ID:", self.id_input)
            form_layout.addRow("Holiday Name:", self.name_input)
            form_layout.addRow("Date:", self.date_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save_item)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def save_item(self):
        """Save the new item"""
        try:
            if self.data_type == "Department":
                if not self.id_input.text().strip() or not self.name_input.text().strip():
                    QMessageBox.warning(self, "Warning", "Please fill in all fields")
                    return
                    
                dept = Department(
                    department_id=self.id_input.text().strip(),
                    department_name=self.name_input.text().strip()
                )
                success = self.master_repo.create_department(dept)
                
            elif self.data_type == "Designation":
                if not self.id_input.text().strip() or not self.name_input.text().strip() or not self.dept_combo.currentData():
                    QMessageBox.warning(self, "Warning", "Please fill in all fields")
                    return
                    
                des = Designation(
                    designation_id=self.id_input.text().strip(),
                    designation_name=self.name_input.text().strip(),
                    department_id=self.dept_combo.currentData()
                )
                success = self.master_repo.create_designation(des)
                
            elif self.data_type == "Branch":
                if not self.id_input.text().strip() or not self.name_input.text().strip():
                    QMessageBox.warning(self, "Warning", "Please fill in required fields")
                    return
                    
                branch = Branch(
                    branch_id=self.id_input.text().strip(),
                    name=self.name_input.text().strip(),
                    branch_address=self.address_input.text().strip(),
                    phone_number=self.phone_input.text().strip()
                )
                success = self.master_repo.create_branch(branch)
                
            elif self.data_type == "Shift":
                if not self.id_input.text().strip() or not self.name_input.text().strip():
                    QMessageBox.warning(self, "Warning", "Please fill in required fields")
                    return
                    
                shift = Shift(
                    shift_id=self.id_input.text().strip(),
                    shift_name=self.name_input.text().strip(),
                    in_time=self.in_time_input.time().toString("HH:mm"),
                    out_time=self.out_time_input.time().toString("HH:mm")
                )
                success = self.master_repo.create_shift(shift)
                
            elif self.data_type == "Holiday":
                if not self.id_input.text().strip() or not self.name_input.text().strip():
                    QMessageBox.warning(self, "Warning", "Please fill in required fields")
                    return
                    
                holiday = Holiday(
                    holiday_id=self.id_input.text().strip(),
                    holiday_name=self.name_input.text().strip(),
                    holiday_date=self.date_input.date().toPython()
                )
                success = self.master_repo.create_holiday(holiday)
            else:
                success = False
            
            if success:
                QMessageBox.information(self, "Success", f"{self.data_type} added successfully")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", f"Failed to add {self.data_type.lower()}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving item: {str(e)}")
