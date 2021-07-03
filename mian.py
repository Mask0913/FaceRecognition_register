from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QApplication, QWidget, QLineEdit,QTextEdit
import sys
from get_face import *
from recognition_face import *

class WinForm(QMainWindow):
    def __init__(self, parent = None):
        super(WinForm, self).__init__(parent)
        self.setWindowTitle('人脸识别打卡')
        self.buton1 = QPushButton('get_face')
        self.buton2 = QPushButton('start')
        self.text = QLineEdit()
        self.content = QTextEdit()
        self.buton1.clicked.connect(self.onButtonClick)
        self.buton2.clicked.connect(self.onButtonClick)

        layout = QHBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.buton1)
        layout.addWidget(self.buton2)
        layout.addWidget(self.content)

        main_frame = QWidget()
        main_frame.setLayout(layout)
        self.setCentralWidget(main_frame)
    def onButtonClick(self):
        sender = self.sender()
        if sender.text() == 'get_face':
            get_faces(self.text.text(),self.content)

        elif sender.text() == 'start':
            reco(self.content)
        else:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = WinForm()
    form.show()
    sys.exit(app.exec_())