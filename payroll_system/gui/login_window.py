"""
PayMaster Login Window
FINAL – all rendering issues fixed (labels, inputs, shadow, text glow)
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFrame, QApplication,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from payroll_system.services.employee_service import EmployeeService
from payroll_system.config import ROLE_NAMES


# ---------- Shadow Helper ----------
def apply_card_shadow(widget: QFrame):
    widget.setAttribute(Qt.WA_TranslucentBackground, True)
    widget.setAutoFillBackground(False)
    widget.setAttribute(Qt.WA_StyledBackground, True)

    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(26)
    shadow.setOffset(0, 6)
    shadow.setColor(QColor(0, 0, 0, 130))
    widget.setGraphicsEffect(shadow)


# ---------- Input Group (CRITICAL FIX) ----------
def input_group(label_text: str, line_edit: QLineEdit) -> QFrame:
    """
    Groups label + input to prevent Qt repaint bleed.
    """
    group = QFrame()
    group.setAttribute(Qt.WA_TranslucentBackground, True)
    group.setAutoFillBackground(False)

    layout = QVBoxLayout(group)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(6)

    label = QLabel(label_text)
    label.setAttribute(Qt.WA_TranslucentBackground, True)
    label.setAutoFillBackground(False)
    label.setStyleSheet("""
        QLabel {
            background: transparent;
            color: #cbd5e1;
            font-size: 13px;
            font-weight: 600;
        }
    """)

    # Ensure input never paints outside itself
    line_edit.setAttribute(Qt.WA_StyledBackground, True)
    line_edit.setAutoFillBackground(True)
    line_edit.setGraphicsEffect(None)

    layout.addWidget(label)
    layout.addWidget(line_edit)
    return group


# ---------- Clean Title Label ----------
def clean_label(text: str, size: int, weight: int, color: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setAlignment(Qt.AlignCenter)
    lbl.setAttribute(Qt.WA_TranslucentBackground, True)
    lbl.setAutoFillBackground(False)

    font = QFont("Segoe UI", size)
    font.setWeight(weight)
    font.setStyleStrategy(QFont.PreferAntialias)  # disable subpixel glow
    lbl.setFont(font)

    lbl.setStyleSheet(f"""
        QLabel {{
            background: transparent;
            color: {color};
        }}
    """)
    return lbl


# ===================================================================

class LoginWindow(QWidget):

    login_successful = Signal(object)

    def __init__(self):
        super().__init__()
        self.employee_service = EmployeeService()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PayMaster – Login")
        self.setFixedSize(480, 600)

        # Background ONLY for root widget
        self.setStyleSheet("""
            LoginWindow {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f172a,
                    stop:1 #1e293b
                );
            }
        """)

        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)
        root.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setAttribute(Qt.WA_TranslucentBackground, True)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(50, 20, 50, 40)
        container_layout.setSpacing(26)

        # ---------- Title ----------
        title = clean_label("PayMaster", 30, QFont.Bold, "#ffffff")
        subtitle = clean_label("Sign in to your account", 14, QFont.Medium, "#94a3b8")

        container_layout.addWidget(title)
        container_layout.addWidget(subtitle)

        # ---------- Card ----------
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 18px;
            }
        """)
        apply_card_shadow(card)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 36)
        card_layout.setSpacing(14)

        # ---------- Email ----------
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setStyleSheet(self.input_style())
        email_group = input_group("Email or Username", self.email_input)

        # ---------- Password ----------
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.input_style())
        password_group = input_group("Password", self.password_input)

        # ---------- Button ----------
        login_btn = QPushButton("Sign In")
        login_btn.setFixedHeight(46)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background: #2563eb;
                border-radius: 12px;
                color: #ffffff;
                font-size: 15px;
                font-weight: 700;
            }
            QPushButton:hover { background: #1d4ed8; }
            QPushButton:pressed { background: #1e40af; }
        """)

        login_btn.clicked.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)

        # ---------- Assemble ----------
        card_layout.addWidget(email_group)
        card_layout.addWidget(password_group)
        card_layout.addSpacing(16)
        card_layout.addWidget(login_btn)

        container_layout.addWidget(card)
        root.addWidget(container)

        self.center_window()

    # ---------- Input Style ----------
    def input_style(self):
        return """
            QLineEdit {
                background: #0b1220;
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 10px;
                padding: 12px 14px;
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:hover { border: 1px solid rgba(255,255,255,0.20); }
            QLineEdit:focus { border: 1px solid #2563eb; }
            QLineEdit::placeholder { color: #64748b; }
        """

    # ---------- Helpers ----------
    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        geo = self.geometry()
        self.move(
            (screen.width() - geo.width()) // 2,
            (screen.height() - geo.height()) // 2
        )

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(
                self, "Login Failed",
                "Please enter both email and password."
            )
            return

        employee, message = self.employee_service.authenticate(email, password)

        if employee:
            QMessageBox.information(
                self, "Login Successful",
                f"Welcome, {employee.employee_name}\n"
                f"Role: {ROLE_NAMES.get(employee.role, 'Employee')}"
            )
            self.login_successful.emit(employee)
        else:
            QMessageBox.critical(self, "Login Failed", message)
