# ui/app_ui.py

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit,
    QPushButton, QFileDialog, QComboBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import fitz  # PyMuPDF

from translator.translator import TranslatorService


class PDFTranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PDF Translator')
        self.translator_service = TranslatorService()
        self.doc = None
        self.current_page = 0
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Button layout
        button_layout = QHBoxLayout()
        self.open_button = QPushButton('Open PDF')
        self.open_button.clicked.connect(self.open_pdf)
        self.prev_button = QPushButton('Previous Page')
        self.next_button = QPushButton('Next Page')
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        self.lang_combo = QComboBox()
        self.lang_combo.addItem('English', 'en')
        self.lang_combo.addItem('Spanish', 'es')
        self.lang_combo.addItem('French', 'fr')
        self.lang_combo.addItem('German', 'de')
        self.lang_combo.addItem('Chinese (Simplified)', 'zh-cn')
        # Add more languages as needed

        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.lang_combo)

        # Content layout
        content_layout = QHBoxLayout()

        # Left pane: PDF display
        self.pdf_label = QLabel('PDF will be displayed here')
        self.pdf_label.setAlignment(Qt.AlignCenter)
        self.pdf_label.setSizePolicy(
            self.pdf_label.sizePolicy().horizontalPolicy(),
            self.pdf_label.sizePolicy().verticalPolicy()
        )
        content_layout.addWidget(self.pdf_label, stretch=1)

        # Right pane: Translated text
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        content_layout.addWidget(self.text_edit, stretch=1)

        # Add layouts to main layout
        main_layout.addLayout(button_layout)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

        # Set focus to the main window to receive key events
        self.setFocusPolicy(Qt.StrongFocus)

    def open_pdf(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open PDF File', '', 'PDF Files (*.pdf)', options=options
        )
        if file_path:
            self.doc = fitz.open(file_path)
            self.current_page = 0
            self.display_page(self.current_page)
            # Set focus to capture key events after opening a PDF
            self.setFocus()

    def display_page(self, page_number):
        if self.doc is not None:
            page = self.doc.load_page(page_number)
            pix = page.get_pixmap(dpi=150)  # Increase DPI for better quality
            image_bytes = pix.tobytes("png")
            pixmap = QPixmap()
            pixmap.loadFromData(image_bytes)

            # Get the size of the pdf_label
            label_width = self.pdf_label.width()
            label_height = self.pdf_label.height()

            # Scale pixmap to fit the label
            pixmap = pixmap.scaled(
                label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

            self.pdf_label.setPixmap(pixmap)
            self.extract_and_translate(page)
        else:
            self.pdf_label.setText('No PDF loaded.')

    def extract_and_translate(self, page):
        text = page.get_text()
        target_lang = self.lang_combo.currentData()
        translation = self.translator_service.translate_text(text, target_lang)
        self.text_edit.setText(translation)
        # Set focus back to the main window after updating text
        self.setFocus()

    def prev_page(self):
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            self.display_page(self.current_page)

    def next_page(self):
        if self.doc and self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.display_page(self.current_page)

    def resizeEvent(self, event):
        if self.doc is not None:
            self.display_page(self.current_page)
        super(PDFTranslatorApp, self).resizeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.prev_page()
        elif event.key() == Qt.Key_Down:
            self.next_page()
        else:
            super(PDFTranslatorApp, self).keyPressEvent(event)
