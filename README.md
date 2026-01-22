# Payroll Management System

A complete desktop Payroll Management System built with Python, PySide6 (Qt), and MongoDB.

## Features

- **Role-based Access Control**: Admin, HR, and Employee roles with different permissions
- **Employee Management**: Add, edit, search, and delete employees
- **Master Data Management**: Departments, Designations, Branches, Shifts, and Holidays
- **Attendance Management**: Mark attendance, track check-in/check-out, LOP (Loss of Pay)
- **Payroll Calculation**: Automatic calculation with statutory deductions (PF, ESI, PT)
- **Payslip Generation**: Generate PDF payslips using ReportLab
- **Excel Export**: Export payroll reports and employee lists to Excel
- **Dashboard**: Overview with statistics and key metrics

## Technology Stack

- **Python 3.10+**
- **PySide6**: GUI framework
- **MongoDB**: Database (via PyMongo)
- **ReportLab**: PDF generation
- **openpyxl**: Excel export

## Installation

1. **Install Python 3.10 or higher**

2. **Install MongoDB**
   - Download and install MongoDB from https://www.mongodb.com/try/download/community
   - Start MongoDB service

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit `payroll_system/config.py` to configure:
- MongoDB connection settings (host, port, database name)
- Statutory deduction rates (PF, ESI, PT)
- Application settings

## Running the Application

1. **Configure MongoDB**

- **Local MongoDB**: nothing special needed (defaults to `localhost:27017`).
- **MongoDB Atlas (recommended)**: set `MONGODB_URI` (do not hardcode credentials in code).

PowerShell example:

```bash
$env:MONGODB_URI="mongodb+srv://<user>:<pass>@<cluster>/?retryWrites=true&w=majority"
$env:MONGODB_DB_NAME="payroll_management"
```

2. **Run the application**
   ```bash
   python -m payroll_system
   ```

3. **Default Login Credentials**
   - Email: `admin@payroll.com`
   - Password: `admin123`

## Project Structure

```
payroll_system/
├── gui/                    # GUI components
│   ├── login_window.py    # Login screen
│   ├── main_window.py     # Main application window
│   ├── dashboard.py       # Dashboard widget
│   ├── employee_management.py
│   ├── attendance_management.py
│   ├── payroll_management.py
│   ├── reports_widget.py
│   └── master_data_widgets.py
├── services/              # Business logic layer
│   ├── employee_service.py
│   ├── attendance_service.py
│   ├── payroll_service.py
│   └── payroll_calculator.py
├── repository/            # Data access layer
│   ├── employee_repository.py
│   ├── attendance_repository.py
│   ├── payroll_repository.py
│   └── master_data_repository.py
├── models/                # Data models
│   ├── employee.py
│   ├── attendance.py
│   ├── payroll.py
│   └── master_data.py
├── reports/               # Report generation
│   ├── payslip_generator.py
│   └── excel_export.py
├── utils/                 # Utilities
│   ├── database.py
│   └── validators.py
├── config.py             # Configuration
└── main.py               # Application entry point
```

## Features Details

### Payroll Calculation

The system automatically calculates:
- **Earnings**: Basic Salary, HRA (40%), DA (20%), Allowances (10%), Bonus, Overtime Pay
- **Deductions**: 
  - PF (Provident Fund): 12% of basic salary (capped at ₹1800)
  - ESI (Employee State Insurance): 0.75% of gross salary (if applicable)
  - PT (Professional Tax): Based on salary slabs
  - LOP (Loss of Pay) deductions

### Statutory Deductions

- **PF Rate**: 12% of basic salary (configurable in `config.py`)
- **ESI Rate**: 0.75% of gross salary for salaries below ₹21,000
- **PT Slabs**:
  - ₹0 - ₹5,999: ₹0
  - ₹6,000 - ₹8,999: ₹80
  - ₹9,000 - ₹11,999: ₹150
  - ₹12,000+: ₹200

## Usage

1. **Login**: Use admin credentials to access the system
2. **Add Master Data**: Set up Departments, Designations, Branches, and Shifts
3. **Add Employees**: Create employee records with salary information
4. **Mark Attendance**: Record daily attendance for employees
5. **Generate Payroll**: Calculate monthly payroll with automatic deductions
6. **Generate Payslips**: Create PDF payslips for employees
7. **Export Reports**: Export payroll data to Excel

## Notes

- All data is stored in MongoDB
- Payslips are saved in `payroll_system/reports/payslips/`
- Excel exports are saved in `payroll_system/reports/exports/`
- Logs are written to `payroll_system.log`

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions, please check the logs in `payroll_system.log` for detailed error messages.

