import os
import re
from PyPDF2 import PdfReader


def read_pdf(file_path):
    """读取PDF文件内容"""
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text().replace('\n', '') + '\n'
    text = re.sub(r' ', '', text).strip()  # 将所有空白符替换成单一空格并去除首尾空白
    return text


def split_text_by_keywords(text, keywords, number):
    # 处理关键词，去除多余的空格
    keywords = [re.sub(r'\s+', '', keyword).strip() for keyword in keywords]

    # 创建正则表达式，用 | 连接多个关键词进行匹配
    keyword_pattern = '|'.join([re.escape(keyword) for keyword in keywords])

    # 使用正则表达式分割文本，并捕获关键词
    parts = re.split(rf'\s*({keyword_pattern})\s*', text)

    # 过滤掉空白部分
    parts = [part.strip() for part in parts if part.strip()]

    # 合并分割后的文本
    merged_parts = []

    # 初始化 part_flag，假设部分从1开始
    part_flag = 1
    # 判断第一个部分是否应该合并
    if part_flag in number and len(parts) > 0:
        merged_parts.append(parts[0])

    # 遍历分割后的文本部分，进行合并
    for i in range(1, len(parts) - 1, 2):  # 每次跳过两个元素，一个是关键词，一个是文本
        part_flag += 1
        if part_flag in number and i + 1 < len(parts):
            # 合并关键词和文本，并加入到 merged_parts
            merged_parts.append(parts[i] + parts[i + 1] + '\n')

    # 如果 merged_parts 为空，则抛出异常
    if not merged_parts:
        raise Exception

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
    save_parts_to_txt(parts, output_folder, prefix='part_')


if __name__ == "__main__":
    pdf_file = r'link_all.pdf'
    # keywords 和 number从昊霖的输入中得到
    # 幂律，复杂网络背后的规律
    # 富者愈富——复杂网络的先发优势
    # 爱因斯坦的馈赠——复杂网络的新星效应
    keywords = [
        '第6链 幂律——复杂网络的分布规律40年前，埃尔德什和莱利将复杂网络放到“随机”灌木丛中，而幂律将复杂网络从中拉了出来，并将其放到色彩斑斓、内涵丰富的“自组织”舞台上。盯着微型搜索引擎带回来的幂律，我们在网络中看到了一种全新而未知的秩序，这种秩序具有不同寻常的优美和一致性。',
        '第7链 富者愈富——复杂网络的先发优势在我们不得不引入生长机制之前，经典模型的静态特性一直没有人注意；在幂律要求我们引入偏好连接之前，随机性也不是什么问题。结构和网络演化不能彼此分开，认识到这一点之后，我们很难再回到主宰我们思维方式几十年之久的静态模型。这种思维方式的转变缔造了一组反义词：静态和生长，随机和无尺度，结构和演化。',
        '第8链 爱因斯坦的馈赠——复杂网络的新星效应在大多数复杂系统中，每个节点都有各自的特性。有些节点虽然出现得很晚，却能在很短的时间内攫取所有链接。其他节点虽然出现得早，却没有获得很多链接，未能利用其先发优势成为枢纽节点。如果我们想要解释在大多数网络中所看到的激烈竞争，就不得不承认每个节点都是不同的。']
    number = [2, 3]
    output_folder = r'split_chapters'
    split_pdf(pdf_file, keywords, number, output_folder)
