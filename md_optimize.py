import re

from getPicture import getPic


def get_optimize_md(api_path):
    # config
    new_content = ('template: Martin Template.pptx\n'
                   + 'cardlayout: horizontal\n'
                   + 'baseTextSize: 20\n'
                   + 'CardColour: BACKGROUND 2\n'
                   + 'CardTitlePosition: inside\n'
                   + 'cardshadow: yes\n'
                   + 'cardshape: rounded\n\n')

    with open(api_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        new_content += content
        f.seek(0)
        f.write(new_content)
        f.truncate()
    #    # 获取图片关键词，删去关键词，增加图片链接
    #    for line in content.split('\n'):
    #        if line.startswith('* (') or line.startswith('(') or line.startswith('  * ('):
    #            pic_query_list = re.findall(r'\((.*?)\)', line)
    #            pic_query = pic_query_list[0]
    #            try:
    #                image_path = getPic(pic_query, 'default')
    #            except:
    #                pass
    #            new_line = f"![{pic_query}](.\\{image_path})\n"
    #            new_content += new_line
    #        elif line.startswith('---'):
    #            break
    #        else:
    #            new_content += line
    #            new_content += '\n'
    #    f.seek(0)
    #    f.write(new_content)
    #    f.truncate()
