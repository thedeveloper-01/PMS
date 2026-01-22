
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QDateEdit, QComboBox, QMessageBox, QDialog,
                              QFormLayout, QTimeEdit, QHeaderView)
from PySide6.QtCore import Qt, QDate, QTime
from PySide6.QtGui import QFont
from payroll_system.services.attendance_service import AttendanceService
from payroll_system.services.employee_service import EmployeeService
from datetime import date, time

class AttendanceManagementWidget(QWidget):
    """Attendance management widget"""
    
    def __init__(self):
        super().__init__()
        self.attendance_service = AttendanceService()
        self.employee_service = EmployeeService()
        self.init_ui()
    
    def refresh_data(self):
        """Refresh data when tab is active"""
        self.load_employees()
        # Optionally reload table if inputs are set
        if self.employee_combo.currentData():
            self.view_attendance()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(32, 24, 32, 24)
        
        # Header
        header = QLabel("Attendance Management")
        header.setObjectName("PageTitle")
        layout.addWidget(header)
        
        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(12)
        
        # Employee filter
        toolbar.addWidget(QLabel("Employee:"))
        self.employee_combo = QComboBox()
        self.load_employees()
        self.employee_combo.setMinimumWidth(200)
        toolbar.addWidget(self.employee_combo)
        
        # Date filter
        toolbar.addWidget(QLabel("Date:"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setMinimumWidth(150)
        toolbar.addWidget(self.date_input)
        
        toolbar.addStretch()
        
        # Action buttons
        view_btn = QPushButton("📊 View Attendance")
        view_btn.clicked.connect(self.view_attendance)
        toolbar.addWidget(view_btn)
        
        mark_btn = QPushButton("✓ Mark Attendance")
        mark_btn.setObjectName("PrimaryButton")
        mark_btn.clicked.connect(self.mark_attendance)
        toolbar.addWidget(mark_btn)
        
        layout.addLayout(toolbar)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Date", "Check-in", "Check-out", "Status", "Actions"
        ])
        
        # Table styling
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(70)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Header resize policies
        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        self.table.setColumnWidth(4, 250)
        
        header.setDefaultAlignment(Qt.AlignLeft)
        
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_employees(self):
        """Load employees into combo"""
        current_id = self.employee_combo.currentData()
        employees = self.employee_service.get_all_employees(status=1)
        self.employee_combo.clear()
        self.employee_combo.addItem("Select Employee", None)
        
        index_to_set = 0
        for i, emp in enumerate(employees):
            self.employee_combo.addItem(f"{emp.employee_id} - {emp.employee_name}", emp.employee_id)
            if current_id and emp.employee_id == current_id:
                index_to_set = i + 1  # +1 because of "Select Employee" item
        
        if index_to_set > 0:
            self.employee_combo.setCurrentIndex(index_to_set)
    
    def mark_attendance(self):
        """Open mark attendance dialog"""
        employee_id = self.employee_combo.currentData()
        if not employee_id:
            QMessageBox.warning(self, "Warning", "Please select an employee")
            return
        
        dialog = MarkAttendanceDialog(self, employee_id, self.date_input.date().toPython())
        if dialog.exec() == QDialog.Accepted:
            self.view_attendance()
    
    def view_attendance(self):
        """View attendance records"""
        employee_id = self.employee_combo.currentData()
        if not employee_id:
            QMessageBox.warning(self, "Warning", "Please select an employee")
            return
        
        try:
            selected_date = self.date_input.date().toPython()
            month = selected_date.month
            year = selected_date.year
            
            attendances = self.attendance_service.get_monthly_attendance(employee_id, month, year)
            
            self.table.setRowCount(len(attendances))
            for row, att in enumerate(attendances):
                from datetime import datetime as dt
                if isinstance(att.date, str):
                    att_date = dt.strptime(att.date, '%Y-%m-%d').date()
                else:
                    att_date = att.date
                self.table.setItem(row, 0, QTableWidgetItem(str(att_date)))
                self.table.setItem(row, 1, QTableWidgetItem(
                    str(att.checkin_time) if att.checkin_time else "N/A"
                ))
                self.table.setItem(row, 2, QTableWidgetItem(
                    str(att.checkout_time) if att.checkout_time else "N/A"
                ))
                
                # Status with styling
                status_item = QTableWidgetItem(att.status)
                if att.status == "Present":
                    status_item.setForeground(Qt.green)
                elif att.status == "Absent":
                    status_item.setForeground(Qt.red)
                elif att.status == "LOP":
                    status_item.setForeground(Qt.yellow)
                self.table.setItem(row, 3, status_item)
                
                # Action buttons
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(5, 0, 5, 0)
                actions_layout.setSpacing(12)
                actions_layout.setAlignment(Qt.AlignCenter)
                
                if att.status != "LOP":
                    lop_btn = QPushButton("Mark Loss")
                    lop_btn.setCursor(Qt.PointingHandCursor)
                    lop_btn.setObjectName("WarningButton")
                    lop_btn.setFixedSize(100, 32) # Standardize size
                    lop_btn.clicked.connect(lambda checked, eid=employee_id, d=att_date: 
                                           self.mark_lop(eid, d))
                    actions_layout.addWidget(lop_btn)
                
                # Delete button
                delete_btn = QPushButton("Del")
                delete_btn.setToolTip("Delete Record")
                delete_btn.setFixedSize(60, 32)
                delete_btn.setCursor(Qt.PointingHandCursor)
                delete_btn.setObjectName("DangerButton")
                delete_btn.clicked.connect(lambda checked, eid=employee_id, d=att_date: 
                                           self.delete_attendance(eid, d))
                actions_layout.addWidget(delete_btn)
                
                self.table.setCellWidget(row, 4, actions_widget)
                
            # self.table.resizeColumnsToContents() # Removed to prevent layout collapse
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading attendance: {str(e)}")
    
    def mark_lop(self, employee_id: str, att_date: date):
        """Mark Loss of Pay"""
        reply = QMessageBox.question(
            self, "Confirm LOP",
            f"Mark Loss of Pay for {att_date}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.attendance_service.mark_lop(employee_id, att_date)
            if success:
                QMessageBox.information(self, "Success", "LOP marked successfully")
                self.view_attendance()
            else:
                QMessageBox.critical(self, "Error", "Failed to mark LOP")
    
    def delete_attendance(self, employee_id: str, att_date: date):
        """Delete attendance record"""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete attendance record for {att_date}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.attendance_service.delete_attendance(employee_id, att_date)
            if success:
                QMessageBox.information(self, "Success", "Attendance record deleted")
                self.view_attendance()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete record")

class MarkAttendanceDialog(QDialog):
    """Mark attendance dialog"""
    
    def __init__(self, parent, employee_id: str, att_date: date):
        super().__init__(parent)
        self.employee_id = employee_id
        self.att_date = att_date
        self.attendance_service = AttendanceService()
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog"""
        self.setWindowTitle("Mark Attendance")
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        layout.setSpacing(15)
        
        # Date display
        date_label = QLabel(f"Date: {self.att_date}")
        date_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addRow(date_label)
        
        # Time inputs
        self.checkin_time = QTimeEdit()
        self.checkin_time.setTime(QTime(9, 0))  # Default 9:00 AM
        self.checkin_time.setDisplayFormat("HH:mm")
        layout.addRow("Check-in Time:", self.checkin_time)
        
        self.checkout_time = QTimeEdit()
        self.checkout_time.setTime(QTime(18, 0))  # Default 6:00 PM
        self.checkout_time.setDisplayFormat("HH:mm")
        layout.addRow("Check-out Time:", self.checkout_time)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("💾 Save")
        save_btn.setObjectName("PrimaryButton")
        save_btn.clicked.connect(self.save_attendance)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addRow(button_layout)
        self.setLayout(layout)
    
    def save_attendance(self):
        """Save attendance"""
        try:
            checkin = self.checkin_time.time().toPython()
            checkout = self.checkout_time.time().toPython()
            
            if checkout < checkin:
                QMessageBox.warning(self, "Warning", "Check-out time must be after check-in time")
                return
            
            success = self.attendance_service.mark_attendance(
                self.employee_id, self.att_date, checkin, checkout
            )
            
            if success:
                QMessageBox.information(self, "Success", "Attendance marked successfully")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to mark attendance")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
