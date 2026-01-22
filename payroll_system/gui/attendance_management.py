"""
Attendance management widget
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QDateEdit, QComboBox, QMessageBox, QDialog,
                              QFormLayout, QTimeEdit, QFrame, QListWidget, QListWidgetItem)
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
        layout.setSpacing(14)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Attendance Management")
        title.setObjectName("PageTitle")
        subtitle = QLabel("Dashboard > Attendance")
        subtitle.setObjectName("PageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # KPI row (like screenshot)
        kpis = QHBoxLayout()
        kpis.setSpacing(16)
        self.kpi_present = self._kpi("Total Present", "0/0", "↑ +0%")
        self.kpi_late = self._kpi("Total Late", "0", "↑ +0%")
        self.kpi_pending = self._kpi("Pending Leave Requests", "0", "Review Now")
        kpis.addWidget(self.kpi_present)
        kpis.addWidget(self.kpi_late)
        kpis.addWidget(self.kpi_pending)
        layout.addLayout(kpis)

        # Main split layout (calendar placeholder + list)
        split = QHBoxLayout()
        split.setSpacing(16)

        left = QFrame()
        left.setObjectName("Card")
        left_l = QVBoxLayout()
        left_l.setContentsMargins(16, 16, 16, 16)
        left_l.setSpacing(10)
        h = QLabel("Attendance Overview")
        h.setStyleSheet("font-size: 16px; font-weight: 800;")
        left_l.addWidget(h)
        cal_hint = QLabel("(Calendar-style overview placeholder)")
        cal_hint.setStyleSheet("color: #92a4c9; font-size: 12px;")
        left_l.addWidget(cal_hint)

        # Keep existing controls inside a compact row
        controls = QFrame()
        controls.setObjectName("CardAlt")
        c = QHBoxLayout()
        c.setContentsMargins(12, 12, 12, 12)
        c.setSpacing(10)
        self.employee_combo = QComboBox()
        self.load_employees()
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        mark_btn = QPushButton("Mark Attendance")
        mark_btn.setObjectName("PrimaryButton")
        mark_btn.clicked.connect(self.mark_attendance)
        view_btn = QPushButton("View")
        view_btn.clicked.connect(self.view_attendance)
        c.addWidget(QLabel("Employee:"))
        c.addWidget(self.employee_combo, 1)
        c.addWidget(QLabel("Month:"))
        c.addWidget(self.date_input)
        c.addWidget(mark_btn)
        c.addWidget(view_btn)
        controls.setLayout(c)
        left_l.addWidget(controls)

        # A simple month grid placeholder (we'll keep table as data view)
        placeholder = QFrame()
        placeholder.setObjectName("CardAlt")
        ph = QVBoxLayout()
        ph.setContentsMargins(16, 16, 16, 16)
        ph.addWidget(QLabel("Tip: use the table on the right to mark LOP / view records."))
        ph.addStretch()
        placeholder.setLayout(ph)
        left_l.addWidget(placeholder, 1)
        left.setLayout(left_l)

        right = QFrame()
        right.setObjectName("Card")
        right_l = QVBoxLayout()
        right_l.setContentsMargins(16, 16, 16, 16)
        right_l.setSpacing(10)
        rh = QLabel("This Month")
        rh.setStyleSheet("font-size: 16px; font-weight: 800;")
        right_l.addWidget(rh)

        # Table (existing)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Check-in", "Check-out", "Status", "Actions"])
        self.table.horizontalHeader().setStretchLastSection(True)
        right_l.addWidget(self.table, 1)
        right.setLayout(right_l)

        split.addWidget(left, 2)
        split.addWidget(right, 1)
        layout.addLayout(split, 1)
        
        self.setLayout(layout)

    def _kpi(self, title: str, value: str, badge: str) -> QFrame:
        card = QFrame()
        card.setObjectName("Card")
        l = QVBoxLayout()
        l.setContentsMargins(16, 16, 16, 16)
        l.setSpacing(6)
        t = QLabel(title)
        t.setStyleSheet("color: #92a4c9; font-size: 12px; font-weight: 700;")
        v = QLabel(value)
        v.setObjectName("KpiValue")
        v.setStyleSheet("font-size: 28px; font-weight: 900;")
        b = QLabel(badge)
        b.setStyleSheet("color: #92a4c9; font-size: 11px; font-weight: 700;")
        l.addWidget(t)
        l.addWidget(v)
        l.addWidget(b)
        l.addStretch()
        card.setLayout(l)
        return card
    
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

            # Update KPIs for the selected employee+month
            summary = self.attendance_service.calculate_attendance_summary(employee_id, month, year)
            self._set_kpi_value(self.kpi_present, f"{summary['present_days']}/{summary['total_days']}")
            self._set_kpi_value(self.kpi_late, "0")  # late tracking not implemented yet
            self._set_kpi_value(self.kpi_pending, "0")  # leave workflow not implemented yet
            
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

    def _set_kpi_value(self, card: QFrame, value: str) -> None:
        lay = card.layout()
        if not lay:
            return
        for i in range(lay.count()):
            w = lay.itemAt(i).widget()
            if isinstance(w, QLabel) and w.objectName() == "KpiValue":
                w.setText(value)
                return
    
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

