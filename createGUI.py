import tkinter as tk
from tkinter import filedialog


class gui:
    def __init__(self, root):
        self.chapters = None
        self.split_flags = None
        self.book_path = ''
        self.prompt_file_path = ''
        self.output_file_path = ''
        self.pages = ''

        self.root = root
        self.root.title("PPT生成器")
        self.root.geometry("500x400")

        # Setup GUI
        self.setup_ui()

    def setup_ui(self):
        self.book_button = tk.Button(self.root, text="选择书籍文件", command=self.select_book_file)
        self.book_button.pack(pady=10)

        self.book_file_label = tk.Label(self.root, text="支持.epub、.pdf、.txt、.docx格式")
        self.book_file_label.pack(pady=5)

        self.prompt_button = tk.Button(self.root, text="选择Prompt文件", command=self.select_prompt_file)
        self.prompt_button.pack(pady=10)

        self.prompt_file_label = tk.Label(self.root, text="支持.txt格式")
        self.prompt_file_label.pack(pady=5)

        self.label_split = tk.Label(self.root, text="分割标志，用换行符分隔")
        self.label_split.pack(pady=5)

        self.text_split = tk.Text(self.root, height=5, width=50)
        self.text_split.pack(pady=5)

        self.label_chapter = tk.Label(self.root, text="选择章节，用英文逗号分隔")
        self.label_chapter.pack(pady=5)

        self.entry_chapter = tk.Entry(self.root, width=50)
        self.entry_chapter.pack(pady=5)

        self.generate_button = tk.Button(self.root, text="生成大纲", command=self.quit_program)
        self.generate_button.pack(pady=20)

    def select_book_file(self):
        self.book_path = filedialog.askopenfilename(
            title="选择书籍文件",
            filetypes=(("所有文件", "*.*"),)
        )
        if self.book_path:
            self.book_file_label.config(text=f"已选择文件: {self.book_path}")

    def select_prompt_file(self):
        self.prompt_file_path = filedialog.askopenfilename(
            title="选择prompt文件",
            filetypes=(("文本文件", "*.txt"),)
        )
        if self.prompt_file_path:
            self.prompt_file_label.config(text=f"已选择文件: {self.prompt_file_path}")

    def get_label(self):
        try:
            # 验证 chapters 中的元素是否符合要求
            if not all(isinstance(chapter, int) and chapter > 0 for chapter in self.chapters):
                raise ValueError("每个 chapter 必须是正整数")

            if not all(chapter <= len(self.split_flags) + 1 for chapter in self.chapters):
                raise ValueError("章节号超出范围")

            # 如果验证通过，返回结果
            return self.split_flags, self.chapters

        except ValueError as e:
            # 捕获并处理验证过程中发生的错误
            print(f"错误: {e}")
            return None

    def get_book_path(self):
        return self.book_path

    def get_prompt_file_path(self):
        return self.prompt_file_path

    def get_output_file_path(self):
        return self.output_file_path

    def quit_program(self):
        self.split_flags = self.text_split.get("1.0", tk.END).strip().split('\n')
        entry_chapter_number_str = self.entry_chapter.get().split(',')
        entry_chapter_number_list = [int(num) for num in entry_chapter_number_str]
        self.chapters = entry_chapter_number_list
        self.root.quit()  # Closes the Tkinter window
        self.root.destroy()
