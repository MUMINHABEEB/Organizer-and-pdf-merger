from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QCheckBox, QComboBox
from services.folder_organizer import FolderOrganizer


class FolderOrganizerPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.folder_organizer = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Folder Organizer")
        layout.addWidget(self.label)

        self.select_folder_button = QPushButton("Select Folder")
        self.select_folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.select_folder_button)

        self.dry_run_checkbox = QCheckBox("Dry run (show what would happen, no moves)")
        self.dry_run_checkbox.setChecked(True)
        layout.addWidget(self.dry_run_checkbox)

        # Scheme selector
        self.scheme_label = QLabel("Destination scheme:")
        layout.addWidget(self.scheme_label)
        self.scheme_combo = QComboBox()
        self.scheme_combo.addItem("Standard (YYYY/MM/DD/Client/Type)", userData="standard")
        self.scheme_combo.addItem("Sample (YYYY/MON/DD-MM-YYYY/Client/Type)", userData="sample")
        self.scheme_combo.setCurrentIndex(0)
        layout.addWidget(self.scheme_combo)

        self.organize_button = QPushButton("Organize Folder")
        self.organize_button.clicked.connect(self.organize_folder)
        layout.addWidget(self.organize_button)

        self.setLayout(layout)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            scheme = self.scheme_combo.currentData() or "standard"
            self.folder_organizer = FolderOrganizer(
                folder_path,
                dry_run=self.dry_run_checkbox.isChecked(),
                scheme=scheme,
            )
            QMessageBox.information(self, "Folder Selected", f"Selected folder: {folder_path}")

    def organize_folder(self):
        try:
            if not self.folder_organizer:
                QMessageBox.warning(self, "No folder", "Please select a folder first.")
                return
            # keep dry-run setting in sync
            self.folder_organizer.dry_run = self.dry_run_checkbox.isChecked()
            # keep scheme in sync
            self.folder_organizer.scheme = self.scheme_combo.currentData() or "standard"
            summary = self.folder_organizer.run()
            first_errors = summary.get("first_errors") or []
            err_text = ("\nFirst errors:\n" + "\n".join(first_errors[:5])) if first_errors else ""
            skipped_all = summary.get("skipped_all")
            skip_reason = summary.get("skip_reason", "")
            msg = (
                f"Dry run: {'Yes' if summary.get('dry_run') else 'No'}\n"
                f"Total files: {summary.get('total')}\n"
                f"Moved (or would move): {summary.get('moved')}\n"
                f"Copied only (source locked): {summary.get('copied_only', 0)}\n"
                f"Skipped: {summary.get('skipped', 0)}\n"
                f"Errors: {summary.get('errors')}\n"
                f"{err_text}\n\n"
                + (f"Note: Skipped entire folder — {skip_reason}\n\n" if skipped_all else "")
                + "Results are placed under '_organized' when not a dry run."
            )
            QMessageBox.information(self, "Organizer Summary", msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")