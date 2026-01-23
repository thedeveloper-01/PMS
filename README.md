# PayMaster - Modern Payroll Management System

A professional, enterprise-grade desktop Payroll Management System built with **Python**, **PySide6 (Qt)**, and **MongoDB**. 
Featuring a **Premium Slate UI**, robust role-based security, and automated statutory calculations.

## 🚀 Key Features

### 🎨 Modern User Experience
-   **Premium Slate Design**: A sleek, dark-themed interface with glassmorphism effects, gradient cards, and high-contrast typography.
-   **Responsive Layouts**: Fully responsive tables and dashboards that auto-adjust to any window size (no fixed sizing issues).
-   **Visual Dashboard**: Interactive main dashboard with real-time statistics, gradient indicator cards, and large actionable metrics.

### 👥 HR & Employee Management
-   **Role-Based Access**: Secure login for Admin, HR, and Employee roles with granular permission control.
-   **Employee Directory**: Comprehensive CRUD operations for employee records including salary details, department, and designations.
-   **Master Data**: Manage Departments, Designations, Branches, Shifts, and Holidays via a unified interface.

### 📅 Attendance & Payroll
-   **Smart Attendance**: Track daily Check-in/Check-out times and status (Present, Absent, LOP).
-   **Automated Payroll**: One-click payroll processing with auto-calculation of:
    -   **Earnings**: Basic, HRA (40%), DA (20%), Allowances.
    -   **Deductions**: PF (12%), ESI (0.75%), Professional Tax (Slab-based), and Loss of Pay (LOP).
-   **Payslip Generation**: Automatic PDF payslip generation using ReportLab.

### 📊 Reporting
-   **Excel Exports**: Export detailed employee lists and payroll register reports to Excel.
-   **Analytics**: Visual reports on department distribution and salary trends.

---

## 🛠️ Technology Stack

-   **Frontend**: Python 3.10+ with [PySide6](https://pypi.org/project/PySide6/) (Qt for Python)
-   **Backend**: [MongoDB](https://www.mongodb.com/) (NoSQL Database)
-   **Driver**: PyMongo
-   **Reporting**: ReportLab (PDF), OpenPyXL (Excel)

---

## ⚙️ Installation & Setup

### Prerequisites
1.  **Python 3.10** or higher.
2.  **MongoDB Community Server** (installed and running locally or via Atlas).

### Quick Start

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/payroll-system.git
    cd payroll-system
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Database**
    -   By default, the app looks for a local MongoDB instance at `localhost:27017`.
    -   To use a cloud database, set the environment variable:
        ```powershell
        $env:MONGODB_URI="mongodb+srv://<user>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority"
        ```

4.  **Run the Application**
    ```bash
    python -m payroll_system
    ```

5.  **First Login**
    -   **Email**: `admin@payroll.com`
    -   **Password**: `admin123`

---

## 📂 Project Architecture

The application follows a clean **Service-Repository Pattern**:

```
payroll_system/
├── gui/                    # Presentation Layer (PySide6 Widgets)
│   ├── main_window.py      # Main Navigation & Layout
│   ├── dashboard.py        # Modern Dashboard with Gradient Cards
│   ├── theme.py            # Centralized Design System (QSS)
│   └── ...                 # Feature Widgets
├── services/               # Business Logic Layer
│   ├── payroll_calculator.py # Core tax & salary logic
│   └── ...
├── repository/             # Data Access Layer (MongoDB)
│   └── ...
├── models/                 # Data Models (Pydantic style classes)
├── reports/                # PDF & Excel Generators
└── utils/                  # Database & Helpers
```

---

## 📝 Configuration

You can fine-tune application settings in `payroll_system/config.py`:
-   **Statutory Rates**: Adjust PF (12%), ESI (0.75%) rates.
-   **PT Slabs**: Configure Professional Tax brackets.
-   **Role Constants**: Define system roles.

---

## 📄 License

This project is open-source and available under the **MIT License**.
