from cv2 import cv2
import pytesseract
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QComboBox
from PyQt5.QtGui import QPixmap
from googletrans import Translator
# btl
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Ứng dụng đọc văn bản"
        self.left = 100
        self.top = 100
        self.width = 500
        self.height = 400

        self.InitWindow()

        self.translator = Translator()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label = QLabel(self)
        self.label.setText("Chọn tệp hình ảnh:")
        self.label.move(30, 50)

        self.button = QPushButton("Chọn", self)
        self.button.move(150, 150)
        self.button.clicked.connect(self.on_click)

        self.save_button = QPushButton("Lưu", self)
        self.save_button.move(250, 150)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_text)

        self.language_label = QLabel(self)
        self.language_label.setText("Chọn ngôn ngữ:")
        self.language_label.move(30, 100)

        self.language_combo = QComboBox(self)
        self.language_combo.addItem("Tiếng Anh", "eng")
        self.language_combo.addItem("Tiếng Việt", "vie")
        self.language_combo.addItem("Tiếng Trung", "chi_sim")
        self.language_combo.move(150, 100)

        self.image_label = QLabel(self)
        self.image_label.move(50, 200)
        self.image_label.setFixedWidth(400)
        self.image_label.setFixedHeight(150)

        self.textbox = QLabel(self)
        # self.textbox.setText("Ket qua demo:")
        self.textbox.move(50, 200)
        self.textbox.setFixedWidth(400)
        self.textbox.setFixedHeight(400)

        self.demo_button = QPushButton("Mẫu hình ảnh", self)
        self.demo_button.move(350, 50)
        self.demo_button.clicked.connect(self.load_demo_image)
        # self.demo_button.setEnabled(False)

    def on_click(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn tệp hình ảnh", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.image = cv2.imread(file_path)
            self.imgWhite=cv2.imread('imageWhite.png')
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            # self.image_label.setPixmap(QPixmap.fromImage(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)))
            self.textbox.setText("Đang xử lý...")
            self.button.setEnabled(False)
            self.save_button.setEnabled(False)
            self.demo_button.setEnabled(True)
            self.extract_text()
            # cv2.imshow("lap rinh", self.image)
            boxes = pytesseract.image_to_data(self.image)
            # print(boxes)

            for x, b in enumerate(boxes.splitlines()):
                if x != 0:
                    print(b)
                    b = b.split()
                    if len(b) == 12:
                        x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                        # cv2.rectangle(self.image, (x, y), (x + w, h + y), (0, 0, 255), 2)
                        cv2.putText(self.imgWhite, b[11], (x, y), cv2.FONT_HERSHEY_PLAIN, 0.9, (50, 50, 255), 1, cv2.LINE_AA)
            cv2.imshow("lap rinh", self.imgWhite)
            cv2.waitKey()
            cv2.destroyWindow()

    def extract_text(self):
        # lang = self.language_combo.currentData()
        pytesseract.pytesseract.tesseract_cmd = "D:\Document\BTL py\Tesseract-OCR\\tesseract.exe"

        lang = self.language_combo.currentData()
        text = pytesseract.image_to_string(self.image, lang=lang)

        # text da dich
        textTran=''

        # in ra man hinh kq test
        print(text)
        if lang != "vie":
            textTran = self.translate_text(text, "vi")
        self.textbox.setText(text)
        self.button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.text = text +"\n kq da dich ra tieng viet \n"+textTran



    def save_text(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Lưu văn bản", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(self.text)
            self.save_button.setEnabled(False)

    def translate_text(self, text, dest_lang):
        translated = self.translator.translate(text, dest=dest_lang)
        return translated.text

    def on_language_change(self, language):
        self.language = language
        self.extract_text()

    def create_language_menu(self):
        self.language_menu = self.menuBar().addMenu("Ngôn ngữ")
        eng_action = self.language_menu.addAction("Tiếng Anh")
        eng_action.triggered.connect(lambda: self.on_language_change("eng"))
        vie_action = self.language_menu.addAction("Tiếng Việt")
        vie_action.triggered.connect(lambda: self.on_language_change("vie"))
        chi_sim_action = self.language_menu.addAction("Tiếng Trung")
        chi_sim_action.triggered.connect(lambda: self.on_language_change("chi_sim"))

    def create_demo_image_button(self):
        self.demo_button = QPushButton("Mẫu hình ảnh", self)
        self.demo_button.move(350, 50)
        self.demo_button.clicked.connect(self.load_demo_image)

    def load_demo_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn tệp hình ảnh", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.image = cv2.imread(file_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.textbox.setText("Đang xử lý...")
            # self.button.setEnabled(False)
            cv2.imshow("anh demo", self.image)

        # demo_path = "demo.jpg"
        # self.image = cv2.imread(demo_path)
        # self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # self.textbox.setText("Đang xử lý...")
        # self.button.setEnabled(False)
        # self.save_button.setEnabled(False)
        # self.extract_text()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())