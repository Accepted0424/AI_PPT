import ebooklib
from ebooklib import epub
import os
from bs4 import BeautifulSoup

def split_epub_to_txt(input_file, output_folder):
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 读取原始EPUB文件
    book = epub.read_epub(input_file)

    # 初始化章节计数器
    chapter_count = 1
    # 遍历每个项目（通常是HTML文件）
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')

            # 假设每个<h1>标签代表一个新的章节
            chapters = soup.find_all('h1')
            # 每遇到一个<h1>标签，就创建一个新的txt文件
            for chapter in chapters:
                chapter_title = chapter.get_text().strip()
                print(chapter_count)
                print(f"Chapter Title: {chapter_title}")

                # 提取章节内容
                chapter_content = []
                next_node = chapter.next_sibling
                while next_node is not None and next_node.name != 'h1':
                    if isinstance(next_node, str):
                        # 如果是字符串节点，直接添加
                        chapter_content.append(next_node.strip())
                    elif next_node.name is not None:
                        # 如果是非字符串节点，提取其文本内容
                        chapter_content.append(next_node.get_text().strip())
                    next_node = next_node.next_sibling

                # chapter_text = BeautifulSoup(''.join(chapter_content), 'html.parser').get_text().strip()
                # 将章节内容列表合并为一个字符串
                chapter_text = '\n'.join(chapter_content)
                print(chapter_text)
                print(f"Chapter Content: {chapter_text}")
                print("\n")
                # 写入txt文件
                output_file = os.path.join(output_folder, f'{chapter_title}.txt')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(chapter_text)

                chapter_count += 1

# 使用函数
input_file = r'C:\桌面\科研课堂\链接.epub'
output_folder = r'D:\pythonProject\AI_PPT\result'
split_epub_to_txt(input_file, output_folder)