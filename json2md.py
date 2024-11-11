import json
import os


def json_to_markdown(json_data):
    # config information
    md_output = 'template: Martin Template.pptx\ncardlayout: horizontal\nbaseTextSize: 20\nCardColour: BACKGROUND 2\nCardTitlePosition: inside\ncardshadow: yes\ncardshape: rounded'

    # cover
    md_output += '\n\n# ' + json_data['title']  # Markdown的标题
    md_output += '\nPowered by Tongyi.ali'

    # 遍历每一页
    for i, page in enumerate(json_data['pages']):
        md_output += '\n\n### ' + page['title']
        # 遍历每一页中的栏
        for j,column in enumerate(page['content']):
            md_output += '\n\n#### ' + column['title']
            md_output += '\n* ' + column['description']
    return md_output

if __name__ == '__main__':
    # 读取JSON文件
    with open("api_return_src/content_format.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)

    # 转换并保存为Markdown格式
    markdown_content = json_to_markdown(json_data)

    # 定义目标文件夹和文件名
    output_folder = "api_return_src"
    output_file = "content.md"
    output_path = os.path.join(output_folder, output_file)

    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)

    print("JSON转换为Markdown完成！")

