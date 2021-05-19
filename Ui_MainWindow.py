from getData import *
from TrayIcon import TrayIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5 import QtPrintSupport
from PyQt5.QtSql import *
import sys
import os
from Lib.AnimationShadowEffect import AnimationShadowEffect



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.setWindowIcon(QIcon('icons/D.ico'))
        self.resize(560, 600)
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        self.setObjectName("MainWindow")
        self.setStyleSheet("#MainWindow{background-color:rgb(229,229,229)}")
        # pe = QPalette()
        # self.setAutoFillBackground(True)
        # pe.setColor(QPalette.Window, Qt.lightGray)  # 设置背景色
        # self.setPalette(pe)



        # 左半边
        self.frame_left = QFrame()
        self.frame_left.setMaximumWidth(140)
        self.vlayout_left = QVBoxLayout(self.frame_left)
        # 加载logo
        self.frame_logo = QFrame()
        # frame_logo.setFrameShape(QFrame.StyledPanel)
        self.frame_logo.setMaximumHeight(140)
        self.pix = QPixmap('icons/D.ico')
        self.lb_img = QLabel(self.frame_logo)
        # lb_img.setGeometry(0, 0, 300, 200)
        # lb_img.setStyleSheet("border: 2px solid red")
        self.lb_img.setPixmap(self.pix)

        # 创建按钮
        self.frame_button = QFrame()
        # frame_button.setFrameShape(QFrame.StyledPanel)
        self.frame_logo.setMaximumHeight(130)
        self.button_create = QPushButton('新建',self.frame_button)
        self.button_create.setIcon(QIcon('icons/create.png'))
        self.button_create.setObjectName('btncreate')
        self.button_create.setGeometry(5,10,110,40)
        self.button_create.setStyleSheet("QPushButton#btncreate{border-radius:20px}"
                                    "QPushButton#btncreate{background-color:rgb(52,155,253)}"
                                    "QPushButton#btncreate{color:white}"
                                    "QPushButton#btncreate{font-size:14px}"
                                    )

        # 树控件
        self.tree = QTreeWidget()
        self.tree.setStyleSheet("QTreeWidget{background-color:rgb(229,229,229)}"
                           "QTreeWidget{border:None}")
        self.tree.setFont(QFont('微软雅黑',12))
        # tree.setColumnCount(1)
        # tree.setHeaderLabels(['key'])
        self.tree.setHeaderHidden(True)
        # 根节点1
        self.root_task = QTreeWidgetItem(self.tree)
        self.root_task.setText(0, '待办事项')
        self.root_task.setIcon(0, QIcon('icons/todo.png'))
        self.tree.setColumnWidth(0, 60)

        # 根节点2
        self.root_remind = QTreeWidgetItem(self.tree)
        self.root_remind.setText(0, '提醒')
        self.root_remind.setIcon(0, QIcon('icons/alarmclock.png'))
        # remind_child1 = QTreeWidgetItem(root_remind)
        # remind_child1.setText(0, '定时提醒')
        # remind_child2 = QTreeWidgetItem(root_remind)
        # remind_child2.setText(0, '短时提醒')

        # 跟节点3
        self.root_thing = QTreeWidgetItem(self.tree)
        self.root_thing.setText(0,'事件纪录')
        self.root_thing.setIcon(0, QIcon('icons/thing.png'))

        self.vlayout_left.addWidget(self.frame_logo)
        self.vlayout_left.addWidget(self.frame_button)
        # vlayout_left.addSpacing()
        # vlayout_left.addWidget(button_create,0,Qt.AlignCenter)
        self.vlayout_left.addWidget(self.tree)
        self.vlayout_left.setStretchFactor(self.frame_logo,2)
        self.vlayout_left.setStretchFactor(self.frame_button,1)
        self.vlayout_left.setStretchFactor(self.tree,6)



        # 最小化、放大、关闭按钮组件
        self.hlayout_switch = QHBoxLayout()

        self.pushbutton_close = QPushButton()
        self.pushbutton_close.setObjectName("pushButton")


        self.pushButton_max = QPushButton()
        self.pushButton_max.setGeometry(QRect(80, 20, 30, 30))
        self.pushButton_max.setObjectName("pushButton_2")
        self.pushbutton_mini = QPushButton()
        self.pushbutton_mini.setGeometry(QRect(130, 20, 30, 30))
        self.pushbutton_mini.setObjectName("pushbutton_mini")
        self.hlayout_switch.addStretch(1)
        self.hlayout_switch.addWidget(self.pushbutton_mini)
        self.hlayout_switch.addWidget(self.pushButton_max)
        self.hlayout_switch.addWidget(self.pushbutton_close)

        # 右半边
        self.vlayout_right = QVBoxLayout()
        # tab选项卡窗口
        self.tabMain = QTabWidget()
        self.tab1 = QWidget()
        self.wellabel = QLabel('<font color=red size=200><b>Welcome！</b></font>',self.tab1)
        self.wellabel.move(130,30)
        self.lcity = QLabel(self.tab1)
        self.lcity.move(160, 80)
        self.lwd = QLabel(self.tab1)
        self.lwd.move(160,110)
        self.ltemp = QLabel(self.tab1)
        self.ltemp.move(160, 140)
        self.lws = QLabel(self.tab1)
        self.lws.move(160, 170)
        self.lsd = QLabel(self.tab1)
        self.lsd.move(160, 200)

        self.tab2 = QDialog()
        self.todoTableWidget = QTableWidget()
        # self.todoTableWidget.setModel()




        self.tab3 = QWidget()


        # 右键菜单
        self.todoTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # tab.resize(200,200)
        self.tabMain.tabBar().setVisible(False)  # 隐藏选项卡标题
        self.tabMain.addTab(self.tab1,'选项卡1')
        self.tabMain.addTab(self.tab2,'选项卡2')
        self.tabMain.addTab(self.tab3,'选项卡3')
        self.vlayout_right.addLayout(self.hlayout_switch)
        self.vlayout_right.addWidget(self.tabMain)


        # 总窗口
        self.hlayout_window = QHBoxLayout()
        self.hlayout_window.addWidget(self.frame_left)
        self.hlayout_window.addLayout(self.vlayout_right)
        self.hlayout_window.setStretch(0,0)
        self.hlayout_window.setStretch(1,1)

        # self.setLayout(self.hlayout_window)
        self.centralwidget.setLayout(self.hlayout_window)


    #
    # def retranslateUi(self, MainWindow):
    #     _translate = QCoreApplication.translate
    #     MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
    #     self.pushButton.setText(_translate("MainWindow", "PushButton"))
    #     self.radioButton.setText(_translate("MainWindow", "RadioButton"))