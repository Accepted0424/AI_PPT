import re
from getPicture import call_image_downloader


def get_optimize_md_with_img(md_path):
    # config
    new_content = ('template: Martin Template.pptx\n'
                   + 'cardlayout: horizontal\n'
                   + 'baseTextSize: 20\n'
                   + 'CardColour: BACKGROUND 2\n'
                   + 'CardTitlePosition: inside\n'
                   + 'cardshadow: yes\n'
                   + 'cardshape: rounded\n\n')

    with open(md_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        # 获取图片关键词，删去关键词，增加图片链接
        for line in content.split('\n'):
            if line.startswith('* (') or line.startswith('(') or line.startswith('  * ('):
                pic_query_list = re.findall(r'\((.*?)\)', line)
                pic_query = pic_query_list[0]
                try:
                    pattern = r'.\\optimize\\content_(\d+)\.md'
                    match = re.match(pattern, md_path)
                    i = int(match.group(1))
                    image_path = call_image_downloader(pic_query, f"picture/part_{i}")
                    new_line = f"![{pic_query}](.\\picture\\part_{i}\\{image_path})\n"
                    new_content += new_line
                except:
                    new_content += line
                    new_content += '\n'
            elif line.startswith('---'):
                pass
            else:
                new_content += line
                new_content += '\n'
        f.seek(0)
        f.write(new_content)
        f.truncate()
        print('图片已添加')


if __name__ == '__main__':
    md_path = './optimize/content_4.md'
    get_optimize_md_with_img(md_path)
    print('图片已添加')
