"""
Reports widget
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QMessageBox, QFileDialog)
from PySide6.QtGui import QFont
from payroll_system.services.employee_service import EmployeeService
from payroll_system.reports.excel_export import ExcelExporter

class ReportsWidget(QWidget):
    """Reports widget"""
    
    def __init__(self):
        super().__init__()
        self.employee_service = EmployeeService()
        self.excel_exporter = ExcelExporter()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Reports")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Export buttons
        export_layout = QVBoxLayout()
        export_layout.setSpacing(15)
        
        employee_list_btn = QPushButton("Export Employee List to Excel")
        employee_list_btn.setMinimumHeight(50)
        employee_list_btn.clicked.connect(self.export_employee_list)
        export_layout.addWidget(employee_list_btn)
        
        layout.addLayout(export_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def export_employee_list(self):
        """Export employee list to Excel"""
        try:
            employees = self.employee_service.get_all_employees(status=1)
            if not employees:
                QMessageBox.warning(self, "Warning", "No employees found")
                return
            
            filepath = self.excel_exporter.export_employee_list(employees)
            QMessageBox.information(self, "Success", f"Employee list exported to:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exporting: {str(e)}")

