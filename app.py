from pypdf import PdfReader 
from pdf2image import convert_from_path
import os
reader = PdfReader('C:\\Users\\Lenovo\\Downloads\\transformer.pdf')
print(len(reader.pages))
page = reader.pages[0]
text = page.extract_text()
print(text)

def extract_images(pdf_path, output_folder):
    poppler_path=r'C:\Program Files (x86)\poppler-24.08.0\Library\bin'
    images = convert_from_path(pdf_path,poppler_path=poppler_path)
    os.makedirs(output_folder, exist_ok=True)
    for i, image in enumerate(images):
        image.save(f"{output_folder}/page_{i+1}.png", "PNG")
        print(f"Saved page_{i+1}.png")
path=r'C:\\Users\\Lenovo\\Downloads\\transformer.pdf'
img_collc='C:\\Users\\Lenovo\\Downloads\\pdf_images'

extract_images(path,img_collc)



