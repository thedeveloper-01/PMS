
"""
Global QSS theme for PayMaster Payroll System
Matches the screenshot designs exactly
"""

from __future__ import annotations


def app_stylesheet() -> str:
    # Color palette matching the screenshot designs
    bg_primary = "#0f172a"      # Main background
    bg_secondary = "#1e293b"    # Secondary background
    bg_card = "#1f2937"         # Card background
    bg_card_alt = "#374151"     # Alternative card background
    bg_surface = "#111827"      # Surface background
    bg_header = "#1f2937"       # Header background
    
    border_primary = "#374151"  # Primary border
    border_secondary = "#4b5563" # Secondary border
    border_light = "#6b7280"    # Light border
    
    text_primary = "#ffffff"    # Primary text
    text_secondary = "#d1d5db"  # Secondary text
    text_muted = "#9ca3af"      # Muted text
    text_dark = "#6b7280"       # Dark text
    
    primary = "#3b82f6"         # Primary blue
    primary_hover = "#2563eb"   # Primary hover
    primary_light = "rgba(59, 130, 246, 0.1)"  # Primary light
    
    success = "#10b981"         # Success green
    success_hover = "#059669"   # Success hover
    success_light = "rgba(16, 185, 129, 0.1)"  # Success light
    
    danger = "#ef4444"          # Danger red
    danger_hover = "#dc2626"    # Danger hover
    danger_light = "rgba(239, 68, 68, 0.1)"  # Danger light
    
    warning = "#f59e0b"         # Warning orange
    warning_hover = "#d97706"   # Warning hover
    warning_light = "rgba(245, 158, 11, 0.1)"  # Warning light
    
    info = "#06b6d4"            # Info cyan
    info_hover = "#0891b2"      # Info hover
    info_light = "rgba(6, 182, 212, 0.1)"  # Info light
    
    purple = "#a855f7"          # Purple
    purple_hover = "#9333ea"    # Purple hover
    purple_light = "rgba(168, 85, 247, 0.1)"  # Purple light
    
    orange = "#f97316"          # Orange
    orange_hover = "#ea580c"    # Orange hover
    orange_light = "rgba(249, 115, 22, 0.1)"  # Orange light
    
    emerald = "#10b981"         # Emerald
    emerald_hover = "#059669"   # Emerald hover
    emerald_light = "rgba(16, 185, 129, 0.1)"  # Emerald light

    return f"""
    /* ========== BASE STYLES ========== */
    * {{
        outline: none;
        font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: {text_primary};
    }}
    
    QMainWindow, QWidget {{
        background: {bg_primary};
    }}
    
    /* ========== TYPOGRAPHY ========== */
    QLabel {{
        color: {text_primary};
    }}
    
    QLabel#PageTitle {{
        font-size: 20px;
        font-weight: 700;
        color: {text_primary};
        letter-spacing: -0.3px;
    }}
    
    QLabel#PageSubtitle {{
        font-size: 12px;
        font-weight: 600;
        color: {text_muted};
    }}
    
    QLabel#SectionTitle {{
        font-size: 18px;
        font-weight: 700;
        color: {text_primary};
        margin-bottom: 10px;
    }}
    
    QLabel#CardTitle {{
        font-size: 14px;
        font-weight: 600;
        color: {text_muted};
        margin-bottom: 5px;
    }}
    
    QLabel#CardValue {{
        font-size: 32px;
        font-weight: 800;
        color: {text_primary};
    }}
    
    /* ========== SURFACES & CARDS ========== */
    QFrame#Surface {{
        background: {bg_surface};
        border: none;
    }}
    
    QFrame#Card {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 10px;
    }}
    
    QFrame#Card:hover {{
        border-color: {primary};
    }}
    
    QFrame#CardAlt {{
        background: {bg_card_alt};
        border: 1px solid {border_secondary};
        border-radius: 8px;
    }}
    
    QFrame#StatCard {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 10px;
        padding: 20px;
    }}
    
    /* ========== INPUTS ========== */
    QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox, QTimeEdit, QTextEdit {{
        background: {bg_card_alt};
        border: 1px solid {border_secondary};
        border-radius: 6px;
        padding: 10px 12px;
        color: {text_primary};
        font-size: 14px;
        selection-background-color: {primary};
        selection-color: {text_primary};
    }}
    
    QLineEdit:focus, QComboBox:focus, QDateEdit:focus, 
    QSpinBox:focus, QDoubleSpinBox:focus, QTimeEdit:focus, QTextEdit:focus {{
        border: 1px solid {primary};
        background: {bg_card_alt};
    }}
    
    QLineEdit::placeholder, QTextEdit::placeholder {{
        color: {text_muted};
    }}
    
    QComboBox::drop-down {{
        border: 0px;
        width: 30px;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 7px solid {text_muted};
        width: 0px;
        height: 0px;
        margin-right: 8px;
    }}
    
    QComboBox::down-arrow:hover {{
        border-top-color: {text_primary};
    }}
    
    QComboBox QAbstractItemView {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 6px;
        padding: 4px;
        selection-background-color: {primary};
        selection-color: {text_primary};
    }}
    
    QComboBox QAbstractItemView::item {{
        padding: 8px 12px;
        border-radius: 4px;
        margin: 2px;
    }}
    
    QComboBox QAbstractItemView::item:hover {{
        background: {primary_light};
    }}
    
    QSpinBox::up-button, QSpinBox::down-button, 
    QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
        background: transparent;
        border: none;
        width: 20px;
    }}
    
    QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-bottom: 7px solid {text_muted};
        width: 0px;
        height: 0px;
    }}
    
    QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 7px solid {text_muted};
        width: 0px;
        height: 0px;
    }}
    
    QSpinBox::up-arrow:hover, QSpinBox::down-arrow:hover,
    QDoubleSpinBox::up-arrow:hover, QDoubleSpinBox::down-arrow:hover {{
        border-bottom-color: {text_primary};
        border-top-color: {text_primary};
    }}
    
    /* ========== BUTTONS ========== */
    QPushButton {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid {border_primary};
        border-radius: 6px;
        padding: 10px 16px;
        font-weight: 600;
        font-size: 14px;
        color: {text_primary};
        min-height: 40px;
    }}
    
    QPushButton:hover {{
        background: rgba(255, 255, 255, 0.1);
        border-color: {border_light};
    }}
    
    QPushButton:pressed {{
        background: rgba(255, 255, 255, 0.15);
    }}
    
    QPushButton:disabled {{
        background: rgba(255, 255, 255, 0.02);
        border-color: {border_secondary};
        color: {text_muted};
    }}
    
    QPushButton#PrimaryButton {{
        background: {primary};
        border: 1px solid {primary};
        color: {text_primary};
        font-weight: 600;
    }}
    
    QPushButton#PrimaryButton:hover {{
        background: {primary_hover};
        border-color: {primary_hover};
    }}
    
    QPushButton#PrimaryButton:pressed {{
        background: #1d4ed8;
        border-color: #1d4ed8;
    }}
    
    QPushButton#SecondaryButton {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: {text_primary};
        font-weight: 500;
    }}
    
    QPushButton#SecondaryButton:hover {{
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.2);
    }}
    
    QPushButton#DangerButton {{
        background: {danger_light};
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: {danger};
    }}
    
    QPushButton#DangerButton:hover {{
        background: rgba(239, 68, 68, 0.2);
        border-color: rgba(239, 68, 68, 0.5);
    }}
    
    /* ========== SIDEBAR NAVIGATION ========== */
    QPushButton#NavButton {{
        background: transparent;
        border: 0px;
        border-radius: 8px;
        padding: 12px 16px;
        text-align: left;
        color: {text_muted};
        font-weight: 600;
        font-size: 14px;
        margin: 2px 0px;
    }}
    
    QPushButton#NavButton:hover {{
        background: rgba(255, 255, 255, 0.05);
        color: {text_primary};
    }}
    
    QPushButton#NavButton[active="true"] {{
        background: {primary};
        color: {text_primary};
    }}
    
    /* ========== TABLES ========== */
    QTableWidget {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 8px;
        gridline-color: {border_primary};
        selection-background-color: {primary_light};
        selection-color: {text_primary};
        alternate-background-color: rgba(255, 255, 255, 0.02);
        outline: none;
    }}
    
    QTableWidget::item {{
        padding: 12px 15px;
        border: none;
        border-bottom: 1px solid {border_primary};
        color: {text_secondary};
    }}
    
    QTableWidget::item:hover {{
        background: rgba(255, 255, 255, 0.03);
    }}
    
    QTableWidget::item:selected {{
        background: {primary_light};
        color: {text_primary};
    }}
    
    QHeaderView::section {{
        background: {bg_header};
        color: {text_muted};
        border: 0px;
        border-bottom: 1px solid {border_primary};
        padding: 14px 15px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    QHeaderView::section:checked {{
        background: {bg_header};
    }}
    
    QTableCornerButton::section {{
        background: {bg_header};
        border: 0px;
        border-bottom: 1px solid {border_primary};
        border-right: 1px solid {border_primary};
    }}
    
    /* ========== TAB WIDGET ========== */
    QTabWidget::pane {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 8px;
        margin-top: 5px;
    }}
    
    QTabWidget::tab-bar {{
        alignment: left;
    }}
    
    QTabBar::tab {{
        background: transparent;
        color: {text_muted};
        padding: 12px 24px;
        margin-right: 2px;
        border: none;
        border-bottom: 2px solid transparent;
        font-weight: 600;
        font-size: 14px;
    }}
    
    QTabBar::tab:selected {{
        color: {primary};
        border-bottom: 2px solid {primary};
    }}
    
    QTabBar::tab:hover:!selected {{
        color: {text_primary};
        background: rgba(255, 255, 255, 0.05);
        border-radius: 6px 6px 0px 0px;
    }}
    
    /* ========== SCROLLBARS ========== */
    QScrollBar:vertical {{
        background: transparent;
        width: 10px;
        margin: 0px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:vertical {{
        background: {border_secondary};
        border-radius: 5px;
        min-height: 24px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: {border_light};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar:horizontal {{
        background: transparent;
        height: 10px;
        margin: 0px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:horizontal {{
        background: {border_secondary};
        border-radius: 5px;
        min-width: 24px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background: {border_light};
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    
    QScrollArea {{
        border: none;
        background: transparent;
    }}
    
    /* ========== MESSAGE BOXES ========== */
    QMessageBox {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 8px;
    }}
    
    QMessageBox QLabel {{
        color: {text_primary};
        font-size: 14px;
    }}
    
    QMessageBox QPushButton {{
        min-width: 80px;
        min-height: 36px;
        margin: 5px;
    }}
    
    /* ========== TOOLTIPS ========== */
    QToolTip {{
        background: {bg_card};
        color: {text_primary};
        border: 1px solid {border_primary};
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 12px;
    }}
    
    /* ========== DIALOGS ========== */
    QDialog {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 8px;
    }}
    
    QDialogButtonBox QPushButton {{
        min-width: 70px;
    }}
    
    /* ========== STATUS BADGES ========== */
    QLabel#StatusActive {{
        background: {emerald_light};
        color: {emerald};
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 600;
    }}
    
    QLabel#StatusInactive {{
        background: {danger_light};
        color: {danger};
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 600;
    }}
    
    QLabel#StatusPending {{
        background: {warning_light};
        color: {warning};
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 12px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 600;
    }}
    
    QLabel#Badge {{
        background: {purple_light};
        color: {purple};
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 600;
    }}
    
    /* ========== PROGRESS BAR ========== */
    QProgressBar {{
        background: {bg_card_alt};
        border: 1px solid {border_secondary};
        border-radius: 4px;
        text-align: center;
        color: {text_primary};
        font-size: 12px;
    }}
    
    QProgressBar::chunk {{
        background: {primary};
        border-radius: 4px;
    }}
    
    /* ========== GROUP BOX ========== */
    QGroupBox {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 8px;
        margin-top: 20px;
        padding-top: 10px;
        font-weight: bold;
        color: {text_primary};
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
    }}
    
    /* ========== CHECKBOX & RADIO BUTTON ========== */
    QCheckBox, QRadioButton {{
        color: {text_primary};
        spacing: 8px;
    }}
    
    QCheckBox::indicator, QRadioButton::indicator {{
        width: 18px;
        height: 18px;
    }}
    
    QCheckBox::indicator:unchecked {{
        background: {bg_card_alt};
        border: 1px solid {border_secondary};
        border-radius: 4px;
    }}
    
    QCheckBox::indicator:checked {{
        background: {primary};
        border: 1px solid {primary};
        border-radius: 4px;
        image: url(":/icons/check.svg");
    }}
    
    QRadioButton::indicator:unchecked {{
        background: {bg_card_alt};
        border: 1px solid {border_secondary};
        border-radius: 9px;
    }}
    
    QRadioButton::indicator:checked {{
        background: {primary};
        border: 1px solid {primary};
        border-radius: 9px;
    }}
    
    /* ========== SLIDER ========== */
    QSlider::groove:horizontal {{
        background: {bg_card_alt};
        height: 4px;
        border-radius: 2px;
    }}
    
    QSlider::handle:horizontal {{
        background: {primary};
        border: 1px solid {primary};
        width: 16px;
        height: 16px;
        margin: -6px 0;
        border-radius: 8px;
    }}
    
    QSlider::sub-page:horizontal {{
        background: {primary};
        border-radius: 2px;
    }}
    
    /* ========== SPLITTER ========== */
    QSplitter::handle {{
        background: {border_primary};
    }}
    
    QSplitter::handle:hover {{
        background: {border_light};
    }}
    
    /* ========== MENU ========== */
    QMenu {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 6px;
        padding: 4px;
    }}
    
    QMenu::item {{
        padding: 6px 24px 6px 24px;
        border-radius: 4px;
        margin: 2px;
    }}
    
    QMenu::item:selected {{
        background: {primary_light};
    }}
    
    QMenu::separator {{
        height: 1px;
        background: {border_primary};
        margin: 4px 8px;
    }}
    
    /* ========== TREE VIEW ========== */
    QTreeView {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 6px;
        alternate-background-color: rgba(255, 255, 255, 0.02);
    }}
    
    QTreeView::item {{
        padding: 6px;
        border: none;
    }}
    
    QTreeView::item:hover {{
        background: rgba(255, 255, 255, 0.05);
    }}
    
    QTreeView::item:selected {{
        background: {primary_light};
    }}
    
    /* ========== LIST VIEW ========== */
    QListView {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 6px;
        alternate-background-color: rgba(255, 255, 255, 0.02);
    }}
    
    QListView::item {{
        padding: 8px 12px;
        border: none;
        border-bottom: 1px solid {border_primary};
    }}
    
    QListView::item:hover {{
        background: rgba(255, 255, 255, 0.05);
    }}
    
    QListView::item:selected {{
        background: {primary_light};
    }}
    
    /* ========== CALENDAR ========== */
    QCalendarWidget {{
        background: {bg_card};
        border: 1px solid {border_primary};
        border-radius: 6px;
    }}
    
    QCalendarWidget QToolButton {{
        background: transparent;
        border: none;
        color: {text_primary};
        font-weight: 600;
    }}
    
    QCalendarWidget QMenu {{
        background: {bg_card};
        border: 1px solid {border_primary};
    }}
    
    QCalendarWidget QSpinBox {{
        background: {bg_card_alt};
        border: 1px solid {border_secondary};
        border-radius: 4px;
        padding: 4px;
    }}
    
    QCalendarWidget QWidget#qt_calendar_navigationbar {{
        background: {bg_header};
        border-bottom: 1px solid {border_primary};
    }}
    
    QCalendarWidget QAbstractItemView:enabled {{
        color: {text_primary};
        selection-background-color: {primary};
        selection-color: {text_primary};
    }}
    
    QCalendarWidget QAbstractItemView:disabled {{
        color: {text_muted};
    }}
    """
