import re
from getPicture import call_image_downloader


def read_file(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content


def write_file(md_path, content):
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)


def search_picture(content, i):
    new_content = ''
    for line in content.split('\n'):
        line_temp = line.strip()
        if line != '' and line_temp[0] == '*' and line_temp[-1] != '*':
            match = None
        else:
            match = re.fullmatch(r'\*?\s*\(([^()*]+)\)\s*\*?', line_temp)
        if match:
            pic_query = match.group(1)
            pic_query = pic_query.strip()
            try:
                image_path = call_image_downloader(pic_query, f"picture/part_{i}")
                new_line = f"![{pic_query}](.\\picture\\part_{i}\\{image_path})\n"
                new_content += new_line
            except:
                new_content += line + '\n'
        elif line.startswith('---'):
            pass
        else:
            new_content += line + '\n'
    return new_content


def format_url(content):
    new_content = ''
    for block in re.split(r'(#{1,3})', content):
        new_block = ''
        url_list = []
        for line in block.split('\n'):
            matches = re.findall(r'!\[[^\]]+\]\([^\)]+\)', line)
            if matches:
                for match in matches:
                    url_list.append(match)
            elif re.fullmatch(r'#{1,3}', line.strip()):
                new_block += line.strip()
            else:
                new_block += line + '\n'
        if len(url_list) == 1:
            new_block += url_list[0] + '\n\n'
        elif len(url_list) > 1:
            new_block += '|' + ('|'.join(url_list)) + '|' + '\n\n'
        new_content += new_block
    return new_content


def get_optimize_md_with_img(md_path, i):
    content = read_file(md_path)
    new_content = ('template: Martin Template.pptx\n'
                   + 'cardlayout: horizontal\n'
                   + 'baseTextSize: 20\n'
                   + 'CardColour: BACKGROUND 2\n'
                   + 'CardTitlePosition: inside\n'
                   + 'cardshadow: yes\n'
                   + 'cardshape: rounded\n'
                   + 'removeFirstSlide: yes\n'
                   + 'backgroundImage: background.png\n'
                   + 'marginBase: 0.5\n\n')
    if content.startswith(new_content):
        new_content = ''
    new_content += search_picture(content, i)
    format_content = format_url(new_content)
    write_file(md_path, format_content)


if __name__ == '__main__':
    md_path = './optimize/content_5.md'
    get_optimize_md_with_img(md_path, 5)
    print('图片已添加')
