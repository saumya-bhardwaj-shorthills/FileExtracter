import os
from PyPDF2 import PdfReader
from loaders.file_loader import FileLoader

class PDFLoader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.file = None

    def validate_file(self):
        # Check if the file exists and has a .pdf extension
        if not os.path.exists(self.file_path):
            raise ValueError(f"File not found: {self.file_path}")
        if not self.file_path.lower().endswith(".pdf"):
            raise ValueError(f"Invalid file type: {self.file_path} is not a PDF file.")
        return True

    def load_file(self):
        try:
            # Open the file and store it in the class instance to keep it open
            self.file = open(self.file_path, "rb")
            reader = PdfReader(self.file)
            return reader
        except Exception as e:
            print(f"Error loading PDF file: {e}")
            return None

    def close_file(self):
        # Close the file manually when you're done with it
        if self.file:
            self.file.close()
