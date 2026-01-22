
"""
Main window with sidebar navigation
"""
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QMessageBox,
    QFrame,
    QLineEdit,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon
from payroll_system.models.employee import Employee
from payroll_system.config import ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE, ROLE_NAMES
from payroll_system.gui.dashboard import DashboardWidget
from payroll_system.gui.employee_management import EmployeeManagementWidget
from payroll_system.gui.attendance_management import AttendanceManagementWidget
from payroll_system.gui.payroll_management import PayrollManagementWidget
from payroll_system.gui.reports_widget import ReportsWidget
from payroll_system.gui.master_data_widgets import MasterDataWidget

from typing import Dict, List, Tuple


class NavButton(QPushButton):
    """Sidebar navigation button with an 'active' property for QSS styling."""

    def __init__(self, text: str, icon: str = "", parent: QWidget | None = None):
        super().__init__(text, parent)
        self.setObjectName("NavButton")
        self.setProperty("active", False)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(False)
        
        # Set icon if provided
        if icon:
            self.setText(f"{icon}  {text}")

    def set_active(self, active: bool) -> None:
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


from PySide6.QtWidgets import QStackedWidget, QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup

class FadingStackedWidget(QStackedWidget):
    """QStackedWidget with fade transition"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fade_anim = None
        
    def setCurrentIndex(self, index: int):
        """Fade to new index"""
        current_idx = self.currentIndex()
        if current_idx == index:
            return
            
        # Get current and next widgets
        current_widget = self.widget(current_idx)
        next_widget = self.widget(index)
        
        if not current_widget or not next_widget:
            super().setCurrentIndex(index)
            return

        # Ensure next widget is visible and sized correctly (but under current)
        next_widget.setVisible(True)
        next_widget.raise_() 
        # Actually in StackedWidget, raise_() makes it the active one.
        # We want to cross-fade.
        
        # Simplified approach to avoid Painter strictness:
        # Just animate opacity of current out, then switch, then animate new in?
        # That's sequential and might flicker.
        
        # Better robust approach: 
        # 0. Cancel any running animation
        if self.fade_anim and self.fade_anim.state() == QPropertyAnimation.Running:
             self.fade_anim.stop()

        # 1. Setup effects
        effect_out = QGraphicsOpacityEffect(current_widget)
        current_widget.setGraphicsEffect(effect_out)
        
        effect_in = QGraphicsOpacityEffect(next_widget)
        next_widget.setGraphicsEffect(effect_in)
        next_widget.setVisible(True)
        
        # 2. Animations
        anim_out = QPropertyAnimation(effect_out, b"opacity")
        anim_out.setDuration(250)
        anim_out.setStartValue(1.0)
        anim_out.setEndValue(0.0)
        
        anim_in = QPropertyAnimation(effect_in, b"opacity")
        anim_in.setDuration(250)
        anim_in.setStartValue(0.0)
        anim_in.setEndValue(1.0)
        
        # 3. Group
        group = QParallelAnimationGroup(self)
        group.addAnimation(anim_out)
        group.addAnimation(anim_in)
        
        def on_finished():
            # Clean up
            super(FadingStackedWidget, self).setCurrentIndex(index)
            current_widget.graphicsEffect().setEnabled(False) # Disable effect to free painter
            next_widget.graphicsEffect().setEnabled(False)
            current_widget.setGraphicsEffect(None) # Remove correctly
            next_widget.setGraphicsEffect(None)
            
        group.finished.connect(on_finished)
        self.fade_anim = group
        self.fade_anim.start()

        # Hack: StackedWidget insists on showing only one. 
        # To show both during animation, we might need to bypass it or toggle quickly.
        # Standard QStackedWidget isn't built for cross-fading children easily.
        # A safer fallback if this causes issues:
        super().setCurrentIndex(index) # Just switch immediately if complex.
        
        # ACTUALLY, the "Painter not active" is usually because we are trying to paint on a widget
        # that isn't fully ready or in a weird state.
        
        # Let's try a safer Sequential transition (Fade Out -> Switch -> Fade In)
        # This completely avoids 2 widgets painting at once.
        pass

    def setCurrentIndex(self, index: int):
        """Fade Out -> Switch -> Fade In sequence to avoid Painter errors"""
        # Stop any running animation and cleanup
        if self.fade_anim and self.fade_anim.state() == QPropertyAnimation.Running:
            self.fade_anim.stop()
        
        # Ensure all widgets are clean (opacity 1, no effects)
        for i in range(self.count()):
            widget = self.widget(i)
            if widget and widget.graphicsEffect():
                widget.setGraphicsEffect(None)
                
        current_idx = self.currentIndex()
        if current_idx == index:
            return
            
        current_widget = self.widget(current_idx)
        next_widget = self.widget(index)

        # Step 1: Fade Out Current
        effect_out = QGraphicsOpacityEffect(current_widget)
        current_widget.setGraphicsEffect(effect_out)
        anim_out = QPropertyAnimation(effect_out, b"opacity")
        anim_out.setDuration(150)
        anim_out.setStartValue(1.0)
        anim_out.setEndValue(0.0)
        anim_out.setEasingCurve(QEasingCurve.OutQuad)
        
        def switch_page():
            # Step 2: Switch Page
            super(FadingStackedWidget, self).setCurrentIndex(index)
            current_widget.setGraphicsEffect(None) # Clean up previous
            
            # Step 3: Fade In Next
            effect_in = QGraphicsOpacityEffect(next_widget)
            next_widget.setGraphicsEffect(effect_in)
            anim_in = QPropertyAnimation(effect_in, b"opacity")
            anim_in.setDuration(200)
            anim_in.setStartValue(0.0)
            anim_in.setEndValue(1.0)
            anim_in.setEasingCurve(QEasingCurve.InQuad)
            
            def cleanup():
                next_widget.setGraphicsEffect(None)
            
            anim_in.finished.connect(cleanup)
            self.fade_anim = anim_in
            self.fade_anim.start()

        anim_out.finished.connect(switch_page)
        self.fade_anim = anim_out
        self.fade_anim.start()

class MainWindow(QMainWindow):
    """Main application window with navigation"""
    
    def __init__(self, employee: Employee):
        super().__init__()
        self.current_employee = employee
        self._nav_buttons: Dict[int, NavButton] = {}
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("PayMaster - Payroll Management System")
        self.setMinimumSize(1280, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Right side (Topbar + content)
        right = QFrame()
        right.setObjectName("Surface")
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        topbar = self.create_topbar()
        right_layout.addWidget(topbar)

        content_wrap = QFrame()
        content_wrap.setObjectName("Surface")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Content area
        self.stacked_widget = FadingStackedWidget()
        self.stacked_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout.addWidget(self.stacked_widget)
        content_wrap.setLayout(content_layout)

        right_layout.addWidget(content_wrap, 1)
        right.setLayout(right_layout)
        main_layout.addWidget(right, 1)
        
        # Add widgets to stack
        self.dashboard = DashboardWidget(self.current_employee)
        self.employee_mgmt = EmployeeManagementWidget()
        self.attendance_mgmt = AttendanceManagementWidget()
        self.payroll_mgmt = PayrollManagementWidget()
        self.reports = ReportsWidget()
        self.master_data = MasterDataWidget()
        
        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.addWidget(self.employee_mgmt)
        self.stacked_widget.addWidget(self.attendance_mgmt)
        self.stacked_widget.addWidget(self.payroll_mgmt)
        self.stacked_widget.addWidget(self.reports)
        self.stacked_widget.addWidget(self.master_data)
        
        # Show dashboard by default
        self.stacked_widget.setCurrentIndex(0)
        self._set_active_nav(0)
        self._set_title_for_index(0)
        
        central_widget.setLayout(main_layout)
    
    def create_sidebar(self):
        """Create sidebar navigation"""
        sidebar = QFrame()
        sidebar.setStyleSheet("""
            QFrame {
                background: #1e293b;
                border-right: 1px solid rgba(255, 255, 255, 0.08);
            }
        """)
        sidebar.setFixedWidth(300)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Brand section
        brand_frame = QFrame()
        brand_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                padding: 20px 12px;
            }
        """)
        brand_layout = QHBoxLayout(brand_frame)
        brand_layout.setContentsMargins(0, 0, 0, 0)
        brand_layout.setSpacing(12)
        
        # Logo/Icon
        logo_label = QLabel("💰")
        logo_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                background: rgba(59, 130, 246, 0.2);
                border-radius: 12px;
                padding: 6px;
                qproperty-alignment: AlignCenter;
            }
        """)
        logo_label.setFixedSize(50, 50)
        
        # App name and role
        text_frame = QFrame()
        text_frame.setStyleSheet("background: transparent; border: none;")
        text_layout = QVBoxLayout(text_frame)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(4)
        
        app_label = QLabel("PayMaster")
        app_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 800;
                color: #f8fafc;
                background: transparent;
            }
        """)
        
        role_label = QLabel(ROLE_NAMES.get(self.current_employee.role, "Employee"))
        role_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #94a3b8;
                font-weight: 500;
                background: transparent;
            }
        """)
        
        text_layout.addWidget(app_label)
        text_layout.addWidget(role_label)
        
        brand_layout.addWidget(logo_label)
        brand_layout.addWidget(text_frame)
        brand_layout.addStretch()
        
        layout.addWidget(brand_frame)
        
        # Navigation section
        nav_frame = QFrame()
        nav_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
                padding: 20px 16px;
            }
        """)
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(6)
        
        # Navigation buttons based on role
        if self.current_employee.role in [ROLE_ADMIN, ROLE_HR]:
            nav_items = [
                ("📊 Dashboard", 0),
                ("👥 Employees", 1),
                ("✓ Attendance", 2),
                ("💰 Payroll", 3),
                ("📈 Reports", 4),
                ("⚙️ Master Data", 5),
            ]
        else:
            # Employee can only see limited options
            nav_items = [
                ("📊 Dashboard", 0),
                ("✓ Attendance", 2),
                ("💰 Payroll", 3),
            ]
        
        for icon_text, index in nav_items:
            btn = NavButton(icon_text)
            btn.setFixedHeight(48)
            btn.clicked.connect(lambda checked=False, idx=index: self.navigate_to(idx))
            nav_layout.addWidget(btn)
            self._nav_buttons[index] = btn
        
        nav_layout.addStretch()
        layout.addWidget(nav_frame, 1)
        
        # Logout section
        logout_frame = QFrame()
        logout_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border-top: 1px solid rgba(255, 255, 255, 0.08);
                border-right: none;
                padding: 20px;
            }
        """)
        logout_layout = QHBoxLayout(logout_frame)
        logout_layout.setContentsMargins(0, 0, 0, 0)
        
        logout_btn = QPushButton("🚪 Sign Out")
        logout_btn.setObjectName("NavButton") # Re-use generic nav styling for hover
        logout_btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                color: #94a3b8;
                padding: 10px 16px;
                border: 1px solid rgba(255,255,255,0.05);
            }
            QPushButton:hover {
                color: #ef4444;
                background: rgba(239, 68, 68, 0.1);
                border: 1px solid rgba(239, 68, 68, 0.2);
            }
        """)
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.clicked.connect(self.logout)
        logout_layout.addWidget(logout_btn)
        
        layout.addWidget(logout_frame)
        
        sidebar.setLayout(layout)
        return sidebar

    def create_topbar(self) -> QFrame:
        """Top bar (title + search + user)"""
        top = QFrame()
        top.setStyleSheet("""
            QFrame {
                background: #1e293b;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            }
        """)
        top.setFixedHeight(80)
        lay = QHBoxLayout()
        lay.setContentsMargins(32, 0, 32, 0)
        lay.setSpacing(24)

        # Page title
        self.page_title = QLabel("Dashboard Overview")
        self.page_title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 700;
                color: #f8fafc;
                background: transparent;
                border: none;
            }
        """)
        lay.addWidget(self.page_title)

        lay.addStretch()

        # Search bar
        search_frame = QFrame()
        search_frame.setStyleSheet("""
            QFrame {
                background: #0f172a;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
            }
        """)
        search_frame.setFixedHeight(44)
        
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(12, 0, 12, 0)
        search_layout.setSpacing(10)
        
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("color: #64748b; font-size: 14px; background: transparent; border: none;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: #f8fafc;
                font-size: 14px;
                padding: 0;
            }
            QLineEdit::placeholder {
                color: #64748b;
            }
        """)
        self.search_input.setFixedWidth(240)
        
        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input)
        lay.addWidget(search_frame)

        # User info
        user_frame = QFrame()
        user_frame.setStyleSheet("background: transparent; border: none;")
        
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(0, 0, 0, 0)
        user_layout.setSpacing(4)
        user_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        user_name = QLabel(self.current_employee.employee_name)
        user_name.setStyleSheet("color: #f8fafc; font-size: 14px; font-weight: 600; background: transparent;")
        user_name.setAlignment(Qt.AlignRight)
        
        user_role = QLabel(ROLE_NAMES.get(self.current_employee.role, 'Employee'))
        user_role.setStyleSheet("color: #94a3b8; font-size: 12px; background: transparent;")
        user_role.setAlignment(Qt.AlignRight)
        
        user_layout.addWidget(user_name)
        user_layout.addWidget(user_role)
        lay.addWidget(user_frame)
        
        # User Avatar (Circle)
        avatar = QLabel(self.current_employee.employee_name[0])
        avatar.setFixedSize(40, 40)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet("""
            QLabel {
                background: #3b82f6;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-radius: 20px;
                border: 2px solid #1e293b;
            }
        """)
        lay.addWidget(avatar)

        top.setLayout(lay)
        return top
    
    def navigate_to(self, index):
        """Navigate to a specific page"""
        self.stacked_widget.setCurrentIndex(index)
        self._set_active_nav(index)
        self._set_title_for_index(index)

        # Refresh data on the new page
        widget = self.stacked_widget.widget(index)
        if hasattr(widget, 'refresh_data'):
            widget.refresh_data()

    def _set_active_nav(self, index: int) -> None:
        for idx, btn in self._nav_buttons.items():
            btn.set_active(idx == index)

    def _set_title_for_index(self, index: int) -> None:
        titles = {
            0: "Dashboard Overview",
            1: "Employee Directory",
            2: "Attendance Management",
            3: "Monthly Payroll Processing",
            4: "Reports & Analytics",
            5: "Master Data Management",
        }
        self.page_title.setText(titles.get(index, "PayMaster"))
    
    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self, "Logout", 
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()
