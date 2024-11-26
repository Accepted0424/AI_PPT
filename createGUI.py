import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QLineEdit, QVBoxLayout, QWidget, QFileDialog,
    QMessageBox, QHBoxLayout, QSplitter, QDialog
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import markdown
from anyio._backends._asyncio import WorkerThread
import callAPI
from callAPI import call_api


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
        self.setWindowIcon(QIcon("icon.png"))  # 使用自己的图标文件路径

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

        self.book_file_label = QLabel("支持 .epub、.pdf 格式")
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

    def show_loading_and_request(self):
        """显示加载界面并请求api"""
        self.close()
        # 创建加载窗口
        self.loading_dialog = LoadingDialog(self)
        self.loading_dialog.show()

        # 启动后台任务
        self.worker = ApiWorker(self.book_path,self.prompt_file_path)
        self.worker.result_ready.connect(self.show_md_editor)
        self.worker.start()

    def show_md_editor(self):
        self.loading_dialog.close()
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

    def __init__(self, book_path, prompt_file_path, parent=None):
        super().__init__(parent)
        self.book_path = book_path
        self.prompt_file_path = prompt_file_path

    def run(self):
        """在后台线程中调用 API"""
        response = call_api(self.book_path, self.prompt_file_path)
        self.result_ready.emit(response)

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

        # 读取 Markdown 文件内容
        content = ''
        with open('api_return_src/content_format.md', 'r+', encoding='utf-8') as f:
            content = f.read()

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

        # 创建左侧的 QTextEdit，用于编辑 Markdown 原码
        self.markdown_editor = QTextEdit(self)
        self.markdown_editor.setPlainText(content)
        self.markdown_editor.textChanged.connect(self.update_rendered_view)  # 监听内容变化

        # 创建右侧的 QWebEngineView，用于显示渲染后的 HTML
        self.rendered_view = QWebEngineView(self)

        # 如果markdown editor的scroll bar变化调用函数调整渲染界面
        self.md_vsb = self.markdown_editor.verticalScrollBar()
        self.md_vsb.valueChanged.connect(self.moveWebScrollBar)

        # 添加控件到分隔器
        splitter.addWidget(self.markdown_editor)
        splitter.addWidget(self.rendered_view)

        # 设置分隔器比例
        splitter.setSizes([500, 500])

        # 将分隔器添加到布局
        layout.addWidget(splitter)

        self.submit_button = QPushButton('生成ppt')
        self.submit_button.setFixedSize(100, 50)
        # 创建水平布局来包含按钮，以便居中对齐
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()

        # 将按钮的水平布局添加到主布局
        layout.addLayout(button_layout)

        # 设置中央部件
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.update_rendered_view()  # 初始化渲染

    def update_rendered_view(self):
        # 获取 Markdown 原码并转换为 HTML
        markdown_content = self.markdown_editor.toPlainText()
        html_content = markdown.markdown(markdown_content)
        self.rendered_view.setHtml(html_content)  # 更新右侧渲染内容

    def moveWebScrollBar(self):
        """同步 Markdown 编辑器滚动条与渲染视图的滚动位置"""
        # 获取 Markdown 编辑器的滚动条位置
        md_vsb_value = self.md_vsb.value()
        self.rendered_view.page().runJavaScript(f"window.scrollTo(0, {md_vsb_value});")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
