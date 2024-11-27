import subprocess
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QLineEdit, QVBoxLayout, QWidget, QFileDialog,
    QMessageBox, QHBoxLayout, QSplitter, QDialog, QFileSystemModel, QTreeView
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QModelIndex
import markdown
from callAPI import call_api
from md_optimize import get_optimize_md


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.chapters = None
        self.split_flags = None
        self.book_path = ''
        self.prompt_file_path = ''
        self.output_file_path = ''
        self.pages = ''
        self.api_request = None

        # 窗口设置
        self.setWindowTitle("PPT生成器")
        self.setGeometry(100, 100, 600, 600)
        self.setWindowIcon(QIcon("buaa_cs_logo.png"))

        # 设置 UI
        self.setup_ui()

    def open_markdown_editor(self):
        # 创建并显示 Markdown 编辑窗口
        self.editor_window = MdEditorWindow()
        self.editor_window.show()
        self.close()  # 可选：关闭主窗口

    def setup_ui(self):
        # 中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # 添加样式
        self.setStyleSheet("""
            QLabel {
                font-family: "Microsoft YaHei";
                font-size: 16px;
                color: #333333;
            }
            QPushButton {
                font-family: "Microsoft YaHei";
                font-size: 16px;
                background-color: #d3d3d3;
                color: black;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #c0c0c0;
            }
            QTextEdit, QLineEdit {
                font-family: "Microsoft YaHei";
                font-size: 16px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 4px;
            }
            QMainWindow {
                font-family: "Microsoft YaHei";
                font-size: 16px;
                background-color: #f9f9f9;
            }
        """)

        # 选择书籍文件
        self.book_button = QPushButton("选择书籍文件")
        self.book_button.clicked.connect(self.select_book_file)
        layout.addWidget(self.book_button, alignment=Qt.AlignCenter)

        self.book_file_label = QLabel("支持.epub、.pdf、.txt、.docx格式")
        self.book_file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.book_file_label)

        # 选择 Prompt 文件
        self.prompt_button = QPushButton("选择 Prompt 文件")
        self.prompt_button.clicked.connect(self.select_prompt_file)
        layout.addWidget(self.prompt_button, alignment=Qt.AlignCenter)

        self.prompt_file_label = QLabel("支持 .txt 格式")
        self.prompt_file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.prompt_file_label)

        # 选择导出位置
        self.output_button = QPushButton("导出位置")
        self.output_button.clicked.connect(self.select_output_file)
        layout.addWidget(self.output_button, alignment=Qt.AlignCenter)

        self.output_file_label = QLabel("请选择有效位置")
        self.output_file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.output_file_label)

        # 分割标志
        self.label_split = QLabel("分割标志，用换行符分隔")
        self.label_split.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_split)

        self.text_split = QTextEdit()
        self.text_split.setFixedHeight(80)
        layout.addWidget(self.text_split)

        # 选择章节
        self.label_chapter = QLabel("选择章节，用逗号分隔")
        self.label_chapter.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_chapter)

        self.entry_chapter = QLineEdit()
        layout.addWidget(self.entry_chapter)

        # 生成按钮
        self.generate_button = QPushButton("下一步")
        self.generate_button.clicked.connect(self.show_loading_and_request)
        layout.addWidget(self.generate_button, alignment=Qt.AlignCenter)

        # 设置布局
        central_widget.setLayout(layout)

    def get_flag_and_chapters(self):
        try:
            # 验证 chapters 中的元素是否符合要求
            if not all(isinstance(chapter, int) and chapter > 0 for chapter in self.chapters):
                raise ValueError("每个 chapter 必须是正整数")

            if not all(chapter <= len(self.split_flags) + 1 for chapter in self.chapters):
                raise ValueError("章节号超出范围")

            # 如果验证通过，返回结果
            self.split_flags = self.text_split.toPlainText().split('\n')
            chapters_str = self.entry_chapter.text().split(',，')
            chapters_list = [int(num) for num in chapters_str]
            self.chapters = chapters_list
            return self.split_flags, self.chapters

        except ValueError as e:
            # 捕获并处理验证过程中发生的错误
            print(f"错误: {e}")
            return None

    def show_loading_and_request(self):
        """显示加载界面并请求api"""
        # 创建加载窗口
        split_flags, chapters = self.get_flag_and_chapters()
        self.loading_dialog = LoadingDialog(self)
        self.loading_dialog.show()
        self.hide()
        # 启动后台任务
        self.worker = ApiWorker(self.book_path, self.prompt_file_path, self.output_file_path, split_flags, chapters)
        self.worker.result_ready.connect(self.show_md_editor)
        self.worker.start()

    def show_md_editor(self):
        self.loading_dialog.hide()
        self.mdEditor = MdEditorWindow()
        self.mdEditor.show()

    def select_book_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择书籍文件", "", "所有文件 (*.*)"
        )
        if file_path:
            self.book_path = file_path
            self.book_file_label.setText(f"已选择文件: {self.book_path}")

    def select_prompt_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Prompt文件", "", "文本文件 (*.txt)"
        )
        if file_path:
            self.prompt_file_path = file_path
            self.prompt_file_label.setText(f"已选择文件: {self.prompt_file_path}")

    def select_output_file(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择导出位置")
        if dir_path:
            self.output_file_path = dir_path
            self.output_file_label.setText(f"已选择导出位置: {self.output_file_path}")

class ApiWorker(QThread):
    result_ready = pyqtSignal(object)  # 信号：API 请求完成后返回结果

    def __init__(self, book_path, prompt_file_path, split_flags, chapters, parent=None):
        super().__init__(parent)
        self.book_path = book_path
        self.prompt_file_path = prompt_file_path
        self.split_flags = split_flags
        self.chapters = chapters

    def run(self):
        """在后台线程中调用 API"""
        response = call_api(self.book_path, self.prompt_file_path)
        self.result_ready.emit(response)

        for i in range(0, len(self.chapters)):
            # 获取大模型返回内容
            chapter_path = f'split_chapters/part_{i}.txt'
            call_api(chapter_path, self.prompt_file_path, )
            # 调整md，嵌入图片
            get_optimize_md()
            command = ['python', './md2pptx/md2pptx', './api_return_src/content_format.md', f'output_{i}.pptx']
            # 使用 subprocess.run 执行命令
            subprocess.run(command)

class LoadingDialog(QDialog):
    """加载界面"""

    WINDOW_TITLE = "Loading"
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 500

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """设置 UI 界面"""
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowIcon(QIcon("buaa_cs_logo.png"))
        self.setModal(True)
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        layout = QVBoxLayout(self)

        loading_label = QLabel("Loading, please wait...", self)
        loading_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(loading_label)

class MdEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('修改大纲')
        self.setGeometry(100, 100, 1500, 1000)
        self.setWindowIcon(QIcon("buaa_cs_logo.png"))
        self.setStyleSheet("""
                   QLabel {
                       font-family: "Microsoft YaHei";
                       font-size: 16px;
                       color: #333333;
                   }
                   QPushButton {
                       font-family: "Microsoft YaHei";
                       font-size: 16px;
                       background-color: #d3d3d3;
                       color: black;
                       padding: 8px 16px;
                       border-radius: 8px;
                   }
                   QPushButton:hover {
                       background-color: #c0c0c0;
                   }
                   QTextEdit, QLineEdit{
                       font-family: "Microsoft YaHei";
                       font-size: 16px;
                       border: 1px solid #cccccc;
                       border-radius: 4px;
                       padding: 4px;
                   }
                   QMainWindow {
                       font-family: "Microsoft YaHei";
                       font-size: 16px;
                       background-color: #f9f9f9;
                   }
               """)

        # 设置布局
        layout = QVBoxLayout()

        # 创建一个 QSplitter，用于左右分隔两个控件
        splitter = QSplitter(Qt.Horizontal, self)
        sub_splitter = QSplitter(Qt.Horizontal, self)

        # 创建文件系统模型和视图
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath('api_return_src')  # 根目录
        self.file_model.setNameFilters(['*.md'])  # 只显示Markdown文件
        self.file_model.setNameFilterDisables(False)

        self.file_view = QTreeView()
        self.file_view.setModel(self.file_model)
        self.file_view.setRootIndex(self.file_model.index('api_return_src'))  # 设置初始路径
        self.file_view.setColumnHidden(1,True)
        self.file_view.setColumnHidden(2,True)
        self.file_view.setColumnWidth(0, 200)  # 设置文件名列宽度
        self.file_view.setColumnWidth(3, 100)  # 设置修改日期列宽度
        self.file_view.clicked.connect(self.open_file)

        # 创建左侧的文件栏 QTreeView
        splitter.addWidget(self.file_view)

        # 创建左侧的 QTextEdit，用于编辑 Markdown 原码
        self.markdown_editor = QTextEdit(self)
        self.md_path = 'api_return_src/content_format.md'
        self.content = ''
        with open(self.md_path, 'r+', encoding='utf-8') as f:
            self.content = f.read()
        self.markdown_editor.setPlainText(self.content)
        self.markdown_editor.textChanged.connect(self.update_rendered_view)  # 监听内容变化

        # 创建右侧的 QWebEngineView，用于显示渲染后的 HTML
        self.rendered_view = QWebEngineView(self)

        # 如果markdown editor的scroll bar变化调用函数调整渲染界面
        self.md_vsb = self.markdown_editor.verticalScrollBar()
        self.md_vsb.valueChanged.connect(self.moveWebScrollBar)

        # 添加控件到分隔器
        sub_splitter.addWidget(self.markdown_editor)
        sub_splitter.addWidget(self.rendered_view)
        splitter.addWidget(sub_splitter)

        # 设置分隔器比例
        splitter.setSizes([300, 1000])
        sub_splitter.setSizes([500,500])

        # 将分隔器添加到布局
        layout.addWidget(splitter)

        self.save_button = QPushButton('保存当前md文件')
        self.save_button.setFixedSize(200, 50)
        self.save_button.clicked.connect(self.save_file)

        self.submit_button = QPushButton('生成ppt')
        self.submit_button.setFixedSize(100, 50)
        # 创建水平布局来包含按钮，以便居中对齐
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()

        # 将按钮的水平布局添加到主布局
        layout.addLayout(button_layout)

        # 设置中央部件
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.update_rendered_view()  # 初始化渲染

    def open_file(self, index: QModelIndex):
        file_path = self.file_model.filePath(index)
        with open(file_path, 'r', encoding='utf-8') as file:
            self.content = file.read()
        self.markdown_editor.setPlainText(self.content)
        self.md_path = file_path

    def update_rendered_view(self):
        # 获取 Markdown 原码并转换为 HTML
        self.content = self.markdown_editor.toPlainText()
        html_content = markdown.markdown(self.content)
        self.rendered_view.setHtml(html_content)  # 更新右侧渲染内容

    def moveWebScrollBar(self):
        """同步 Markdown 编辑器滚动条与渲染视图的滚动位置"""
        # 获取 Markdown 编辑器的滚动条位置
        md_vsb_value = self.md_vsb.value()
        self.rendered_view.page().runJavaScript(f"window.scrollTo(0, {md_vsb_value});")

    def save_file(self):
        with open(self.md_path, 'w', encoding='utf-8') as file:
            file.write(self.content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MdEditorWindow()
    gui.show()
    sys.exit(app.exec_())
