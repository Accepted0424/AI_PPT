import os
import re
from ebooklib import epub
from bs4 import BeautifulSoup


def read_pdf(file_path):
    """读取Epub文件内容"""
    # 打开 EPUB 文件
    book = epub.read_epub(file_path)
    text = ''
    # 遍历书籍的所有项目
    for item in book.get_items():
        # 仅处理 XHTML 类型的章节内容
        if item.media_type == 'application/xhtml+xml':
            # 使用 get_body_content() 获取章节 HTML 内容
            html_content = item.get_body_content().decode("utf-8")  # 解码为字符串
            soup = BeautifulSoup(html_content, 'html.parser')
            # 提取纯文本内容
            text_content = soup.get_text(separator='\n', strip=True)
            # 使用正则表达式匹配前面一个字符不是 "。" 的 \n
            pattern = r'(?<!。)\n'
            # 替换匹配到的 \n 为空字符串
            text_content = re.sub(pattern, '', text_content)
            text = text + text_content

    # 去掉没有意义的空白符
    text = text.replace(' ', '')
    text = text.replace('\t', '')
    text = text.replace('\r', '')
    text = text.replace('\f', '')
    text = text.replace('\v', '')
    # 缩进
    text = text.replace('\n', '\n  ')
    with open("text.txt", 'w', encoding='utf-8') as file:
        file.write(text)
    return text


def split_text_by_keywords(text, keywords, number):
    # 使用正则表达式处理空白符，去除多余的空格、换行等
    keywords = [re.sub(r'\s+', '', keyword).strip() for keyword in keywords]  # 处理多个关键词的空白符
    # 创建一个正则表达式，匹配任何一个关键词
    keyword_pattern = '|'.join([re.escape(keyword) for keyword in keywords])  # 用 | 连接多个关键词，进行或匹配
    # 使用正则表达式匹配多个关键词，并分割文本
    parts = re.split(f'({keyword_pattern})', text)  # 用括号捕获关键词本身，并匹配空白符

    merged_parts=[]

    part_flag = 1
    if part_flag in number:
        merged_parts.append(parts[0])

    for i in range(1, len(parts)-1, 2):
        part_flag = part_flag + 1
        if part_flag in number:
            # 缩进
            merged_parts.append('  ' + parts[i] + parts[i+1] + '\n')
    return merged_parts


def save_parts_to_txt(parts, output_folder, prefix='part_'):
    """将分割后的文本部分保存为txt文件"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, part in enumerate(parts):
        file_name = f"{prefix}{i}.txt"
        file_path = os.path.join(output_folder, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(part)

def split_pdf(file_path, keywords, number, output_folder):
    pdf_content = read_pdf(file_path)
    parts = split_text_by_keywords(pdf_content, keywords, number)
    save_parts_to_txt(parts, output_folder)

if __name__ == "__main__":
    pdf_file = r'C:\桌面\科研课堂\链接.epub'
    # keywords 和 number从昊霖的输入中得到
    #幂律，复杂网络背后的规律
    #富者愈富——复杂网络的先发优势
    #爱因斯坦的馈赠——复杂网络的新星效应
    keywords = ['第6链 幂律——复杂网络的分布规律40年前，埃尔德什和莱利将复杂网络放到“随机”灌木丛中，而幂律将复杂网络从中拉了出来，并将其放到色彩斑斓、内涵丰富的“自组织”舞台上。',
                '第7链 富者愈富——复杂网络的先发优势在我们不得不引入生长机制之前，经典模型的静态特性一直没有人注意；在幂律要求我们引入偏好连接之前，随机性也不是什么问题。',
                '第8链 爱因斯坦的馈赠——复杂网络的新星效应在大多数复杂系统中，每个节点都有各自的特性。']
    number = [2,3]
    output_folder =  r'D:\pythonProject\AI_PPT\split_chapters'
    split_pdf(pdf_file, keywords, number, output_folder)