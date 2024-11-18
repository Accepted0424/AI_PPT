from generatePPT import *
from callAPI import *

book_path = ''
prompt_file_path = ''
output_file_path = ''
theme = ''
pages = ''


def select_book_file():
    global book_path
    book_path = filedialog.askopenfilename(
        title="选择书籍文件",
        filetypes=(("所有文件", "*.*"),)  # 可以根据需要设置文件类型过滤
    )
    if book_path:
        book_file_label.config(text=f"已选择文件: {book_path}")


# 用于选择prompt文件的函数
def select_prompt_file():
    global prompt_file_path
    prompt_file_path = filedialog.askopenfilename(
        title="选择prompt文件",
        filetypes=(("文本文件", "*.txt"),)  # 可以根据需要设置文件类型过滤
    )
    if prompt_file_path:
        prompt_file_label.config(text=f"已选择文件: {prompt_file_path}")


def select_output_file():
    global output_file_path
    output_file_path = filedialog.askdirectory(
        title="选择导出位置",
    )
    if output_file_path:
        output_file_label.config(text=f"已选择导出位置: {output_file_path}")


def save_ppt():
    get_theme_and_pages()
    split_flags, chapters = get_label()
    if prompt_file_path and book_path and output_file_path and theme and pages:
        md_content = call_openai(theme, pages, book_path, prompt_file_path, output_file_path)
        with open('md2pptx/input.md', 'w', encoding='utf-8') as file:
            file.write(md_content)
        # 构建命令
        input_path = os.path.abspath('md2pptx\\input.md')
        command = ['python', './md2pptx/md2pptx', input_path, output_file_path, theme]
        # 使用 subprocess.run 执行命令
        subprocess.run(command)
        # 关闭GUI窗口
        root.quit()
    else:
        messagebox.showerror("信息缺失", "请确保已选择所有必要的文件和输入了主题与页数。")


def get_theme_and_pages():
    global theme, pages
    theme = theme_entry.get()
    pages = page_count_entry.get()
    try:
        pages = int(pages)
        if pages <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("输入错误", "页数必须是正整数！")


def get_label():
    # 获取“分割标志”的内容，每一行作为一个元素
    split_flags = text_split.get("1.0", tk.END).strip().split('\n')
    # 获取“选择章节”的内容并转换为数字列表
    chapter_str = entry_chapter.get().strip()
    try:
        # 将逗号分隔的字符串转化为整数列表，并进行去重和排序
        chapters = [int(num) for num in chapter_str.split(',')]
        chapters = sorted(set(chapters))  # 去重并排序
    except ValueError:
        messagebox.showwarning("输入错误", "章节输入必须是由数字组成的字符串，且用逗号分隔！")
        return
    return split_flags, chapters


if __name__ == "__main__":
    # 创建GUI窗口
    root = tk.Tk()
    root.title("PPT生成器")

    # 设置窗口大小
    root.geometry("500x700")

    # 创建输入框和标签
    theme_label = tk.Label(root, text="请输入PPT主题:")
    theme_label.pack(pady=10)
    theme_entry = tk.Entry(root, width=40)
    theme_entry.pack(pady=5)

    page_count_label = tk.Label(root, text="请输入页数:")
    page_count_label.pack(pady=10)
    page_count_entry = tk.Entry(root, width=40)
    page_count_entry.pack(pady=5)

    # 创建“选择书籍文件”按钮
    book_button = tk.Button(root, text="选择书籍文件", command=select_book_file)
    book_button.pack(pady=10)

    # 显示书籍文件路径的标签
    book_file_label = tk.Label(root, text="未选择书籍文件")
    book_file_label.pack(pady=5)

    # 创建“选择Prompt文件”按钮
    prompt_button = tk.Button(root, text="选择Prompt文件", command=select_prompt_file)
    prompt_button.pack(pady=10)

    # 显示Prompt文件路径的标签
    prompt_file_label = tk.Label(root, text="未选择Prompt文件")
    prompt_file_label.pack(pady=5)

    # 创建“选择Prompt文件”按钮
    output_button = tk.Button(root, text="导出位置", command=select_output_file)
    output_button.pack(pady=10)

    # 显示Prompt文件路径的标签
    output_file_label = tk.Label(root, text="未选择导出位置")
    output_file_label.pack(pady=5)

    # 设置标签
    label_split = tk.Label(root, text="分割标志")
    label_split.pack(pady=5)

    # 多行文本框 - 分割标志
    text_split = tk.Text(root, height=5, width=50)
    text_split.pack(pady=5)

    # 设置标签
    label_chapter = tk.Label(root, text="选择章节")
    label_chapter.pack(pady=5)

    # 输入框 - 选择章节
    entry_chapter = tk.Entry(root, width=50)
    entry_chapter.pack(pady=5)

    # 创建生成PPT的按钮
    generate_button = tk.Button(root, text="生成PPT", command=save_ppt)
    generate_button.pack(pady=20)

    # 运行主循环
    root.mainloop()
