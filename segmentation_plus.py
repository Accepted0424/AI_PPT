import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


def create_directory(name):
    if not os.path.exists(name):
        os.makedirs(name)


def save_text_to_file(text, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


def parse_epub(epub_path, output_dir):
    try:
        book = epub.read_epub(epub_path)
        chapter_hierarchy = {}

        # 遍历所有项目
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                print(headings)

                current_path = []
                for heading in headings:
                    level = int(heading.name[1])
                    title = heading.text.strip()

                    while len(current_path) >= level:
                        current_path.pop()

                    current_path.append(title)
                    path = os.path.join(output_dir, *current_path[:-1])
                    create_directory(path)

                    if len(current_path) == level:  # 当前是叶子节点
                        content = '\n'.join([str(p) for p in heading.find_next_siblings()])
                        filename = os.path.join(path, f"{title}.txt")
                        save_text_to_file(content, filename)

        print("转换完成！")

    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    epub_path = r'C:\桌面\科研课堂\链接.epub'  # EPUB 文件路径
    output_dir = r'D:\pythonProject\AI_PPT\result'  # 输出目录
    parse_epub(epub_path, output_dir)