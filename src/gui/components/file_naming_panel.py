from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QFileDialog,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
from services.file_naming import (
    generate_file_name,
    rename_files_in_directory,
)


class FileNamingPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._target_folder = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("File Naming Automation")

        layout = QVBoxLayout()

        label = QLabel("Base Name:")
        layout.addWidget(label)

        self.file_name_input = QLineEdit(self)
        layout.addWidget(self.file_name_input)

        dir_row = QHBoxLayout()
        self.dir_label = QLabel("Target Folder: (choose)")
        dir_row.addWidget(self.dir_label)
        self.btn_browse = QPushButton("Browse…", self)
        self.btn_browse.clicked.connect(self.pick_folder)
        dir_row.addWidget(self.btn_browse)
        layout.addLayout(dir_row)

        self.preview_button = QPushButton("Preview Name", self)
        self.preview_button.clicked.connect(self.preview_name)
        layout.addWidget(self.preview_button)

        self.apply_button = QPushButton("Rename Files in Folder", self)
        self.apply_button.clicked.connect(self.apply_bulk)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def pick_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select target folder")
        if folder:
            self.dir_label.setText(f"Target Folder: {folder}")
            self._target_folder = folder

    def preview_name(self):
        base = self.file_name_input.text().strip()
        if not base:
            QMessageBox.warning(self, "Input Error", "Please enter a base name.")
            return
        name = generate_file_name(base, include_date=True, index=1, ext="txt")
        QMessageBox.information(self, "Preview", f"Example: {name}")

    def apply_bulk(self):
        base = self.file_name_input.text().strip()
        folder = self._target_folder
        if not base:
            QMessageBox.warning(self, "Input Error", "Please enter a base name.")
            return
        if not folder:
            QMessageBox.warning(self, "Select Folder", "Please choose a target folder.")
            return
        try:
            count = rename_files_in_directory(folder, base, include_date=True)
            QMessageBox.information(self, "Done", f"Renamed {count} files in:\n{folder}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))