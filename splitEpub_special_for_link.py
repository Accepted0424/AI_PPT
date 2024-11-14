# 由于《链接》这本书的有些杂乱，故单独写了个程序对该书进行特殊优化
# 1.去除推荐序、序言、注释等无用内容，仅保留章节
# 2.epub文件中的第一链分割混乱，对第一链进行特殊优化

from ebooklib import epub
from bs4 import BeautifulSoup
import os
import re


def split_epub_by_chapter(epub_path, output_folder):
    # 打开 EPUB 文件
    book = epub.read_epub(epub_path)
    os.makedirs(output_folder, exist_ok=True)

    chapter_count = 1
    first_chapter_content = []
    # 遍历书籍的所有项目
    for item in book.get_items():
        # 仅处理 XHTML 类型的章节内容
        if item.media_type == 'application/xhtml+xml':
            # 获取章节 HTML 内容
            html_content = item.get_body_content().decode("utf-8")
            soup = BeautifulSoup(html_content, 'html.parser')

            # 获取章节文本前两行
            lines = soup.get_text(separator='\n', strip=True).splitlines()
            first_two_lines = lines[:2] if len(lines) >= 2 else lines
            first_line = first_two_lines[0] if first_two_lines else ''

            target_strings = ["第1链","让雅虎网站瘫痪的少年黑客", "社会网络与基督教的兴起", "复杂网络的力量","谁在支配网络的结构与演化","当还原论撞上复杂性","探寻下一个大变革"]
            first_chapter_found = any(target_string in first_line for target_string in target_strings)

            # 判断是否包含“第x链”格式的内容
            other_chapter_found = any(re.search(r'第[0123456789]+链', line) for line in first_two_lines)
            # 跳过“注释”部分
            if any("注释" in line for line in first_two_lines):
                continue

            if first_chapter_found:
                first_chapter_content += lines
                first_chapter_content += ' '
                if "探寻下一个大变革" in first_line:
                    chapter_filename = f"{output_folder}/chapter_{chapter_count}.txt"
                    with open(chapter_filename, "w", encoding="utf-8") as f:
                        f.write('\n'.join(first_chapter_content))  # 保存整个章节内容

                    print(f"Saved {chapter_filename}")
                    chapter_count += 1
            # 如果符合条件，则保存该章节
            elif other_chapter_found:
                chapter_filename = f"{output_folder}/chapter_{chapter_count}.txt"
                with open(chapter_filename, "w", encoding="utf-8") as f:
                    f.write('\n'.join(lines))  # 保存整个章节内容

                print(f"Saved {chapter_filename}")
                chapter_count += 1


# 使用示例
epub_path = 'link.epub'  # EPUB文件路径
output_folder = 'output_link_chapters'  # 保存章节的文件夹
split_epub_by_chapter(epub_path, output_folder)
