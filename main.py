import sys
from PyQt5.QtWidgets import QApplication
import createGUI


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = createGUI.MainWindow()
    gui.show()
    sys.exit(app.exec_())
