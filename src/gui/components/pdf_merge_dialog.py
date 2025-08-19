from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QFileDialog,
    QMessageBox, QListWidgetItem, QLabel
)
from PyQt5.QtCore import Qt
import os


class PDFMergeDialog(QDialog):
    """Interactive PDF merge dialog inspired by the provided Tkinter code.

    Features:
      - Add PDFs (multi-select)
      - Remove Selected
      - Remove All
      - Reorder (Move Up / Move Down)
      - Merge to chosen output file with default name derived from first PDF
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Merge PDFs")
        self.setModal(True)
        self.resize(600, 420)

        self.pdf_files = []  # full paths

        layout = QVBoxLayout(self)
        self.info_label = QLabel("Add PDF files in the order you want them merged.")
        layout.addWidget(self.info_label)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(self.list_widget.SingleSelection)
        layout.addWidget(self.list_widget)

        # Button rows
        row1 = QHBoxLayout()
        self.btn_add = QPushButton("Add PDFs")
        self.btn_add.clicked.connect(self.add_pdfs)
        row1.addWidget(self.btn_add)

        self.btn_remove = QPushButton("Remove Selected")
        self.btn_remove.clicked.connect(self.remove_selected)
        row1.addWidget(self.btn_remove)

        self.btn_remove_all = QPushButton("Remove All")
        self.btn_remove_all.clicked.connect(self.remove_all)
        row1.addWidget(self.btn_remove_all)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        self.btn_up = QPushButton("Move Up")
        self.btn_up.clicked.connect(self.move_up)
        row2.addWidget(self.btn_up)

        self.btn_down = QPushButton("Move Down")
        self.btn_down.clicked.connect(self.move_down)
        row2.addWidget(self.btn_down)

        self.btn_merge = QPushButton("Merge PDFs")
        self.btn_merge.clicked.connect(self.merge_pdfs)
        row2.addWidget(self.btn_merge)
        layout.addLayout(row2)

        close_row = QHBoxLayout()
        close_row.addStretch(1)
        self.btn_close = QPushButton("Close")
        self.btn_close.clicked.connect(self.reject)
        close_row.addWidget(self.btn_close)
        layout.addLayout(close_row)

    # --- actions ---

    def add_pdfs(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF Files", "", "PDF Files (*.pdf)")
        for f in files:
            if f and f not in self.pdf_files:
                self.pdf_files.append(f)
                self.list_widget.addItem(QListWidgetItem(os.path.basename(f)))
        self._update_info()

    def remove_selected(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        self.list_widget.takeItem(row)
        self.pdf_files.pop(row)
        self._update_info()

    def remove_all(self):
        self.list_widget.clear()
        self.pdf_files.clear()
        self._update_info()

    def move_up(self):
        row = self.list_widget.currentRow()
        if row <= 0:
            return
        self._swap_rows(row, row - 1)

    def move_down(self):
        row = self.list_widget.currentRow()
        if row < 0 or row >= len(self.pdf_files) - 1:
            return
        self._swap_rows(row, row + 1)

    def _swap_rows(self, a, b):
        self.pdf_files[a], self.pdf_files[b] = self.pdf_files[b], self.pdf_files[a]
        a_item = self.list_widget.item(a).text()
        b_item = self.list_widget.item(b).text()
        self.list_widget.item(a).setText(b_item)
        self.list_widget.item(b).setText(a_item)
        self.list_widget.setCurrentRow(b)

    def merge_pdfs(self):
        if not self.pdf_files:
            QMessageBox.warning(self, "No PDFs", "Please add PDF files to merge.")
            return
        try:
            from PyPDF2 import PdfMerger
        except Exception as e:  # pragma: no cover
            QMessageBox.critical(self, "Dependency Error", f"PyPDF2 not available: {e}")
            return

        # Default output name based on first file
        first_base = os.path.splitext(os.path.basename(self.pdf_files[0]))[0]
        default_name = f"{first_base}_merged.pdf"
        out_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Merged PDF",
            default_name,
            "PDF Files (*.pdf)"
        )
        if not out_path:
            return

        merger = PdfMerger()
        try:
            for pdf in self.pdf_files:
                merger.append(pdf)
            merger.write(out_path)
        except Exception as e:
            QMessageBox.critical(self, "Merge Failed", f"Failed to merge PDFs: {e}")
            return
        finally:
            try:
                merger.close()
            except Exception:
                pass

        QMessageBox.information(self, "Success", f"Merged PDF saved to: {out_path}")

    def _update_info(self):
        count = len(self.pdf_files)
        self.info_label.setText(f"{count} file(s) queued.")
