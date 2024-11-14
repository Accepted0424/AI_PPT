from openai import OpenAI
from json2md import *
from readBook import read_file
import os


# 调用API生成目标文字
def call_openai(theme, pages, book_path, prompt_file_path, output_file_path):
    # 创建 OpenAI 客户端
    client = OpenAI(
        api_key="YOUR_TONGYI_API_KEY",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    output_format = json.dumps({
        "title": "PPT的主题",
        "pages": [
            {
                "title": "第一页的主题",
                "content": [
                    {
                        "title": "第一段的主题",
                        "description": "第一段的细节内容，120-170字",
                    },
                    {
                        "title": "第二段的主题",
                        "description": "第二段的细节内容，120-170字",
                    },
                ],
                "picture": "用一个词语总结本页的内容",
            },
            {
                "title": "第二页的主题",
                "content": [
                    {
                        "title": "第一段的主题",
                        "description": "第一段的细节内容，120-170字",
                    },
                    {
                        "title": "第二段的主题",
                        "description": "第二段的细节内容，120-170字",
                    },
                    {
                        "title": "第三段的主题",
                        "description": "第三段的细节内容，120-170字",
                    },
                ],
                "picture": "用一个词语总结本页的内容",
            },
        ],
    }, ensure_ascii=True)
    # 输入 prompt 内容
    prompt = f'''我要准备1个关于{theme}的PPT，要求一共写{pages}页，请你根据主题生成详细文本内容，不要省略。
       按这个JSON格式输出{output_format}，只能返回JSON，且JSON不要用```包裹，内容要用中文。'''

    # 读取 prompt.txt 文件内容
    with open(prompt_file_path, 'r', encoding='utf-8') as prompt_file:
        prompt_content = prompt_file.read()

    # 读取 book.file 文件内容
    file_content = read_file(book_path)

    # 创建聊天完成请求
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': f"文件内容：{file_content}"},
            {'role': 'user', 'content': f"内容要求：{prompt_content}"},
            {'role': 'user', 'content': f"格式要求：{prompt}"},
        ]
    )

    # 将结果转换为 JSON 字符串
    completion_json = completion.model_dump_json()
    content = json.loads(completion_json)
    str_content = content['choices'][0]['message']['content']
    str_content = str_content.replace("\\", "\\\\")
    dic_content = json.loads(str_content)
    md_content = json_to_markdown(dic_content)

    return md_content


'''
    # 将返回内容保存到文件夹“api_return_src”，用于缓存和测试
    folder_path = "api_return_src"
    completion_file_path = os.path.join(folder_path, "completion.json")
    os.makedirs(folder_path, exist_ok=True)
    with open(completion_file_path, 'w', encoding='utf-8') as completion_file:
        completion_file.write(completion_json)
        print("api返回文件(格式化)已保存")
    content_file_path = os.path.join(folder_path, "content_format.json")
    with open(content_file_path, 'w', encoding='utf-8') as content_file:
        content_file.write(str_content)
        print("返回文件中的content部分已保存")
'''

# 直接运行该文件进行测试
if __name__ == '__main__':
    theme_test = input("请输入ppt的主题：")
    page_test = input("请输入ppt的页数：")
    book_path_test = "book.pdf"
    prompt_file_path_test = "prompt.txt"
    call_openai(theme_test, page_test, book_path_test, prompt_file_path_test)
