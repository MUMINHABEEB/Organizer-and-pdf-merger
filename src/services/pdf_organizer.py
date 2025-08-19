import os

# Support both PyPDF2>=2 (PdfReader/PdfWriter) and legacy 1.x
try:
    from PyPDF2 import PdfReader, PdfWriter  # type: ignore
except Exception:  # pragma: no cover - fallback for old versions
    import PyPDF2  # type: ignore
    PdfReader = PyPDF2.PdfFileReader
    PdfWriter = PyPDF2.PdfFileWriter

class PDFOrganizer:
    def __init__(self, source_folder, destination_folder):
        self.source_folder = source_folder
        self.destination_folder = destination_folder

    def organize_pdfs(self):
        if not os.path.exists(self.destination_folder):
            os.makedirs(self.destination_folder)

        for filename in os.listdir(self.source_folder):
            if filename.endswith('.pdf'):
                self.process_pdf(filename)

    def process_pdf(self, filename):
        pdf_path = os.path.join(self.source_folder, filename)
        # Open and copy pages in a version-tolerant way
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            pages = getattr(reader, "pages", None)
            if pages is None:
                # Legacy API
                with open(pdf_path, "rb") as fp:
                    reader = PdfReader(fp)
                    page_count = getattr(reader, "numPages", 0)
                    for i in range(page_count):
                        page = reader.getPage(i)
                        add = getattr(writer, "addPage", getattr(writer, "add_page", None))
                        if add:
                            add(page)
            else:
                for page in pages:
                    add = getattr(writer, "add_page", getattr(writer, "addPage", None))
                    if add:
                        add(page)
        except Exception:
            # As a last resort, try legacy import style
            import PyPDF2  # type: ignore
            with open(pdf_path, "rb") as fp:
                reader = PyPDF2.PdfFileReader(fp)
                writer = PyPDF2.PdfFileWriter()
                for i in range(reader.numPages):
                    writer.addPage(reader.getPage(i))

        new_filename = self.generate_new_filename(filename)
        new_pdf_path = os.path.join(self.destination_folder, new_filename)

        with open(new_pdf_path, 'wb') as output_pdf:
            # Handle both write APIs
            write = getattr(writer, "write", None)
            if write:
                write(output_pdf)
            else:
                writer.write(output_pdf)

    def generate_new_filename(self, original_filename):
        base_name = os.path.splitext(original_filename)[0]
        new_name = f"{base_name}_organized.pdf"
        return new_name

# Example usage:
# organizer = PDFOrganizer('path/to/source', 'path/to/destination')
# organizer.organize_pdfs()