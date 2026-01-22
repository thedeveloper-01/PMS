"""
Attendance management widget
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QDateEdit, QComboBox, QMessageBox, QDialog,
                              QFormLayout, QTimeEdit)
from PySide6.QtCore import Qt, QDate
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
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Attendance Management")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Filter
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Employee:"))
        self.employee_combo = QComboBox()
        self.load_employees()
        filter_layout.addWidget(self.employee_combo)
        
        filter_layout.addWidget(QLabel("Date:"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        filter_layout.addWidget(self.date_input)
        
        mark_btn = QPushButton("Mark Attendance")
        mark_btn.clicked.connect(self.mark_attendance)
        filter_layout.addWidget(mark_btn)
        
        view_btn = QPushButton("View Attendance")
        view_btn.clicked.connect(self.view_attendance)
        filter_layout.addWidget(view_btn)
        
        header_layout.addLayout(filter_layout)
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Date", "Check-in", "Check-out", "Status", "Actions"
        ])
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_employees(self):
        """Load employees into combo"""
        employees = self.employee_service.get_all_employees(status=1)
        self.employee_combo.clear()
        self.employee_combo.addItem("Select Employee", None)
        for emp in employees:
            self.employee_combo.addItem(f"{emp.employee_id} - {emp.employee_name}", emp.employee_id)
    
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
                self.table.setItem(row, 3, QTableWidgetItem(att.status))
                
                # Mark LOP button
                lop_btn = QPushButton("Mark LOP")
                lop_btn.clicked.connect(lambda checked, eid=employee_id, d=att_date: 
                                       self.mark_lop(eid, d))
                self.table.setCellWidget(row, 4, lop_btn)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading attendance: {str(e)}")
    
    def mark_lop(self, employee_id: str, att_date: date):
        """Mark Loss of Pay"""
        success = self.attendance_service.mark_lop(employee_id, att_date)
        if success:
            QMessageBox.information(self, "Success", "LOP marked successfully")
            self.view_attendance()
        else:
            QMessageBox.critical(self, "Error", "Failed to mark LOP")

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
        layout = QFormLayout()
        
        from PySide6.QtCore import QTime
        self.checkin_time = QTimeEdit()
        self.checkin_time.setTime(QTime.currentTime())
        layout.addRow("Check-in Time:", self.checkin_time)
        
        self.checkout_time = QTimeEdit()
        self.checkout_time.setTime(QTime.currentTime())
        layout.addRow("Check-out Time:", self.checkout_time)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("Save")
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

