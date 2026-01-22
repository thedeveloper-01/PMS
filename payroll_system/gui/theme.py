"""
Global QSS theme inspired by the provided `screens/*` designs.

Dark, card-based UI with blue primary accent.
"""

from __future__ import annotations


def app_stylesheet() -> str:
    # Palette derived from the screenshots' Tailwind config.
    primary = "#135bec"
    bg = "#101622"
    surface = "#111318"
    card = "#1c212c"
    card_2 = "#232f48"
    border = "#282e39"
    border_2 = "#324467"
    text = "#ffffff"
    muted = "#92a4c9"
    danger = "#ef4444"
    success = "#10b981"
    warning = "#f59e0b"

    return f"""
    /* Base */
    * {{
        font-family: "Segoe UI", "Inter", sans-serif;
        color: {text};
        selection-background-color: {primary};
        selection-color: {text};
    }}

    QMainWindow, QWidget {{
        background: {bg};
    }}

    /* Typography */
    QLabel#PageTitle {{
        font-size: 28px;
        font-weight: 800;
        color: {text};
    }}
    QLabel#PageSubtitle {{
        font-size: 12px;
        font-weight: 600;
        color: {muted};
    }}

    /* Surfaces */
    QFrame#Surface {{
        background: {surface};
        border: 1px solid {border};
    }}
    QFrame#Card {{
        background: {card};
        border: 1px solid {border};
        border-radius: 14px;
    }}
    QFrame#CardAlt {{
        background: {card_2};
        border: 1px solid {border_2};
        border-radius: 14px;
    }}

    /* Inputs */
    QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox, QTimeEdit {{
        background: {card_2};
        border: 1px solid {border_2};
        border-radius: 10px;
        padding: 10px 12px;
        color: {text};
    }}
    QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTimeEdit:focus {{
        border: 1px solid {primary};
    }}

    QComboBox::drop-down {{
        border: 0px;
        width: 28px;
    }}

    /* Buttons */
    QPushButton {{
        background: rgba(255,255,255,0.04);
        border: 1px solid {border};
        border-radius: 10px;
        padding: 10px 14px;
        font-weight: 600;
    }}
    QPushButton:hover {{
        border: 1px solid rgba(19,91,236,0.65);
        background: rgba(19,91,236,0.10);
    }}
    QPushButton:pressed {{
        background: rgba(19,91,236,0.18);
    }}

    QPushButton#PrimaryButton {{
        background: {primary};
        border: 1px solid {primary};
    }}
    QPushButton#PrimaryButton:hover {{
        background: #0f4ad0;
        border: 1px solid #0f4ad0;
    }}

    QPushButton#DangerButton {{
        background: rgba(239,68,68,0.18);
        border: 1px solid rgba(239,68,68,0.40);
    }}
    QPushButton#DangerButton:hover {{
        background: rgba(239,68,68,0.28);
        border: 1px solid rgba(239,68,68,0.65);
    }}

    /* Sidebar nav buttons */
    QPushButton#NavButton {{
        background: transparent;
        border: 0px;
        border-radius: 12px;
        padding: 12px 14px;
        text-align: left;
        color: {muted};
    }}
    QPushButton#NavButton:hover {{
        background: rgba(255,255,255,0.05);
        color: {text};
    }}
    QPushButton#NavButton[active="true"] {{
        background: {primary};
        color: {text};
    }}

    /* Tables */
    QTableWidget {{
        background: {card};
        border: 1px solid {border};
        border-radius: 14px;
        gridline-color: {border};
        selection-background-color: rgba(19,91,236,0.25);
        selection-color: {text};
    }}
    QHeaderView::section {{
        background: #1e293b;
        color: {muted};
        border: 0px;
        border-bottom: 1px solid {border};
        padding: 10px 12px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
    }}
    QTableWidget::item {{
        padding: 10px;
        border-bottom: 1px solid {border};
    }}

    /* Scrollbars */
    QScrollBar:vertical {{
        background: {surface};
        width: 10px;
        margin: 0px;
    }}
    QScrollBar::handle:vertical {{
        background: {border_2};
        border-radius: 5px;
        min-height: 24px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: #4b628b;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    """


