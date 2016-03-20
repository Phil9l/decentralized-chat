#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import signal
from optparse import OptionParser
from PyQt5 import QtCore, QtGui, QtWidgets
from json import loads
from client import ChatClient


class ChatThread(QtCore.QThread):
    def __init__(self, port, render_message, get_nickname):
        QtCore.QThread.__init__(self)
        self.chat = ChatClient(port, render_message, get_nickname)

    def run(self):
        while True:
            self.chat.iterate()

    def send_message(self, message):
        self.chat.send_message(message)


class UiMainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(886, 534)
        self.centralWidget = QtWidgets.QWidget(main_window)
        self.centralWidget.setMinimumSize(QtCore.QSize(886, 0))
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(3)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(size_policy)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout.addWidget(self.textBrowser)
        self.listWidget = QtWidgets.QListWidget(self.centralWidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(size_policy)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widget = QtWidgets.QWidget(self.centralWidget)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 30))
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("Сообщение")
        self.gridLayout_2.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        main_window.setCentralWidget(self.centralWidget)

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "Супер Чатик"))
        self.textBrowser.setHtml(_translate(
            "MainWindow",
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">"
            "p, li { white-space: pre-wrap; }</style>"
            "</head><body style=\" font-family:\'Noto Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">"
            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;"
            "-qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"
        ))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("MainWindow", "Send"))
        self.listWidget.itemClicked.connect(self.accost_user)
        self.lineEdit.setFocus()
        self.pushButton.clicked.connect(self.send_message)

    def accost_user(self, user):
        if not self.is_personal_message(self.lineEdit.text(), user.text()):
            self.lineEdit.setText('@{}, {}'.format(user.text(), self.lineEdit.text()))
        self.lineEdit.setFocus()

    def __init__(self, port):
        self.centralWidget = None
        self.gridLayout = None
        self.verticalLayout = None
        self.horizontalLayout = None
        self.textBrowser = None
        self.listWidget = None
        self.widget = None
        self.gridLayout_2 = None
        self.pushButton = None
        self.lineEdit = None
        self.smiles = {}
        self.chat = None
        self.port = port
        self.nickname = ''

        smiles_folder = 'smiles'
        for file in os.listdir(smiles_folder):
            if file.endswith(".png"):
                self.smiles[':{}:'.format(file[:-4])] = os.path.join(smiles_folder, file)

    def start_chatting(self):
        self.chat = ChatThread(self.port, self.render_message, self.get_nickname)
        self.chat.start()
        self.nickname = self.chat.chat.nickname

    def add_user(self, username, me=False):
        self.textBrowser.append('<i>New user in the chat: {}</i>'.format(username))
        _translate = QtCore.QCoreApplication.translate
        item = QtWidgets.QListWidgetItem()
        item.setText(_translate("MainWindow", username))

        if me:
            font = QtGui.QFont()
            font.setBold(True)
            item.setFont(font)

        self.listWidget.addItem(item)

    def remove_item(self, username):
        for index in range(self.listWidget.count()):
            if self.listWidget.item(index).text() == username:
                self.listWidget.takeItem(index)
                self.textBrowser.append('<i>{} left the chat</i>'.format(username))
                break

    @staticmethod
    def is_personal_message(message, user):
        return len(re.findall(r'@{}\W'.format(user), message)) > 0

    def insert_smiles(self, message):
        for code, file in self.smiles.items():
            message = message.replace(code, '<img src="{}" />'.format(file))
        return message

    def handle_message(self, message):
        self.textBrowser.append('<b>{}:</b> <span style="{}">{}</span>'.format(
            message['nickname'],
            'color: #f36223;font-weight:bold;' if self.is_personal_message(message['data'], self.nickname) else '',
            self.insert_smiles(message['data'])
        ))

    def render_message(self, message):
        self.handle_message(loads(message))

    # TODO
    @staticmethod
    def get_nickname():
        return 'test'

    def send_message(self):
        self.chat.send_message(self.lineEdit.text())
        self.lineEdit.setText('')


def signal_handler(signal, frame):
    sys.exit(0)


def get_options():
    parser = OptionParser(usage='usage: %prog [options] hostname')
    parser.add_option(
        '-p', '--port', dest='port', help='Run server on given port',
        type='int', metavar='PORT', default=8888
    )
    (opt, args) = parser.parse_args()
    return opt, args


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    (options, args) = get_options()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow(options.port)

    ui.setup_ui(MainWindow)
    MainWindow.show()
    ui.add_user('phil9l', True)
    ui.add_user('r0mjk3')
    # ui.handle_message({'nickname': 'phil9l', 'data': 'Флэш просто сущий макро терран :peka:'})
    # ui.handle_message({'nickname': 'r0mjk3', 'data': 'Всё тлен :grumpy:'})
    # ui.handle_message({'nickname': 'r0mjk3', 'data': '@phil9l, Привет :kawai:'})
    ui.start_chatting()
    app.exec_()

