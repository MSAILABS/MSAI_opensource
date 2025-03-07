import numpy as np
import os
import PyPDF2
from docx.document import Document
import textract
from docx import Document
import easyocr
from PIL import Image
import io

def extract_text_from_docx(file_path):
    doc: Document = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    full_text.append("===msai-labs page break===")
    return '\n'.join(full_text)

def extract_text_from_doc(file_path):
    text = textract.process(file_path)
    full_text = text.decode('utf-8')
    full_text += "\n===msai-labs page break==="
    return full_text

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        full_text = file.read()
    full_text += "\n===msai-labs page break==="
    return full_text

def extract_text_from_pdf(file_path):
    dir_path = os.path.join(os.getcwd(), "easy_ocr_model") 

    os.makedirs(dir_path, exist_ok=True)

    reader = easyocr.Reader(["en"], model_storage_directory=dir_path)
    pdf_reader = PyPDF2.PdfReader(file_path)
    full_text = []
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        full_text.append(" ".join(page.extract_text().split("\n")))
        images = page.images
        for image in images:
            base_image = image.data
            image_bytes = io.BytesIO(base_image)
            pil_image = Image.open(image_bytes).convert('RGB')
            numpy_image = np.array(pil_image)
            
            result = reader.readtext(numpy_image, detail=0)
            full_text.append("\n".join(result))
        full_text.append("===msai-labs page break===")
    
    unique_list = []
    for item in full_text:
        if item not in unique_list:
            unique_list.append(item)
        elif item == "===msai-labs page break===":
            unique_list.append(item)

    
    return '\n'.join(unique_list)

def extract_text(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension == '.doc':
        return extract_text_from_doc(file_path)
    elif file_extension == '.txt':
        return extract_text_from_txt(file_path)
    elif file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")

# Example usage:
# text = extract_text('/path/to/your/file.docx')
# print(text)