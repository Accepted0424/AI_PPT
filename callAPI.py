import json
import re
import md_optimize
import os
from openai import OpenAI
from readBook import read_file


# 调用API生成目标文字
def call_api(book_path, prompt_file_path, temp=0.4, top=0.5):
    # 从环境变量中读取 API 密钥
    key = os.getenv("API_KEY")
    if not key:
        raise ValueError("找不到环境变量API_KEY")

    # 创建 OpenAI 客户端
    client = OpenAI(
        api_key=key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # 读取 prompt.txt 文件内容
    with open(prompt_file_path, 'r', encoding='utf-8') as prompt_file:
        prompt_content = prompt_file.read()

    # 输入 prompt 内容
    '''
    prompt = f"""使用markdown的格式，并且请严格遵循以下要求:
            1.最少要有四级标题。
            2.第一级(#)表示ppt的标题,第二级(##)表示章节的标题,第三级(###)表示章节的重点,第四级(*)表示重点内容下的知识点,第四级下有对知识点的详细介绍，介绍时用(  *)表示分点.
            2.第一级(#)内容固定为“本章内容”。第二级(##)表示。第三级(###)表示。第四级用(*)表示具体的知识点。
            3.每一章重点(###)知识点列举完之后用英语单词或短语概括该重点,用作关键词搜索图片,关键词应该与ppt的主题相符,用括号括起来,单独占一行,例如"(network)"
            4.生成的markdown文档不要用```包裹。
        """
    '''

    # 读取 book.file 文件内容
    file_content = read_file(book_path)
    # 创建聊天完成请求
    completion = client.chat.completions.create(
        model="qwen-plus",
        temperature=temp,
        top_p=top,
        messages=[
            {'role': 'system',
             'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': f"文章内容：{file_content}"},
            {'role': 'user', 'content': f"思考方式：{prompt_content}"},
        ]

    )

    # 将结果转换为 JSON 字符串
    response = completion.model_dump_json()
    content = json.loads(response)
    md_content = content['choices'][0]['message']['content']

    # 将返回内容保存到文件夹“apiReturn”，用于缓存和测试
    folder_path = "apiReturn"
    md_path = "optimize"
    os.makedirs(folder_path, exist_ok=True)
    os.makedirs(md_path, exist_ok=True)
    # 正则表达式获取文件路径中的序号，避免并行运行时序号错误
    pattern = r'chapters/part_(\d+)\.txt'
    match = re.match(pattern, book_path)
    i = int(match.group(1))
    md_file_path = os.path.join(md_path, f"content_{i}.md")
    content_file_path = os.path.join(folder_path, f"content_{i}.md")
    with open(content_file_path, 'w', encoding='utf-8') as content_file:
        content_file.write(md_content)
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)
        print("返回文件中的content部分已保存")
    optimize_path = f'.\\{md_file_path}'
    md_optimize.get_optimize_md_with_img(optimize_path)


# 直接运行该文件进行测试
if __name__ == '__main__':
    book_path_test = "chapters/part_1.txt"
    prompt_file_path_test = "prompt.txt"
    call_api(book_path_test, prompt_file_path_test)
