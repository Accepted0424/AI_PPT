import warnings
import docx
import os
import re
import fitz
from ebooklib import epub
from bs4 import BeautifulSoup


# 处理 TXT 文件
def read_txt(book_path):
    with open(book_path, 'r', encoding='utf-8') as file:
        return file.read()


# 处理 PDF 文件
def read_pdf(book_path):
    """读取PDF文件内容"""
    # 打开 PDF 文件
    document = fitz.open(book_path)
    text = ''
    # 遍历每一页
    for page_num in range(len(document)):
        page = document.load_page(page_num)  # 加载页面
        page_text = page.get_text("text")  # 提取文本
        # 使用正则表达式匹配前面一个字符不是 "。" 的 \n
        pattern = r'(?<!。)\n'
        # 替换匹配到的 \n 为空字符串
        page_text = re.sub(pattern, '', page_text)
        text = text + page_text
    # 关闭文档
    document.close()
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
    # 打开 EPUB 文件
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    book = epub.read_epub(book_path)

    text = ""
    # 遍历书籍的所有项目
    for item in book.get_items():
        # 仅处理 XHTML 类型的章节内容
        if item.media_type == 'application/xhtml+xml':
            # 使用 get_body_content() 获取章节 HTML 内容
            html_content = item.get_body_content().decode("utf-8")  # 解码为字符串
            soup = BeautifulSoup(html_content, 'html.parser')
            # 提取纯文本内容
            text += soup.get_text(separator='\n', strip=True)
    return text


# 主函数，判断文件扩展名并调用相应的读取方法
def read_file(book_path):
    if not os.path.exists(book_path):
        raise FileNotFoundError

    file_extension = os.path.splitext(book_path)[1].lower()
    if file_extension == '.txt':
        file_content = read_txt(book_path)
    elif file_extension == '.pdf':
        file_content = read_pdf(book_path)
    elif file_extension == '.docx':
        file_content = read_docx(book_path)
    elif file_extension == '.epub':
        file_content = read_epub(book_path)
    else:
        raise FileNotFoundError
    with open("text.txt", 'w', encoding='utf-8') as file:
        file.write(file_content)
    return file_content


if __name__ == "__main__":
    print(read_file("link.epub"))
