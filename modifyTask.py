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


class modifyTask(QDialog):
    def __init__(self, parent=None):
        super(modifyTask, self).__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(300, 300)
        self.setWindowTitle('修改任务')
        self.tasknameedit = QLineEdit()
        self.taskedit = QTextEdit()
        self.form = QFormLayout()
        # self.buttonok = QPushButton('我是按钮')
        # self.buttonok.clicked.connect(self.test)
        self.btn_confirm = QPushButton('确认修改')
        self.btn_confirm.setFixedWidth(100)
        self.btn_confirm.setFixedHeight(40)
        aniButton = AnimationShadowEffect(Qt.blue, self.btn_confirm)
        self.btn_confirm.setGraphicsEffect(aniButton)

        self.form.addRow('任务名',self.tasknameedit)
        self.form.addRow('任务内容',self.taskedit)
        self.form.addRow('',self.btn_confirm)
        self.setLayout(self.form)

    def test(self):
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons/D.ico"))
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = modifyTask()
    window.show()
    sys.exit(app.exec_())