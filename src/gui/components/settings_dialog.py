from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel("Customize your settings:")
        self.layout.addWidget(self.label)

        self.theme_label = QLabel("Select Theme:")
        self.layout.addWidget(self.theme_label)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "System Default"])
        self.layout.addWidget(self.theme_combo)

        self.auto_save_checkbox = QCheckBox("Enable Auto Save")
        self.layout.addWidget(self.auto_save_checkbox)

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def save_settings(self):
        selected_theme = self.theme_combo.currentText()
        auto_save_enabled = self.auto_save_checkbox.isChecked()
        # Here you would typically save these settings to a config file or database
        print(f"Settings saved: Theme - {selected_theme}, Auto Save - {auto_save_enabled}")
        self.accept()