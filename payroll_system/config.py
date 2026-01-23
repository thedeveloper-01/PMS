"""
Configuration settings for the Payroll Management System
"""
import os
import sys
from pathlib import Path

# MongoDB Configuration
# Prefer a full MongoDB URI (supports Atlas SRV, auth, options), otherwise fall back to host/port.
#
# NOTE: You asked to hardcode the online MongoDB URL. This is convenient for demos,
# but you should rotate credentials if this repo is shared publicly.
#
# Examples:
# - mongodb://localhost:27017
# - mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://vr8120168439_db_user:PIqMgLhdWX5vCXBs@pms.oyk9ywl.mongodb.net/?appName=PMS",
).strip()
MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
MONGODB_PORT = int(os.getenv("MONGODB_PORT", 27017))
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "payroll_management")

# Application Configuration
APP_NAME = "Payroll Management System"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# If set to 1, the app will reset the default admin password on startup.
# (Handy if you changed it or imported old data.)
RESET_DEFAULT_ADMIN = os.getenv("RESET_DEFAULT_ADMIN", "0").strip() == "1"

# Statutory Deduction Rates (Indian context - can be customized)
PF_RATE = 0.12  # 12% of basic salary
ESI_RATE = 0.0075  # 0.75% of gross salary (if applicable)
PT_SLABS = {
    (0, 5999): 0,
    (6000, 8999): 80,
    (9000, 11999): 150,
    (12000, float('inf')): 200
}

# File Paths
BASE_DIR = Path(__file__).parent
REPORTS_DIR = BASE_DIR / "reports"
PAYSLIPS_DIR = REPORTS_DIR / "payslips"
EXPORTS_DIR = REPORTS_DIR / "exports"

# Create directories if they don't exist
REPORTS_DIR.mkdir(exist_ok=True)
PAYSLIPS_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)

# Role Codes
ROLE_ADMIN = 1
ROLE_HR = 2
ROLE_EMPLOYEE = 3

ROLE_NAMES = {
    ROLE_ADMIN: "Admin",
    ROLE_HR: "HR",
    ROLE_EMPLOYEE: "Employee"
}


# Resource helper
def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = BASE_DIR

    return str(Path(base_path) / relative_path)
