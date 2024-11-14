from ebooklib import epub
from bs4 import BeautifulSoup
import os


def split_epub_by_chapter(epub_path, output_folder):
    # 打开 EPUB 文件
    book = epub.read_epub(epub_path)
    os.makedirs(output_folder, exist_ok=True)

    chapter_count = 1

    # 遍历书籍的所有项目
    for item in book.get_items():
        # 仅处理 XHTML 类型的章节内容
        if item.media_type == 'application/xhtml+xml':
            # 使用 get_body_content() 获取章节 HTML 内容
            html_content = item.get_body_content().decode("utf-8")  # 解码为字符串
            soup = BeautifulSoup(html_content, 'html.parser')

            # 提取纯文本内容
            text_content = soup.get_text(separator='\n', strip=True)

            # 保存为单独的文本文件
            chapter_filename = f"{output_folder}/chapter_{chapter_count}.txt"
            with open(chapter_filename, "w", encoding="utf-8") as f:
                f.write(text_content)

            print(f"Saved {chapter_filename}")
            chapter_count += 1


# 使用示例
epub_path = 'path_epub_file'  # EPUB文件路径
output_folder = 'output_chapters'  # 保存章节的文件夹
split_epub_by_chapter(epub_path, output_folder)
