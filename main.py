import os
from loaders.pdf_loader import PDFLoader
from extractors.data_extractor import DataExtractor
from storage.file_storage import FileStorage

def main():
    pdf_file = "sample2.pdf"  # Replace this with the actual file name

    # Load and validate the PDF
    pdf_loader = PDFLoader(pdf_file)
    pdf_loader.validate_file()

    # Extract data from the PDF
    extractor = DataExtractor(pdf_loader)
    pdf_text = extractor.extract_text()
    images = extractor.extract_images()
    urls = extractor.extract_urls()

    pdf_loader.close_file()

    # Store the extracted data
    pdf_base_name = os.path.splitext(os.path.basename(pdf_file))[0]
    output_dir = os.path.join("extracted_data", pdf_base_name)
    file_storage = FileStorage(output_dir)

    file_storage.save(pdf_text, pdf_base_name, 'text')
    file_storage.save(images, pdf_base_name, 'image')
    file_storage.save(urls, pdf_base_name, 'url')

    print(f"Extracted data saved to: {output_dir}")

if __name__ == "__main__":
    main()
