import os
from docx import Document

def convert_txt_to_docx(txt_folder, docx_folder):
    if not os.path.exists(docx_folder):
        os.makedirs(docx_folder)
    for filename in os.listdir(txt_folder):
        if filename.endswith('.txt'):
            txt_file_path = os.path.join(txt_folder, filename)
            docx_file_path = os.path.join(docx_folder, filename.replace('.txt', '.docx'))
            with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
                content = txt_file.read()
            doc = Document()
            doc.add_paragraph(content)
            doc.save(docx_file_path)
            print(f"Сохранен файл: {docx_file_path}")


