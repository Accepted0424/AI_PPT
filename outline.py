import tkinter as tk
from tkinter import messagebox


# 假设这是生成PPT的方法


# 读取文件内容
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        messagebox.showerror("错误", f"无法读取文件: {e}")
        return ""


# 将修改后的内容写回文件
def save_to_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        messagebox.showinfo("成功", "内容已保存！")
    except Exception as e:
        messagebox.showerror("错误", f"无法保存文件: {e}")


# 创建Tkinter窗口
def polish(file_path):
    # 创建主窗口
    root = tk.Tk()
    root.title("大纲")

    # 创建文本框来显示和编辑文件内容
    text_area = tk.Text(root, wrap=tk.WORD, width=80, height=20)
    text_area.pack(padx=10, pady=10)

    # 读取文件内容并显示
    content = read_file(file_path)
    text_area.insert(tk.END, content)

    # 按钮点击事件：保存文件并生成PPT
    def click():
        modified_content = text_area.get("1.0", tk.END).strip()
        if modified_content == "":
            messagebox.showwarning("警告", "内容不能为空！")
            return

        # 保存修改后的内容到文件
        save_to_file(file_path, modified_content)
        return modified_content

    # 创建生成PPT按钮
    generate_button = tk.Button(root, text="生成PPT", command=click)
    generate_button.pack(pady=10)

    # 启动主循环
    root.mainloop()


if __name__ == "__main__":
    # 设置文件路径
    file_path = "README.md"
    # 创建GUI
    polish(file_path)
