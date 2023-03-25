from storage import Storage, Client
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton
import sys


class TextEditDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("QTextEdit")
        self.resize(300, 270)

        self.textEdit = QTextEdit()
        self.btnPress = QPushButton("get clients")

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.btnPress)
        self.setLayout(layout)

        self.btnPress.clicked.connect(self.btnPress_Clicked)

    def btnPress_Clicked(self):
        storage = Storage('server')
        clients = storage.select(Client).all()
        text = 'clients registered on server\n'
        for client in clients:
            text += f"{client.id} {client.login}\n"
        self.textEdit.setPlainText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TextEditDemo()
    win.show()
    sys.exit(app.exec_())