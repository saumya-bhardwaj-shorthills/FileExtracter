from loaders.pdf_loader import PDFLoader
from loaders.docx_loader import DOCXLoader
from loaders.ppt_loader import PPTLoader
from loaders.file_loader import FileLoader

class DataExtractor:
    def __init__(self, loader: FileLoader):
        self.loader = loader
        self.file = self.loader.load_file()

    def extract_text(self):
        """Extract text and metadata such as page numbers and font styles."""
        if isinstance(self.loader, PDFLoader):
            return self._extract_text_pdf()
        elif isinstance(self.loader, DOCXLoader):
            return self._extract_text_docx()
        elif isinstance(self.loader, PPTLoader):
            return self._extract_text_ppt()

    def _extract_text_pdf(self):
        texts = []
        for page_num, page in enumerate(self.file.pages, start=1):
            page_text = page.extract_text()
            texts.append({"page": page_num, "text": page_text})
        return texts

    def _extract_text_docx(self):
        texts = []
        for para in self.file.paragraphs:
            texts.append(para.text)
        return texts

    def _extract_text_ppt(self):
        texts = []
        for slide in self.file.slides:
            slide_text = ' '.join([shape.text for shape in slide.shapes if hasattr(shape, "text")])
            texts.append(slide_text)
        return texts

    def extract_links(self):
        """Extract hyperlinks from the document."""
        return []

    def extract_images(self):
        """Extract images from the document."""
        return []

    def extract_tables(self):
        """Extract tables from the document."""
        return []
