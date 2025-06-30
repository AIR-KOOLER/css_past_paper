import os
import html2text
from docx import Document

def html_to_docx(html_path, docx_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = False
    plain_text = text_maker.handle(html_content)

    doc = Document()
    doc.add_paragraph(plain_text)
    doc.save(docx_path)
    print(f"Converted: {html_path} -> {docx_path}")

def convert_all_html_in_dir(directory="."):
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            html_path = os.path.join(directory, filename)
            docx_path = os.path.splitext(html_path)[0] + ".docx"
            html_to_docx(html_path, docx_path)

if __name__ == "__main__":
    convert_all_html_in_dir()
