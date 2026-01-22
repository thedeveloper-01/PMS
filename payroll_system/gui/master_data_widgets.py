"""
Master Data Management Widgets
UI FIXED – no bleed, no ghost backgrounds, theme-safe
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QLineEdit,
    QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from payroll_system.repository.master_data_repository import MasterDataRepository


class MasterDataWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.repo = MasterDataRepository()
        self.init_ui()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 24, 32, 24)
        root.setSpacing(24)

        # ---------- Header ----------
        header = QLabel("Master Data Management")
        header.setObjectName("PageTitle")
        header.setAttribute(Qt.WA_TranslucentBackground, True)
        root.addWidget(header)

        # ---------- Grid ----------
        grid = QHBoxLayout()
        grid.setSpacing(24)

        grid.addWidget(self.create_section(
            "🏢 Departments",
            self.repo.get_all_departments,
            self.repo.add_department,
            self.repo.delete_department
        ))

        grid.addWidget(self.create_section(
            "🎓 Designations",
            self.repo.get_all_designations,
            self.repo.add_designation,
            self.repo.delete_designation
        ))

        grid.addWidget(self.create_section(
            "🏬 Branches",
            self.repo.get_all_branches,
            self.repo.add_branch,
            self.repo.delete_branch
        ))

        root.addLayout(grid)
        root.addStretch()

    # =================================================================

    def create_section(self, title, fetch_fn, add_fn, delete_fn) -> QFrame:
        card = QFrame()
        card.setObjectName("Card")
        card.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setObjectName("SectionTitle")
        title_label.setAttribute(Qt.WA_TranslucentBackground, True)

        list_widget = QListWidget()
        self.populate_list(list_widget, fetch_fn)

        input_field = QLineEdit()
        input_field.setPlaceholderText("Enter name")

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        add_btn = QPushButton("➕ Add")
        add_btn.setObjectName("PrimaryButton")

        delete_btn = QPushButton("🗑 Delete")
        delete_btn.setObjectName("DangerButton")

        btn_row.addWidget(add_btn)
        btn_row.addWidget(delete_btn)

        layout.addWidget(title_label)
        layout.addWidget(list_widget)
        layout.addWidget(input_field)
        layout.addLayout(btn_row)

        # ---------- Actions ----------
        add_btn.clicked.connect(
            lambda: self.add_item(
                input_field, list_widget, add_fn
            )
        )

        delete_btn.clicked.connect(
            lambda: self.delete_item(
                list_widget, delete_fn
            )
        )

        return card

    # =================================================================

    def populate_list(self, list_widget, fetch_fn):
        list_widget.clear()
        for item in fetch_fn():
            list_widget.addItem(item.name)

    def add_item(self, input_field, list_widget, add_fn):
        name = input_field.text().strip()
        if not name:
            QMessageBox.warning(self, "Required", "Name cannot be empty.")
            return

        try:
            add_fn(name)
            list_widget.addItem(name)
            input_field.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete_item(self, list_widget, delete_fn):
        selected = list_widget.currentItem()
        if not selected:
            QMessageBox.warning(self, "Select", "Please select an item to delete.")
            return

        try:
            delete_fn(selected.text())
            list_widget.takeItem(list_widget.currentRow())
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
