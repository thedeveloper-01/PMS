"""
Global QSS theme – FIXED
No label bleed, no white bars, no ghost backgrounds
"""

from __future__ import annotations


def app_stylesheet() -> str:
    primary = "#135bec"
    primary_hover = "#0f4ad0"

    bg = "#101622"
    surface = "#111722"
    card = "#1c212c"
    card_alt = "#232f48"

    border = "#282e39"
    border_alt = "#324467"

    text = "#ffffff"
    text_secondary = "#cbd5e1"
    muted = "#92a4c9"

    danger = "#ef4444"
    success = "#10b981"

    return f"""
    /* =====================================================
       BASE RESET (CRITICAL)
       ===================================================== */

    * {{
        font-family: "Segoe UI", "Inter", sans-serif;
        color: {text};
        background: transparent;
    }}

    QMainWindow {{
        background: {bg};
    }}

    /* =====================================================
       LABELS (NO BACKGROUND – EVER)
       ===================================================== */

    QLabel {{
        background: transparent;
    }}

    QLabel#PageTitle {{
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }}

    QLabel#PageSubtitle {{
        font-size: 12px;
        font-weight: 600;
        color: {muted};
    }}

    QLabel#SectionTitle {{
        font-size: 18px;
        font-weight: 700;
    }}

    QLabel#CardTitle {{
        font-size: 14px;
        font-weight: 600;
        color: {muted};
    }}

    QLabel#CardValue {{
        font-size: 32px;
        font-weight: 700;
    }}

    /* =====================================================
       SURFACES & CARDS
       ===================================================== */

    QFrame#Surface {{
        background: {surface};
        border: none;
    }}

    QFrame#Card {{
        background: {card};
        border: 1px solid {border};
        border-radius: 14px;
    }}

    QFrame#StatCard {{
        background: {card};
        border: 1px solid {border};
        border-radius: 14px;
        padding: 20px;
    }}

    QFrame#StatCard:hover {{
        border: 1px solid rgba(19,91,236,0.45);
    }}

    /* =====================================================
       INPUTS (CLIPPED – NO BLEED)
       ===================================================== */

    QLineEdit,
    QComboBox,
    QDateEdit,
    QSpinBox,
    QDoubleSpinBox,
    QTextEdit,
    QTimeEdit {{
        background: {card_alt};
        border: 1px solid {border_alt};
        border-radius: 10px;
        padding: 10px 12px;
        font-size: 14px;
    }}

    QLineEdit:focus,
    QComboBox:focus,
    QDateEdit:focus,
    QSpinBox:focus,
    QDoubleSpinBox:focus,
    QTextEdit:focus,
    QTimeEdit:focus {{
        border: 1px solid {primary};
    }}

    QLineEdit::placeholder {{
        color: {muted};
    }}

    /* =====================================================
       BUTTONS
       ===================================================== */

    QPushButton {{
        background: rgba(255,255,255,0.04);
        border: 1px solid {border};
        border-radius: 10px;
        padding: 10px 16px;
        font-weight: 600;
        font-size: 14px;
    }}

    QPushButton:hover {{
        background: rgba(19,91,236,0.10);
        border-color: rgba(19,91,236,0.55);
    }}

    QPushButton:pressed {{
        background: rgba(19,91,236,0.18);
    }}

    QPushButton#PrimaryButton {{
        background: {primary};
        border: 1px solid {primary};
    }}

    QPushButton#PrimaryButton:hover {{
        background: {primary_hover};
        border-color: {primary_hover};
    }}

    QPushButton#DangerButton {{
        background: rgba(239,68,68,0.18);
        border: 1px solid rgba(239,68,68,0.40);
        color: #fca5a5;
    }}

    /* =====================================================
       TABLES
       ===================================================== */

    QTableWidget {{
        background: {card};
        border: 1px solid {border};
        border-radius: 14px;
        gridline-color: {border};
        selection-background-color: rgba(19,91,236,0.15);
    }}

    QTableWidget::item {{
        padding: 12px;
        border-bottom: 1px solid {border};
        color: {text_secondary};
    }}

    QTableWidget::item:selected {{
        background: rgba(19,91,236,0.18);
        color: {text};
    }}

    QHeaderView::section {{
        background: #1e293b;
        color: {muted};
        border: none;
        border-bottom: 1px solid {border};
        padding: 12px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
    }}

    /* =====================================================
       SCROLLBARS
       ===================================================== */

    QScrollBar:vertical {{
        background: {surface};
        width: 10px;
        border-radius: 5px;
    }}

    QScrollBar::handle:vertical {{
        background: {border_alt};
        border-radius: 5px;
        min-height: 24px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: #4b628b;
    }}

    QScrollBar::add-line,
    QScrollBar::sub-line {{
        height: 0px;
        width: 0px;
    }}

    /* =====================================================
       MESSAGE BOX
       ===================================================== */

    QMessageBox {{
        background: {card};
    }}

    QMessageBox QLabel {{
        background: transparent;
    }}
    """
