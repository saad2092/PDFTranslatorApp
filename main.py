# main.py

import sys
from PyQt5.QtWidgets import QApplication
from ui.app_ui import PDFTranslatorApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator_app = PDFTranslatorApp()
    translator_app.show()
    sys.exit(app.exec_())
