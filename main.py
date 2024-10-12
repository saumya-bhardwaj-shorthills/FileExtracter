import os
from loaders.pdf_loader import PDFLoader
from extractors.data_extractor import DataExtractor
from storage.file_storage import FileStorage
import fitz  # PyMuPDF

def main():
    # Path to the PDF file
    pdf_file = "sample2.pdf"  # Replace this with the actual file name

    # Create a PDFLoader instance
    pdf_loader = PDFLoader(pdf_file)

    # Validate the PDF file
    pdf_loader.validate_file()

    # Extract data from the PDF
    extractor = DataExtractor(pdf_loader)
    pdf_text = extractor.extract_text()

    # Extract images from the PDF
    images = extract_images_from_pdf(pdf_file)

    # Close the file after processing
    pdf_loader.close_file()

    # Create a folder for storing the extracted data
    pdf_base_name = os.path.splitext(os.path.basename(pdf_file))[0]
    output_dir = os.path.join("extracted_data", pdf_base_name)
    file_storage = FileStorage(output_dir)

    # Save the extracted text
    file_storage.save(pdf_text, os.path.basename(pdf_file), 'text')

    # Save the extracted images and their metadata
    file_storage.save(images, os.path.basename(pdf_file), 'image')

    print(f"Extracted data saved to: {output_dir}")

def extract_images_from_pdf(pdf_path):
    """Extract existing images from a PDF file using PyMuPDF."""
    images = []
    pdf_document = fitz.open(pdf_path)  # Open the PDF document with PyMuPDF

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image_list = page.get_images(full=True)

        for image_index, img in enumerate(image_list):
            xref = img[0]  # Xref of the image
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            width, height = base_image["width"], base_image["height"]

            # Store the image info
            images.append({
                "image_data": image_bytes,
                "ext": image_ext,
                "page": page_num + 1,
                "dimensions": (width, height)
            })

    pdf_document.close()
    return images

if __name__ == "__main__":
    main()
