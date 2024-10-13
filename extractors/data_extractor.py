import fitz  # PyMuPDF for images and URLs
from PyPDF2 import PdfReader

class DataExtractor:
    def __init__(self, pdf_loader):
        self.pdf_loader = pdf_loader
        self.pdf_reader = pdf_loader.load_file()
        self.pdf_path = pdf_loader.file_path

    def extract_text(self):
        """Extract text using PyPDF2."""
        text = []
        for page in self.pdf_reader.pages:
            text.append(page.extract_text())
        return text

    def extract_images(self):
        """Extract images from the PDF using PyMuPDF."""
        images = []
        pdf_document = fitz.open(self.pdf_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            image_list = page.get_images(full=True)
            for img in image_list:
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                images.append({
                    "image_data": base_image["image"],
                    "ext": base_image["ext"],
                    "page": page_num + 1,
                    "dimensions": (base_image["width"], base_image["height"])
                })
        pdf_document.close()
        return images

    def extract_urls(self):
        """Extract URLs from the PDF using PyMuPDF."""
        urls = []
        pdf_document = fitz.open(self.pdf_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            links = page.get_links()
            for link in links:
                if "uri" in link:
                    rect = link["from"]
                    urls.append({
                        "url": link["uri"],
                        "page": page_num + 1,
                        "position": {
                            "x0": rect.x0, "y0": rect.y0, "x1": rect.x1, "y1": rect.y1
                        }
                    })
        pdf_document.close()
        return urls
