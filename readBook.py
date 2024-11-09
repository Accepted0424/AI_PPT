import os
import docx
import ebooklib
from PyPDF2 import PdfReader
from ebooklib import epub
from bs4 import BeautifulSoup


# 处理 TXT 文件
def read_txt(book_path):
    with open(book_path, 'r', encoding='utf-8') as file:
        return file.read()


# 处理 PDF 文件
def read_pdf(book_path):
    pdf_reader = PdfReader(book_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# 处理 DOCX 文件
def read_docx(book_path):
    doc = docx.Document(book_path)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text


# 处理 EPUB 文件
def read_epub(book_path):
    book = epub.read_epub(book_path)
    text = ''
    # 遍历所有的 HTML 文件并提取文本
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, 'html.parser')
            text += soup.get_text() + '\n'
    return text


# 主函数，判断文件扩展名并调用相应的读取方法
def read_file(book_path):
    if not os.path.exists(book_path):
        return "文件不存在"

    file_extension = os.path.splitext(book_path)[1].lower()

    if file_extension == '.txt':
        return read_txt(book_path)
    elif file_extension == '.pdf':
        return read_pdf(book_path)
    elif file_extension == '.docx':
        return read_docx(book_path)
    elif file_extension == '.epub':
        return read_epub(book_path)
    else:
        return "不支持的文件格式"
