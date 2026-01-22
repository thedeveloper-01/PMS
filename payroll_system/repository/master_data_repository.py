"""
Master Data Management Widgets
FINAL FIX – aligned with model-based repository
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QLineEdit,
    QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from datetime import datetime
from payroll_system.repository.master_data_repository import MasterDataRepository
from payroll_system.models.master_data import Department, Designation, Branch


class MasterDataWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.repo = MasterDataRepository()
        self.init_ui()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 24, 32, 24)
        root.setSpacing(24)

        header = QLabel("Master Data Management")
        header.setObjectName("PageTitle")
        header.setAttribute(Qt.WA_TranslucentBackground, True)
        root.addWidget(header)

        grid = QHBoxLayout()
        grid.setSpacing(24)

        grid.addWidget(self.department_section())
        grid.addWidget(self.designation_section())
        grid.addWidget(self.branch_section())

        root.addLayout(grid)
        root.addStretch()

    # =====================================================
    # SECTIONS
    # =====================================================

    def department_section(self) -> QFrame:
        return self.create_section(
            "🏢 Departments",
            self.repo.get_all_departments,
            self.add_department
        )

    def designation_section(self) -> QFrame:
        return self.create_section(
            "🎓 Designations",
            self.repo.get_all_designations,
            self.add_designation
        )

    def branch_section(self) -> QFrame:
        return self.create_section(
            "🏬 Branches",
            self.repo.get_all_branches,
            self.add_branch
        )

    # =====================================================
    # UI BUILDER
    # =====================================================

    def create_section(self, title, fetch_fn, add_fn) -> QFrame:
        card = QFrame()
        card.setObjectName("Card")
        card.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setObjectName("SectionTitle")

        list_widget = QListWidget()
        self.populate_list(list_widget, fetch_fn)

        input_field = QLineEdit()
        input_field.setPlaceholderText("Enter name")

        add_btn = QPushButton("➕ Add")
        add_btn.setObjectName("PrimaryButton")

        layout.addWidget(title_label)
        layout.addWidget(list_widget)
        layout.addWidget(input_field)
        layout.addWidget(add_btn)

        add_btn.clicked.connect(
            lambda: self.add_item(
                input_field, list_widget, add_fn
            )
        )

        return card

    # =====================================================
    # MODEL-CORRECT OPERATIONS
    # =====================================================

    def add_department(self, name: str):
        dept = Department(
            department_id=name.lower().replace(" ", "_"),
            department_name=name,
            created_date=datetime.now(),
            status=1
        )
        return self.repo.create_department(dept)

    def add_designation(self, name: str):
        desig = Designation(
            designation_id=name.lower().replace(" ", "_"),
            designation_name=name,
            department_name="General",
            created_date=datetime.now(),
            status=1
        )
        return self.repo.create_designation(desig)

    def add_branch(self, name: str):
        branch = Branch(
            branch_id=name.lower().replace(" ", "_"),
            name=name,
            branch_address="",
            phone_number="",
            email="",
            created_date=datetime.now(),
            status=1
        )
        return self.repo.create_branch(branch)

    # =====================================================
    # HELPERS
    # =====================================================

    def populate_list(self, list_widget, fetch_fn):
        list_widget.clear()
        for item in fetch_fn():
            if hasattr(item, "department_name"):
                list_widget.addItem(item.department_name)
            elif hasattr(item, "designation_name"):
                list_widget.addItem(item.designation_name)
            elif hasattr(item, "name"):
                list_widget.addItem(item.name)

    def add_item(self, input_field, list_widget, add_fn):
        name = input_field.text().strip()
        if not name:
            QMessageBox.warning(self, "Required", "Name cannot be empty.")
            return

        success = add_fn(name)
        if success:
            list_widget.addItem(name)
            input_field.clear()
        else:
            QMessageBox.critical(self, "Error", "Failed to save record.")
