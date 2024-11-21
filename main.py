import os
import tkinter as tk
import callAPI
import createGUI
import subprocess
from md_optimize import get_optimize_md
from splitPDF import split_pdf

if __name__ == "__main__":
    # 图形界面
    root = tk.Tk()
    gui = createGUI.gui(root)
    root.mainloop()

    #获取用户输入
    book_path = gui.get_book_path()
    prompt_file_path = gui.get_prompt_file_path()
    split_flag, chapters = gui.get_label()

    #根据用户需求分割文件
    #幂律，复杂网络背后的规律
    #富者愈富——复杂网络的先发优势
    #爱因斯坦的馈赠——复杂网络的新星效应
    split_chapters_path = os.path.join("split_chapters")
    split_pdf(book_path, split_flag, chapters, split_chapters_path)

    # 遍历分割章节生成ppt
    for i in range(0,len(chapters)):
        # 获取大模型返回内容
        chapter_path = f'split_chapters/part_{i}.txt'
        api_return_content = callAPI.call_api(chapter_path, prompt_file_path)
        # 调整md，嵌入图片
        get_optimize_md()
        command = ['python', './md2pptx/md2pptx', './api_return_src/content_format.md', f'output_{i}.pptx']
        # 使用 subprocess.run 执行命令
        subprocess.run(command)
