import os
import sys
import random
from functools import partial

from PySide6 import QtGui
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import *
from database import DataBase
from datetime import datetime

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        loader = QUiLoader()
        self.ui = loader.load('form.ui')

        self.ui.show()
        self.dark = False

        self.ui.setWindowIcon(QtGui.QIcon('logo.png'))

        self.message_restriction = 3600  # in seconds


        self.ui.btn_dark.clicked.connect(self.dark_theme)
        self.ui.btn_ref.clicked.connect(self.readMessages)
        self.ui.btn_del_all.clicked.connect(self.del_all)
        self.ui.btn_send.clicked.connect(self.addNewMessage)
        self.readMessages()


    def del_all(self):
        for i in reversed(range(self.ui.gl_messages.count())):
            self.ui.gl_messages.itemAt(i).widget().setParent(None)
        DataBase.delete_all()
        # self.refresh_messages()

    def refresh_messages(self):
        for i in reversed(range(self.ui.gl_messages.count())):
            self.ui.gl_messages.itemAt(i).widget().setParent(None)
        self.readMessages()

    def dark_theme(self):
        if not self.dark:
            self.ui.setStyleSheet("background-color: rgb(80, 80, 80)")
            self.dark = not self.dark
        else:
            self.ui.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.dark = not self.dark

    def readMessages(self):
        messages = DataBase.select()

        for i, message in enumerate(messages):
            label = QLabel()
            label.setText(message[3] + "-" + message[1] + ": " + message[2])
            self.ui.gl_messages.addWidget(label, i, 1)

            btn = QPushButton()
            btn.setIcon(QIcon('recycle bin.png'))
            btn.setFixedWidth(20)
            btn.clicked.connect(partial(self.delete_message, btn, i))
            self.ui.gl_messages.addWidget(btn, i, 0)

    def delete_message(self, btn, i):
        self.ui.gl_messages.itemAt(i).widget().setParent(None)
        messages = DataBase.select()
        id_list = [item[0] for item in messages]
        target_id = id_list[i]
        DataBase.delete(target_id)
        self.refresh_messages()

    def empty_layout(self):
        for i in reversed(range(self.ui.gl_messages.count())):
            self.ui.gl_messages.itemAt(i).widget().setParent(None)  # .deleteLater()
            self.ui.gl_messages.itemAt(i).widget().deleteLater()


    def addNewMessage(self):
        messages = DataBase.select()
        name = self.ui.tb_name.text()
        text = self.ui.tb_text.text()
        if name != "" and text != "":

            allow_to_send_message, min_ = DataBase.last_message_time_check(name, self.message_restriction)

            if allow_to_send_message:
                response = DataBase.insert(name, text)
                if response:
                    label = QLabel()
                    label.setText(name + ": " + text)

                    # add message and recycle bin
                    self.ui.gl_messages.addWidget(label, len(messages)+1, 1)
                    btn = QPushButton()
                    btn.setIcon(QIcon('recycle bin.png'))
                    btn.setFixedWidth(20)
                    btn.clicked.connect(partial(self.delete_message, btn, len(messages)+1))
                    self.ui.gl_messages.addWidget(btn, len(messages)+1, 0)

                    self.ui.tb_name.setText("")
                    self.ui.tb_text.setText("")

                    mes_box = QMessageBox()
                    mes_box.setText("your message sent")
                    mes_box.exec()
                else:
                    mes_box = QMessageBox()
                    mes_box.setText("Database Error")
                    mes_box.exec()
            else:
                minute = min_ // 60
                QMessageBox.warning(self, 'Warning', f"Too many messages, please wait {minute} minutes")

        else:
            msg_box = QMessageBox()
            msg_box.setText("Error: empty feilds")
            msg_box.exec()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
