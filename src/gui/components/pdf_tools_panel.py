from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import pyqtSlot
import os
from services.pdf_organizer import PDFOrganizer  # noqa: F401 (reserved for integration)
from gui.components.pdf_merge_dialog import PDFMergeDialog


class PDFToolsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pdf_file = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        self.label = QLabel("PDF Tools", self)
        layout.addWidget(self.label)

        self.btn_select_pdf = QPushButton("Select PDF File", self)
        self.btn_select_pdf.clicked.connect(self.select_pdf)
        layout.addWidget(self.btn_select_pdf)

        self.btn_merge_pdfs_simple = QPushButton("Quick Merge PDFs", self)
        self.btn_merge_pdfs_simple.clicked.connect(self.merge_pdfs)
        layout.addWidget(self.btn_merge_pdfs_simple)

        self.btn_merge_pdfs_adv = QPushButton("Advanced Merge (Reorder)", self)
        self.btn_merge_pdfs_adv.clicked.connect(self.open_merge_dialog)
        layout.addWidget(self.btn_merge_pdfs_adv)

        self.setLayout(layout)

    @pyqtSlot()
    def select_pdf(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options
        )
        if file_name:
            self.pdf_file = file_name
            self.label.setText(f"Selected PDF: {os.path.basename(file_name)}")

    @pyqtSlot()
    def merge_pdfs(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select PDF Files to Merge", "", "PDF Files (*.pdf);;All Files (*)", options=options
        )
        if files:
            output_file, _ = QFileDialog.getSaveFileName(
                self, "Save Merged PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options
            )
            if output_file:
                try:
                    from PyPDF2 import PdfMerger
                    merger = PdfMerger()
                    for f in files:
                        merger.append(f)
                    if not output_file.lower().endswith('.pdf'):
                        output_file += '.pdf'
                    merger.write(output_file)
                    merger.close()
                    self.label.setText(
                        f"Merged PDFs saved as: {os.path.basename(output_file)}"
                    )
                except Exception as e:  # pragma: no cover
                    self.label.setText(f"Merge failed: {e}")

    def open_merge_dialog(self):
        dlg = PDFMergeDialog(self)
        dlg.exec_()