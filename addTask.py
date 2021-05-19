from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.uic import loadUiType
from PyQt5 import QtPrintSupport
import sys
import os
import qdarkstyle
from Lib.AnimationShadowEffect import AnimationShadowEffect

class addTask(QDialog):
    def __init__(self, parent=None):
        super(addTask, self).__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle('添加任务')
        self.resize(300, 300)
        self.form = QFormLayout()

        self.tasknameedit = QLineEdit()

        self.tasktime = QDateTimeEdit(QDateTime.currentDateTime())
        self.tasktime.setCalendarPopup(True)
        self.tasktime.setDisplayFormat('yyyy-MM-dd HH:mm:00')

        self.taskedit = QTextEdit()
        self.btn_confirm = QPushButton('创建任务')
        self.btn_confirm.setFixedWidth(100)
        self.btn_confirm.setFixedHeight(40)
        self.btn_confirm.clicked.connect(self.onBtnConfirm)
        aniButton = AnimationShadowEffect(Qt.blue, self.btn_confirm)
        self.btn_confirm.setGraphicsEffect(aniButton)

        self.form.addRow('任务名',self.tasknameedit)
        self.form.addRow('任务时间', self.tasktime)
        self.form.addRow('任务内容',self.taskedit)
        self.form.addRow('',self.btn_confirm)
        self.setLayout(self.form)

    def onBtnConfirm(self):
        name = self.tasknameedit.text()
        time = self.tasktime.dateTime()
        print(str(time))




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons/D.ico"))
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = addTask()
    window.show()
    sys.exit(app.exec_())