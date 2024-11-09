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
    if prompt_file_path and book_path and output_file_path and theme and pages:
        ppt_content = call_openai(theme, pages, book_path, prompt_file_path, output_file_path)
        ppt = generate(ppt_content)
        ppt.save(output_file_path + '/' + theme + ".pptx")
        output_file_label.config(text=f"PPT导出到: {output_file_path}")
        messagebox.showinfo("导出成功", f"PPT已保存到: {output_file_path}")
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


if __name__ == "__main__":
    # 创建GUI窗口
    root = tk.Tk()
    root.title("PPT生成器")

    # 设置窗口大小
    root.geometry("500x500")

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

    # 创建生成PPT的按钮
    generate_button = tk.Button(root, text="生成PPT", command=save_ppt)
    generate_button.pack(pady=20)

    # 运行主循环
    root.mainloop()
