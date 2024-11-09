from openai import OpenAI
import json
from readBook import *
import os


# 调用API生成目标文字
def call_openai(theme, pages, book_path, prompt_file_path, output_file_path):
    # 创建 OpenAI 客户端
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    output_format = json.dumps({
        "title": "example title",
        "pages": [
            {
                "title": "title for page 1",
                "content": [
                    {
                        "title": "title for paragraph 1",
                        "description": "detail for paragraph 1",
                    },
                    {
                        "title": "title for paragraph 2",
                        "description": "detail for paragraph 2",
                    },
                ],
                "picture": "summarize the content of this page in a few words",
            },
            {
                "title": "title for page 2",
                "content": [
                    {
                        "title": "title for paragraph 1",
                        "description": "detail for paragraph 1",
                    },
                    {
                        "title": "title for paragraph 2",
                        "description": "detail for paragraph 2",
                    },
                    {
                        "title": "title for paragraph 3",
                        "description": "detail for paragraph 3",
                    },
                ],
                "picture": "summarize the content of this page in a few words",
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
    ppt_content = json.loads(str_content)
    return ppt_content
