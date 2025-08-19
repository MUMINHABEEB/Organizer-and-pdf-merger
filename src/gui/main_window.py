from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QAction, QMessageBox
from gui.components.file_naming_panel import FileNamingPanel
from gui.components.folder_organizer_panel import FolderOrganizerPanel
from gui.components.pdf_tools_panel import PDFToolsPanel
from gui.components.settings_dialog import SettingsDialog
from gui.about_dialog import AboutDialog
from gui.widgets.branded_background import BrandedBackground


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Automation Suite")
        self.setGeometry(100, 100, 800, 600)

        # Core container inside branded background
        self._core_widget = QWidget()
        core_layout = QVBoxLayout(self._core_widget)
        core_layout.setContentsMargins(16, 16, 16, 16)
        core_layout.setSpacing(16)

        self.central_widget = BrandedBackground(self._core_widget)
        self.setCentralWidget(self.central_widget)

        # Panels
        self.file_naming_panel = FileNamingPanel()
        self.folder_organizer_panel = FolderOrganizerPanel()
        self.pdf_tools_panel = PDFToolsPanel()

        core_layout.addWidget(self.file_naming_panel)
        core_layout.addWidget(self.folder_organizer_panel)
        core_layout.addWidget(self.pdf_tools_panel)

        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings_dialog)
        file_menu.addAction(settings_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.open_about)
        help_menu.addAction(about_action)

    def open_settings_dialog(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

    def show_error(self, message: str):
        QMessageBox.critical(self, "Error", message)

    def show_info(self, message: str):
        QMessageBox.information(self, "Information", message)

    def open_about(self):
        dlg = AboutDialog(self, version="0.1.0")
        dlg.exec_()

    def resizeEvent(self, event):  # noqa: D401
        super().resizeEvent(event)