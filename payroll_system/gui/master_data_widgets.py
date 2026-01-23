"""
Master data management widgets
"""
from functools import partial
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QTabWidget, QTableWidget,
                               QTableWidgetItem, QMessageBox, QDialog,
                               QFormLayout, QLineEdit, QDateEdit, QTimeEdit,
                               QDialogButtonBox, QComboBox, QHeaderView, QFrame)
from PySide6.QtCore import Qt, QDate, QTime
from PySide6.QtGui import QFont, QIcon
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
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Master Data Management")
        title.setObjectName("PageTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Configuration for each tab
        # This setup ensures consistent behavior and easy extension
        self.tab_widgets = {}
        
        tab_configs = [
            ("Department", "Departments"),
            ("Designation", "Designations"),
            ("Branch", "Branches"),
            ("Shift", "Shifts"),
            ("Holiday", "Holidays")
        ]
        
        for data_type, title in tab_configs:
            widget = MasterDataTableWidget(data_type, self.master_repo)
            self.tabs.addTab(widget, title)
            self.tab_widgets[data_type] = widget
            
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def refresh_data(self):
        """Refresh data for all tabs"""
        for widget in self.tab_widgets.values():
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
        layout.setSpacing(0)
        layout.setContentsMargins(0, 10, 0, 0)
        
        # --- Card Container ---
        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)
        card_layout.setContentsMargins(15, 15, 15, 15)
        
        # --- Toolbar ---
        toolbar = QHBoxLayout()
        
        title = QLabel(f"{self.data_type} List")
        title.setObjectName("SectionTitle")
        toolbar.addWidget(title)
        
        toolbar.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_data)
        toolbar.addWidget(refresh_btn)
        
        add_btn = QPushButton(f"+ Add {self.data_type}")
        add_btn.setObjectName("PrimaryButton")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.add_item)
        toolbar.addWidget(add_btn)
        
        card_layout.addLayout(toolbar)
        
        # --- Table ---
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(50) # Comfortable height
        
        # Column Configuration
        self.columns = self._get_columns()
        self.table.setColumnCount(len(self.columns) + 1) # +1 for Actions
        self.table.setHorizontalHeaderLabels(self.columns + ["Action"]) # Singular "Action" fits better
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        # Fix Action column width
        header.setSectionResizeMode(len(self.columns), QHeaderView.Fixed)
        self.table.setColumnWidth(len(self.columns), 80) # Widen slightly for header
        
        card_layout.addWidget(self.table)
        
        layout.addWidget(card)
        self.setLayout(layout)
        
    def _get_columns(self):
        """Get column names based on data type"""
        if self.data_type == "Department":
            return ["ID", "Name"]
        elif self.data_type == "Designation":
            return ["ID", "Name", "Department"]
        elif self.data_type == "Branch":
            return ["ID", "Name", "Address", "Phone"]
        elif self.data_type == "Shift":
            return ["ID", "Name", "In Time", "Out Time"]
        elif self.data_type == "Holiday":
            return ["ID", "Name", "Date"]
        return []

    def load_data(self):
        """Load data into table"""
        try:
            items = []
            if self.data_type == "Department":
                items = self.master_repo.get_all_departments()
            elif self.data_type == "Designation":
                items = self.master_repo.get_all_designations()
            elif self.data_type == "Branch":
                items = self.master_repo.get_all_branches()
            elif self.data_type == "Shift":
                items = self.master_repo.get_all_shifts()
            elif self.data_type == "Holiday":
                items = self.master_repo.get_all_holidays()
                
            self.table.setRowCount(len(items))
            self.table.setSortingEnabled(False) 
            
            for row, item in enumerate(items):
                # Helpers to safely get attributes
                def get_val(obj, attr, default=""):
                    return str(getattr(obj, attr, default))
                
                # Fetch Data
                id_val = ""
                data = []
                
                if self.data_type == "Department":
                    id_val = item.department_id
                    data = [item.department_id, item.department_name]
                    
                elif self.data_type == "Designation":
                    id_val = item.designation_id
                    data = [item.designation_id, item.designation_name, getattr(item, 'department_name', 'N/A')]
                    
                elif self.data_type == "Branch":
                    id_val = item.branch_id
                    data = [item.branch_id, item.name, item.branch_address, item.phone_number]
                    
                elif self.data_type == "Shift":
                    id_val = item.shift_id
                    data = [item.shift_id, item.shift_name, item.in_time, item.out_time]
                    
                elif self.data_type == "Holiday":
                    id_val = item.holiday_id
                    date_val = item.holiday_date.isoformat() if hasattr(item.holiday_date, 'isoformat') else str(item.holiday_date)
                    data = [item.holiday_id, item.holiday_name, date_val]
                
                # Populate columns
                for col, text in enumerate(data):
                    item_widget = QTableWidgetItem(str(text))
                    item_widget.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    self.table.setItem(row, col, item_widget)
                
                # Action Buttons
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(0, 0, 0, 0)
                actions_layout.setAlignment(Qt.AlignCenter)
                
                # Delete Button (Text, Compact, Refined)
                delete_btn = QPushButton("Del")
                delete_btn.setToolTip(f"Delete {self.data_type}")
                # We won't use DangerButton object name to avoid the big padding from theme
                # We'll set a custom style sheet for this specific sub-component
                delete_btn.setCursor(Qt.PointingHandCursor)
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(239, 68, 68, 0.2); 
                        color: #ef4444;
                        border: 1px solid rgba(239, 68, 68, 0.5);
                        border-radius: 4px;
                        padding: 0px;
                        font-weight: 600;
                        font-size: 11px;
                        min-height: 24px;
                        max-width: 40px;
                        width: 40px;
                    }
                    QPushButton:hover {
                        background-color: rgba(239, 68, 68, 0.8);
                        color: white;
                    }
                """)
                # Use partial to capture specific item_id
                delete_btn.clicked.connect(partial(self.delete_item, id_val))
                
                actions_layout.addWidget(delete_btn)
                
                self.table.setCellWidget(row, len(self.columns), actions_widget)
            
            self.table.setSortingEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading data: {str(e)}")
    
    def add_item(self):
        """Add new item dialog"""
        dialog = MasterDataDialog(self.data_type, self.master_repo, self)
        if dialog.exec() == QDialog.Accepted:
            self.load_data()
    
    def delete_item(self, item_id):
        """Delete item"""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete this {self.data_type.lower()}?\nID: {item_id}",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                success = False
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
                
                if success:
                    QMessageBox.information(self, "Success", f"{self.data_type} deleted successfully")
                    self.load_data()
                else:
                    QMessageBox.warning(self, "Error", f"Failed to delete {self.data_type.lower()}. It may countain dependencies.")
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
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel(f"New {self.data_type}")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        
        # Field definitions
        self.fields = {}
        
        if self.data_type == "Department":
            self.add_field(form_layout, "id", "Department ID")
            self.add_field(form_layout, "name", "Department Name")
            
        elif self.data_type == "Designation":
            self.add_field(form_layout, "id", "Designation ID")
            self.add_field(form_layout, "name", "Designation Name")
            
            self.dept_combo = QComboBox()
            depts = self.master_repo.get_all_departments()
            for d in depts:
                self.dept_combo.addItem(d.department_name, d.department_id)
            form_layout.addRow("Department:", self.dept_combo)
            
        elif self.data_type == "Branch":
            self.add_field(form_layout, "id", "Branch ID")
            self.add_field(form_layout, "name", "Branch Name")
            self.add_field(form_layout, "address", "Address")
            self.add_field(form_layout, "phone", "Phone Number")
            
        elif self.data_type == "Shift":
            self.add_field(form_layout, "id", "Shift ID")
            self.add_field(form_layout, "name", "Shift Name")
            
            self.in_time = QTimeEdit()
            self.in_time.setDisplayFormat("HH:mm")
            self.in_time.setTime(time(9,0))
            form_layout.addRow("In Time:", self.in_time)
            
            self.out_time = QTimeEdit()
            self.out_time.setDisplayFormat("HH:mm")
            self.out_time.setTime(time(18,0))
            form_layout.addRow("Out Time:", self.out_time)
            
        elif self.data_type == "Holiday":
            self.add_field(form_layout, "id", "Holiday ID")
            self.add_field(form_layout, "name", "Holiday Name")
            
            self.date_edit = QDateEdit()
            self.date_edit.setCalendarPopup(True)
            self.date_edit.setDate(QDate.currentDate())
            form_layout.addRow("Date:", self.date_edit)
            
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setObjectName("PrimaryButton")
        save_btn.clicked.connect(self.save_item)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
    def add_field(self, layout, key, label):
        """Helper to add text field"""
        field = QLineEdit()
        layout.addRow(label + ":", field)
        self.fields[key] = field
        
    def save_item(self):
        """Save the new item"""
        try:
            # Common validation
            for key, field in self.fields.items():
                if not field.text().strip():
                    QMessageBox.warning(self, "Validation Error", f"{key.title()} is required.")
                    field.setFocus()
                    return

            success = False
            
            if self.data_type == "Department":
                obj = Department(
                    department_id=self.fields['id'].text().strip(),
                    department_name=self.fields['name'].text().strip()
                )
                success = self.master_repo.create_department(obj)
                
            elif self.data_type == "Designation":
                dept_id = self.dept_combo.currentData()
                if not dept_id:
                     QMessageBox.warning(self, "Validation Error", "Please select a department.")
                     return
                obj = Designation(
                    designation_id=self.fields['id'].text().strip(),
                    designation_name=self.fields['name'].text().strip(),
                    department_id=dept_id
                )
                success = self.master_repo.create_designation(obj)
                
            elif self.data_type == "Branch":
                obj = Branch(
                    branch_id=self.fields['id'].text().strip(),
                    name=self.fields['name'].text().strip(),
                    branch_address=self.fields['address'].text().strip(),
                    phone_number=self.fields['phone'].text().strip()
                )
                success = self.master_repo.create_branch(obj)
                
            elif self.data_type == "Shift":
                obj = Shift(
                    shift_id=self.fields['id'].text().strip(),
                    shift_name=self.fields['name'].text().strip(),
                    in_time=self.in_time.time().toString("HH:mm"),
                    out_time=self.out_time.time().toString("HH:mm")
                )
                success = self.master_repo.create_shift(obj)
                
            elif self.data_type == "Holiday":
                obj = Holiday(
                    holiday_id=self.fields['id'].text().strip(),
                    holiday_name=self.fields['name'].text().strip(),
                    holiday_date=self.date_edit.date().toPython()
                )
                success = self.master_repo.create_holiday(obj)
            
            if success:
                QMessageBox.information(self, "Success", f"{self.data_type} saved successfully.")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", f"Failed to save {self.data_type}. ID might already exist.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")
