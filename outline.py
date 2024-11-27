import tkinter as tk
from tkinter import messagebox


# 创建Tkinter窗口
def polish(file_path):
    # 创建主窗口
    root = tk.Tk()
    root.title("大纲")

    # 创建文本框来显示和编辑文件内容
    text_area = tk.Text(root, wrap=tk.WORD, width=80, height=20)
    text_area.pack(padx=10, pady=10)

    # 读取文件内容并显示
    with open(file_path[0], 'r', encoding='utf-8') as file:
        content = file.read()
    text_area.insert(tk.END, content)

    # 按钮点击事件：保存文件并生成PPT
    def click():
        modified_content = text_area.get("1.0", tk.END).strip()
        if modified_content == "":
            messagebox.showwarning("警告", "内容不能为空！")
            return

        # 保存修改后的内容到文件
        with open(file_path[0], 'w', encoding='utf-8') as file:
            file.write(content)
        with open(file_path[1], 'w', encoding='utf-8') as file:
            file.write(content)
        root.destroy()
        return modified_content

    # 创建生成PPT按钮
    generate_button = tk.Button(root, text="生成PPT", command=click)
    generate_button.pack(pady=10)

    # 启动主循环
    root.mainloop()
