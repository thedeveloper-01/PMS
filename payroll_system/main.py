"""
Main entry point for the Payroll Management System
"""
import sys
from pathlib import Path
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# Allow running as: `python payroll_system/main.py` (from repo root)
# Without this, `import payroll_system...` may fail because the repo root may
# not be on sys.path when executing a file inside the package directory.
_THIS_FILE = Path(__file__).resolve()
_REPO_ROOT = _THIS_FILE.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from payroll_system.gui.login_window import LoginWindow
from payroll_system.gui.main_window import MainWindow
from payroll_system.utils.database import db
from payroll_system.config import APP_NAME

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('payroll_system.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def initialize_database():
    """Initialize database connection and create default data"""
    try:
        db.connect()
        logger.info("Database connected successfully")
        
        # Create (or optionally reset) default admin user
        from payroll_system.services.employee_service import EmployeeService
        from payroll_system.models.employee import Employee
        from payroll_system.config import ROLE_ADMIN
        from datetime import datetime
        
        employee_service = EmployeeService()
        ok, msg = employee_service.ensure_default_admin(
            email="admin@payroll.com",
            password="admin123",
            employee_id="ADMIN001",
        )
        if ok:
            logger.info(msg)
        else:
            logger.warning(msg)
        
        # Create default master data if needed
        from payroll_system.repository.master_data_repository import MasterDataRepository
        from payroll_system.models.master_data import Department, Designation, Branch, Shift
        
        master_repo = MasterDataRepository()
        
        # Default department
        if not master_repo.get_all_departments():
            dept = Department("DEPT001", "Administration")
            master_repo.create_department(dept)
        
        # Default branch
        if not master_repo.get_all_branches():
            branch = Branch("BR001", "Main Branch", "123 Main St", "1234567890", "branch@company.com")
            master_repo.create_branch(branch)
        
        # Default shift
        if not master_repo.get_all_shifts():
            shift = Shift("SHIFT001", "General Shift", "09:00:00", "18:00:00")
            master_repo.create_shift(shift)
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def main():
    """Main application entry point"""
    try:
        # Initialize database
        initialize_database()
        
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName(APP_NAME)
        app.setStyle('Fusion')  # Use Fusion style for better cross-platform appearance
        
        # Create and show login window
        login_window = LoginWindow()
        
        def on_login_success(employee):
            """Handle successful login"""
            login_window.close()
            main_window = MainWindow(employee)
            main_window.show()
        
        login_window.login_successful.connect(on_login_success)
        login_window.show()
        
        # Run application
        sys.exit(app.exec())
        
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # Disconnect from database
        db.disconnect()

if __name__ == "__main__":
    main()

