"""
设置QTableWidget的滚动条样式

"""
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
import requests

Style = '''
        QCheckBox
        {
        padding-left:13px;
        }
        QHeaderView     
        {
        border: none;
        border-bottom: 3px solid rgb(0, 160, 230);
        background: rgb(57, 58, 60);
        min-height: 30px;
        }    

        QScrollBar:vertical {
        width: 20px;
        background: transparent;
        margin-left: 3px;
        margin-right: 3px;
        }
        QScrollBar::handle:vertical {
                width: 20px;
                min-height: 30px;
                background: rgb(68, 69, 73);
                margin-top: 15px;
                margin-bottom: 15px;
        }
        QScrollBar::handle:vertical:hover {
                background: rgb(80, 80, 80);
        }
        QScrollBar::sub-line:vertical {
                height: 15px;
                background: transparent;
                image: url(:/Black/arrowTop);
                subcontrol-position: top;
        }
        QScrollBar::add-line:vertical {
                height: 15px;
                background: transparent;
                image: url(:/Black/arrowBottom);
                subcontrol-position: bottom;
        }
        QScrollBar::sub-line:vertical:hover {
                background: rgb(68, 69, 73);
        }
        QScrollBar::add-line:vertical:hover {
                background: rgb(68, 69, 73);
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent;
        }

        QScrollBar#verticalScrollBar:vertical {
                margin-top: 30px;
        }
'''


class MainUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_qss()
        self.CreateSignalSlot()
        self.getWeather()

    def init_ui(self):
        self.setFixedSize(560, 600)
        self.main_widget = QWidget()  # 创建窗口主部件
        self.main_layout = QHBoxLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.left_widget = QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QVBoxLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网

        self.btn_widget = QWidget()
        self.btn_layout = QGridLayout()
        self.btn_widget.setLayout(self.btn_layout)
        self.left_layout.addWidget(self.btn_widget)

        self.right_widget = QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget)  # 左侧部件在第0行第0列，占12行2列
        self.main_layout.addWidget(self.right_widget)  # 右侧部件在第0行第3列，占12行10列

        # 左侧菜单栏
        self.left_close = QPushButton("")  # 关闭按钮
        self.left_visit = QPushButton("")  # 空白按钮
        self.left_mini = QPushButton("")  # 最小化按钮
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小
        self.btn_layout.addWidget(self.left_close, 0, 0, 1, 1)
        self.btn_layout.addWidget(self.left_mini, 0, 1, 1, 1)
        self.btn_layout.addWidget(self.left_visit, 0, 2, 1, 1, )

        self.tree = QTreeWidget()
        self.tree.setFont(QFont('微软雅黑', 12))
        # tree.setColumnCount(1)
        # tree.setHeaderLabels(['key'])
        self.tree.setHeaderHidden(True)
        # 根节点1
        self.root_task = QTreeWidgetItem(self.tree)
        self.root_task.setText(0, '待办事项')
        self.root_task.setIcon(0, QIcon('icons/todo.png'))
        # self.tree.setColumnWidth(0, 60)

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
        self.root_thing.setText(0, '事件纪录')
        self.root_thing.setIcon(0, QIcon('icons/thing.png'))
        self.left_layout.addWidget(self.tree)

        # 右边tab

        self.tab = QTabWidget()
        self.tab1 = QWidget()
        self.wellabel = QLabel('<font color=red size=200><b>Welcome！</b></font>', self.tab1)
        self.wellabel.move(130, 30)
        self.lcity = QLabel(self.tab1)
        self.lcity.move(160, 80)
        self.lwd = QLabel(self.tab1)
        self.lwd.move(160, 110)
        self.ltemp = QLabel(self.tab1)
        self.ltemp.move(160, 140)
        self.lws = QLabel(self.tab1)
        self.lws.move(160, 170)
        self.lsd = QLabel(self.tab1)
        self.lsd.move(160, 200)
        self.todoTableWidget = QTableWidget()
        self.tab3 = QTableWidget()

        self.tab.addTab(self.tab1, '选项卡1')
        self.tab.addTab(self.todoTableWidget, '选项卡2')
        self.tab.addTab(self.tab3, '选项卡3')
        self.right_layout.addWidget(self.tab, 0, 0,12,12)

        # 添加表格按钮-----------------------------------------------
        from_btn_widget = QWidget()
        form_btn_layout = QHBoxLayout()
        from_btn_widget.setLayout(form_btn_layout)
        btn_add = QPushButton('添加')
        btn_add.clicked.connect(self.add_row)
        btn_delete = QPushButton('删除')
        form_btn_layout.addWidget(btn_add)
        form_btn_layout.addWidget(btn_delete)
        self.right_layout.addWidget(from_btn_widget,13,0,1,12)

    def init_qss(self):
        # QSSSSSSSSSSSSSSSSSSSSSSSSSS

        # 左侧
        self.left_widget.setFixedWidth(140)

        # 左侧按钮
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:7px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:7px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:7px;}QPushButton:hover{background:green;}''')
        # 左侧树
        self.tree.setStyleSheet('''
                QTreeWidget{
                background-color:gray;
                border:None;
                border-bottom-left-radius:10px;
                border-bottom:1px solid white;
                border-left:1px solid white;
                }
                ''')

        # 右侧窗口
        self.right_widget.setStyleSheet('''
          QWidget#right_widget{
            color:#232C51;
            background:white;
            border-top:1px solid darkGray;
            border-bottom:1px solid darkGray;
            border-right:1px solid darkGray;
            border-top-right-radius:10px;
            border-bottom-right-radius:10px;
          }
          QLabel#right_lable{
            border:none;
            font-size:16px;
            font-weight:700;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
          }
          ''')
        self.tab.tabBar().setVisible(False)  # 隐藏选项卡标题
        self.tab.setStyleSheet('''
        QTabWidget::pane {
        border:1px solid gray;
        border-top-right-radius:10px;
        border-bottom-right-radius:10px;
        }
        ''')
        self.todoTableWidget.setStyleSheet('''
        QTableWidget {
        border:1px solid gray;
        border-top-right-radius:10px;
        border-bottom-right-radius:10px;
        }
        ''')
        # self.todoTableWidget.QScrollBar.setStyleSheet('''
        # QScrollBar {
        # border:1px solid gray;
        # border-top-right-radius:10px;
        # border-bottom-right-radius:10px;
        # }
        # ''')

        # 设置窗口背景透明
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        # 再对左侧部件添加QSS
        self.main_widget.setStyleSheet('''
                QWidget#left_widget{
                background:gray;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
                }
                ''')

        # 去掉左右部件间的缝隙
        self.main_layout.setSpacing(0)
        # self.main_layout.setContentsMargins(0,0,0,0)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setContentsMargins(0, 0, 0, 0)

    # -----------------------------------------------
    def add_row(self):
        rc = self.todoTableWidget.rowCount()
        print(rc)
        self.todoTableWidget.insertRow(rc)
        checkBox = QCheckBox()
        self.todoTableWidget.setCellWidget(rc, 1, checkBox)



    # 信号与槽
    def CreateSignalSlot(self):
        self.tree.clicked.connect(self.onTreeClick)

        self.left_close.clicked.connect(self.close)
        self.left_visit.clicked.connect(self.maxOrNormal)
        self.left_mini.clicked.connect(self.clickmini)

        # self.todoTableWidget.customContextMenuRequested.connect(self.generateMenu)
        # # tab.resize(200,200)

    # 获取首页天气信息并显示
    def getWeather(self):
        print('* queryWeather  ')
        rep = requests.get('http://www.weather.com.cn/data/sk/101020100.html')
        rep.encoding = 'utf-8'
        print(rep.json())

        msg1 = '城市: %s' % rep.json()['weatherinfo']['city'] + '\n'
        msg2 = '风向: %s' % rep.json()['weatherinfo']['WD'] + '\n'
        msg3 = '温度: %s' % rep.json()['weatherinfo']['temp'] + ' 度' + '\n'
        msg4 = '风力: %s' % rep.json()['weatherinfo']['WS'] + '\n'
        msg5 = '湿度: %s' % rep.json()['weatherinfo']['SD'] + '\n'
        result = msg1 + msg2 + msg3 + msg4 + msg5
        self.lcity.setText(msg1)
        self.lwd.setText(msg2)
        self.ltemp.setText(msg3)
        self.lws.setText(msg4)
        self.lsd.setText(msg5)

    # 窗口按钮功能
    def clickmini(self):
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.showMinimized()

    def maxOrNormal(self):
        pass
        # if self.isMaximized():
        #     self.showNormal()
        # else:
        #     self.showMaximized()

    # 左侧树点击事件
    def onTreeClick(self, index):
        # print(index.row())
        item = self.tree.currentItem()
        text1 = item.text(0)
        if text1 == '待办事项':
            self.getTodoView()
            self.tab.setCurrentIndex(1)
        elif text1 == '提醒':
            self.tab.setCurrentIndex(2)
            # 显示表格
        elif text1 == '事件记录':
            self.tab.setCurrentIndex(3)
        else:
            return

    def getTodoView(self):
        # 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果
        data, num = getTodoData()
        print(data, num)
        self.todoTableWidget.setRowCount(num)
        self.todoTableWidget.setColumnCount(3)
        self.todoTableWidget.setHorizontalHeaderLabels(['任务名', '状态', '任务内容'])

        self.todoTableWidget.setColumnWidth(1, 40)
        # TODO 优化 2 设置水平方向表格为自适应的伸缩模式
        # self.todoTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.todoTableWidget.horizontalHeader().setStretchLastSection(True)
        # TODO 优化3 将表格变为禁止编辑
        # self.todoTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # TODO 优化 4 设置表格整行选中
        self.todoTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # TODO 优化 5 将行与列的高度设置为所显示的内容的宽度高度匹配
        # QTableWidget.resizeColumnsToContents(self.todoTableWidget)
        # QTableWidget.resizeRowsToContents(self.todoTableWidget)

        for row, i in enumerate(data):
            self.todoTableWidget.setItem(row, 0, QTableWidgetItem(i["taskname"]))
            self.checkBox = QCheckBox()
            self.checkBox.stateChanged.connect(self.handleCheckbox)
            self.checkBox.setChecked(i["status"])
            self.todoTableWidget.setCellWidget(row, 1, self.checkBox)
            self.todoTableWidget.setItem(row, 2, QTableWidgetItem(i["details"]))
            self.todoTableWidget.setRowHeight(row, 35)
            if i["status"]:
                # self.todoTableWidget.item(row, 0).setBackground(Qt.red)
                self.todoTableWidget.cellWidget(row,1).setStyleSheet('''QCheckBox{background:red;}''')
                # self.todoTableWidget.item(row, 2).setBackground(Qt.red)

    def handleCheckbox(self, statuNum):
        print('*'*100)
        print(statuNum)
        s = self.todoTableWidget.sender()  # 获取发信号的对象
        print(s.isChecked())
        index = self.todoTableWidget.indexAt(s.pos())  # 获取对象在表中的位置
        row = index.row()
        col = index.column()
        print(row, col)
        if s.isChecked() == True:
            print('checked')
            # self.todoTableWidget.item(row,0).setBackground(Qt.red)
            self.todoTableWidget.cellWidget(row,1).setStyleSheet('''QCheckBox{background:red;}''')
            # self.todoTableWidget.item(row,2).setBackground(Qt.red)
        else:
            # self.todoTableWidget.item(row, 0).setBackground(Qt.white)
            self.todoTableWidget.cellWidget(row, 1).setStyleSheet('''QCheckBox{background:white;}''')
            # self.todoTableWidget.item(row, 2).setBackground(Qt.white)
        pass


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(Style)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
