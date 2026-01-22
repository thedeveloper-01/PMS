
"""
Global QSS theme for PayMaster Payroll System
Matches the premium "Slate" design of the Login Window
"""

from __future__ import annotations


def app_stylesheet() -> str:
    # Premium Slate Color Palette (Tailwind-inspired)
    bg_primary = "#0f172a"      # Slte 900 (Main background)
    bg_secondary = "#1e293b"    # Slate 800 (Secondary background / Sidebar)
    bg_card = "#1e293b"         # Slate 800 (Cards)
    bg_card_alt = "#334155"     # Slate 700 (Input fields)
    bg_surface = "#020617"      # Slate 950 (Surface / Deep background)
    bg_header = "#1e293b"       # Header background
    
    border_primary = "rgba(255, 255, 255, 0.08)"  # Subtle light border
    border_secondary = "rgba(255, 255, 255, 0.15)" # Slightly stronger border
    border_focus = "#3b82f6"    # Blue 500 (Focus state)
    
    text_primary = "#f8fafc"    # Slate 50 (Primary text)
    text_secondary = "#cbd5e1"  # Slate 300 (Secondary text)
    text_muted = "#94a3b8"      # Slate 400 (Muted text)
    text_dark = "#64748b"       # Slate 500 (Darker text)
    
    primary = "#3b82f6"         # Blue 500
    primary_hover = "#2563eb"   # Blue 600
    primary_active = "#1d4ed8"  # Blue 700
    primary_light = "rgba(59, 130, 246, 0.15)"  # Primary transparent
    
    success = "#10b981"         # Emerald 500
    success_bg = "rgba(16, 185, 129, 0.15)"
    
    danger = "#ef4444"          # Red 500
    danger_bg = "rgba(239, 68, 68, 0.15)"
    
    warning = "#f59e0b"         # Amber 500
    warning_bg = "rgba(245, 158, 11, 0.15)"
    
    info = "#06b6d4"            # Cyan 500
    info_bg = "rgba(6, 182, 212, 0.15)"
    
    purple = "#a855f7"          # Purple 500
    purple_bg = "rgba(168, 85, 247, 0.15)"

    return f"""
    /* ========== BASE STYLES ========== */
    * {{
        outline: none;
        font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: {text_primary};
        selection-background-color: {primary};
        selection-color: {text_primary};
    }}
    
    QMainWindow, QWidget {{
        background: {bg_primary};
    }}
    
    /* ========== TYPOGRAPHY ========== */
    QLabel {{
        color: {text_primary};
        background: transparent;
    }}
    
    QLabel#PageTitle {{
        font-size: 24px;
        font-weight: 700;
        color: {text_primary};
        letter-spacing: -0.5px;
        padding-bottom: 5px;
    }}
    
    QLabel#PageSubtitle {{
        font-size: 14px;
        font-weight: 500;
        color: {text_secondary};
    }}
    
    QLabel#SectionTitle {{
        font-size: 16px;
        font-weight: 600;
        color: {text_primary};
        margin-top: 10px;
        margin-bottom: 8px;
    }}
    
    QLabel#CardTitle {{
        font-size: 13px;
        font-weight: 700;
        color: {text_secondary};
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    QLabel#CardValue {{
        font-size: 36px;
        font-weight: 800;
        color: {text_primary};
        padding-top: 8px;
    }}
    
    /* ========== SURFACES & CARDS ========== */
    QFrame#Surface {{
        background: {bg_surface};
        border: none;
    }}
    
    QFrame#Card {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 12px;
    }}
    
    QFrame#Card:hover {{
        border: 1px solid {border_secondary};
    }}
    
    QFrame#StatCard {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {bg_card}, stop:1 {bg_card_alt});
        border: 1px solid {border_primary};
        border-radius: 16px;
    }}

    QFrame#StatCard:hover {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {bg_card_alt}, stop:1 {bg_card});
        border: 1px solid {border_secondary};
    }}
    
    /* ========== INPUTS ========== */
    QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox, QTimeEdit, QTextEdit {{
        background: {bg_surface};
        border: 1px solid {border_primary};
        border-radius: 8px;
        padding: 8px 12px;
        color: {text_primary};
        font-size: 13px;
        min-height: 20px;
    }}
    
    QLineEdit:hover, QComboBox:hover, QDateEdit:hover, 
    QSpinBox:hover, QDoubleSpinBox:hover, QTimeEdit:hover, QTextEdit:hover {{
        border: 1px solid {border_secondary};
    }}
    
    QLineEdit:focus, QComboBox:focus, QDateEdit:focus, 
    QSpinBox:focus, QDoubleSpinBox:focus, QTimeEdit:focus, QTextEdit:focus {{
        border: 1px solid {primary};
        background: {bg_surface};
    }}
    
    QLineEdit::placeholder, QTextEdit::placeholder {{
        color: {text_dark};
    }}
    
    /* Combo Box Dropdown */
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        border: none;
        width: 0;
        height: 0;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {text_muted};
        margin-right: 10px;
    }}
    
    QComboBox QAbstractItemView {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 8px;
        padding: 4px;
        outline: none;
    }}
    
    QComboBox QAbstractItemView::item {{
        padding: 8px 12px;
        border-radius: 4px;
        color: {text_secondary};
    }}
    
    QComboBox QAbstractItemView::item:hover {{
        background: {bg_card_alt};
        color: {text_primary};
    }}
    
    QComboBox QAbstractItemView::item:selected {{
        background: {primary_light};
        color: {primary};
    }}
    
    /* Spin Boxes */
    QSpinBox::up-button, QSpinBox::down-button, 
    QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
        background: transparent;
        border: none;
        width: 20px;
        border-radius: 2px;
    }}
    
    QSpinBox::up-button:hover, QSpinBox::down-button:hover,
    QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
        background: {bg_card_alt};
    }}
    
    QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-bottom: 5px solid {text_muted};
        height: 0;
        width: 0;
    }}
    
    QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid {text_muted};
        height: 0;
        width: 0;
    }}
    
    /* ========== BUTTONS ========== */
    QPushButton {{
        background: {bg_card_alt};
        border: 1px solid {border_primary};
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 14px;
        color: {text_secondary};
        min-height: 32px;
    }}
    
    QPushButton:hover {{
        background: #475569; /* Slate 600 */
        border: 1px solid {border_secondary};
        color: {text_primary};
    }}
    
    QPushButton:pressed {{
        background: {bg_card_alt};
    }}
    
    QPushButton#PrimaryButton {{
        background: {primary};
        border: 1px solid {primary};
        color: #ffffff;
    }}
    
    QPushButton#PrimaryButton:hover {{
        background: {primary_hover};
        border: 1px solid {primary_hover};
    }}
    
    QPushButton#PrimaryButton:pressed {{
        background: {primary_active};
        border: 1px solid {primary_active};
    }}
    
    QPushButton#DangerButton {{
        background: {danger};
        border: 1px solid {danger};
        color: #ffffff;
    }}
    
    QPushButton#DangerButton:hover {{
        background: #dc2626; /* Red 600 */
        border: 1px solid #dc2626;
    }}

    QPushButton#WarningButton {{
        background: {warning};
        border: 1px solid {warning};
        color: #ffffff;
    }}
    
    QPushButton#WarningButton:hover {{
        background: #d97706; /* Amber 600 */
        border: 1px solid #d97706;
    }}
    
    QPushButton#InfoButton {{
        background: {primary};
        border: 1px solid {primary};
        color: #ffffff;
    }}
    
    QPushButton#InfoButton:hover {{
        background: {primary_hover};
        border: 1px solid {primary_hover};
    }}
    
    /* ========== SIDEBAR NAVIGATION ========== */
    /* Handled mostly in MainWindow, but here are shared styles */
    
    QPushButton#NavButton {{
        background: transparent;
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        text-align: left;
        color: {text_muted};
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 4px;
    }}
    
    QPushButton#NavButton:hover {{
        background: rgba(255, 255, 255, 0.03);
        color: {text_primary};
    }}
    
    QPushButton#NavButton[active="true"] {{
        background: {primary};
        color: white;
    }}
    
    /* ========== TABLES ========== */
    QTableWidget {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 8px;
        gridline-color: {border_primary};
        outline: none;
    }}
    
    QTableWidget::item {{
        padding: 10px 12px;
        border-bottom: none;
        color: {text_secondary};
    }}
    
    QTableWidget::item:selected {{
        background: {primary_light};
        color: {primary};
    }}
    
    QHeaderView::section {{
        background: {bg_surface};
        color: {text_muted};
        border: none;
        border-bottom: 1px solid {border_primary};
        padding: 12px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    QTableCornerButton::section {{
        background: {bg_surface};
        border: none;
        border-bottom: 1px solid {border_primary};
    }}
    
    /* ========== TABS ========== */
    QTabWidget::pane {{
        border: 1px solid {border_primary};
        background: {bg_card};
        border-radius: 8px;
    }}
    
    QTabBar::tab {{
        background: transparent;
        color: {text_muted};
        padding: 10px 20px;
        border-bottom: 2px solid transparent;
        font-weight: 600;
    }}
    
    QTabBar::tab:selected {{
        color: {primary};
        border-bottom: 2px solid {primary};
    }}
    
    QTabBar::tab:hover:!selected {{
        color: {text_primary};
        background: rgba(255, 255, 255, 0.03);
    }}
    
    /* ========== SCROLLBARS ========== */
    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 0;
    }}
    
    QScrollBar::handle:vertical {{
        background: {bg_card_alt};
        min-height: 20px;
        border-radius: 4px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: {text_muted};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    
    QScrollBar:horizontal {{
        background: transparent;
        height: 8px;
        margin: 0;
    }}
    
    QScrollBar::handle:horizontal {{
        background: {bg_card_alt};
        min-width: 20px;
        border-radius: 4px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background: {text_muted};
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0;
    }}
    
    /* ========== MISC ========== */
    QMessageBox {{
        background: {bg_card};
    }}
    
    QDialog {{
        background: {bg_card};
    }}
    
    QToolTip {{
        background: {bg_surface};
        color: {text_primary};
        border: 1px solid {border_primary};
        padding: 4px 8px;
        border-radius: 4px;
    }}
    
    /* ========== BADGES ========== */
    QLabel#StatusActive {{
        background: {success_bg};
        color: {success};
        border-radius: 6px;
        padding: 2px 8px;
        font-weight: 600;
        font-size: 11px;
    }}
    
    QLabel#StatusInactive {{
        background: {danger_bg};
        color: {danger};
        border-radius: 6px;
        padding: 2px 8px;
        font-weight: 600;
        font-size: 11px;
    }}
    
    QLabel#Badge {{
        background: {purple_bg};
        color: {purple};
        border-radius: 6px;
        padding: 2px 8px;
        font-weight: 600;
        font-size: 11px;
    }}
    """
