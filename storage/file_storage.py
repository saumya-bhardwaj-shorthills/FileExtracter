import os
import json
import fitz  # PyMuPDF
from storage.storage import Storage

class FileStorage(Storage):
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def save(self, data, filename: str, data_type: str):
        """Save data based on type: 'text' or 'image'."""
        if data_type == 'text':
            self.save_text(data, filename)
        elif data_type == 'image':
            self.save_images(data, filename)
        else:
            raise ValueError("Unsupported data type. Use 'text' or 'image'.")

    def save_text(self, data, filename: str):
        """Save extracted text as a .txt file with the same name as the PDF."""
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(self.output_dir, txt_filename)
        
        with open(output_path, 'w') as f:
            if isinstance(data, list):
                for line in data:
                    f.write(f"{line}\n")
            else:
                f.write(data)
    
    def save_images(self, images, filename: str):
        """Save extracted images and their metadata."""
        images_dir = os.path.join(self.output_dir, "images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        metadata = []
        for idx, image_info in enumerate(images):
            image_filename = f"image_{idx + 1}.{image_info['ext']}"
            image_path = os.path.join(images_dir, image_filename)

            # Save the image to file
            with open(image_path, "wb") as img_file:
                img_file.write(image_info["image_data"])

            # Collect metadata
            metadata.append({
                "file_name": image_filename,
                "page_number": image_info["page"],
                "dimensions": image_info["dimensions"]
            })

        # Save metadata to a JSON file
        metadata_file = os.path.join(images_dir, 'metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=4)
