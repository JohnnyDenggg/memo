from getData import *
from TrayIcon import TrayIcon
from Ui_MainWindow import Ui_MainWindow
from addTask import addTask
from modifyTask import modifyTask
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5 import QtPrintSupport
from PyQt5.QtSql import *
import sys
import os
import requests

Style = """
QMenu {
    /* 半透明效果 */
    background-color: rgba(255, 255, 255, 230);
    border: none;
    border-radius: 4px;
}

QMenu::item {
    border-radius: 4px;
    /* 这个距离很麻烦需要根据菜单的长度和图标等因素微调 */
    padding: 8px 48px 8px 36px; /* 36px是文字距离左侧距离*/
    background-color: transparent;
}

/* 鼠标悬停和按下效果 */
QMenu::item:selected {
    border-radius: 0px;
    /* 半透明效果 */
    background-color: rgba(232, 232, 232, 232);
}

/* 禁用效果 */
QMenu::item:disabled {
    background-color: transparent;
}

/* 图标距离左侧距离 */
QMenu::icon {
    left: 15px;
}

/* 分割线效果 */
QMenu::separator {
    height: 1px;
    background-color: rgb(232, 236, 243);
}
"""

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.getWeather()
        self.CreateSignalSlot()

    def getWeather(self):
        print('* queryWeather  ')
        # cityName = self.ui.weatherComboBox.currentText()
        # cityCode = self.transCityName(cityName)

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

    # def transCityName(self, cityName):
    #     cityCode = ''
    #     if cityName == '北京':
    #         cityCode = '101010100'
    #     elif cityName == '天津':
    #         cityCode = '101030100'
    #     elif cityName == '上海':
    #         cityCode = '101020100'
    #
    #     return cityCode
    #
    # def clearResult(self):
    #     print('* clearResult  ')
    #     self.ui.resultText.clear()



# 信号与槽
    def CreateSignalSlot(self):
        self.tree.clicked.connect(self.onTreeClick)

        self.pushbutton_close.clicked.connect(self.close)
        self.pushButton_max.clicked.connect(self.maxOrNormal)
        self.pushbutton_mini.clicked.connect(self.clickmini)

        # self.todoTableWidget.clicked.connect()

        self.todoTableWidget.customContextMenuRequested.connect(self.generateMenu)
        # tab.resize(200,200)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def getTodoView(self):

        # 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果
        data, num = getTodoData()
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
            widget = QWidget()
            celllayout = QHBoxLayout()
            checkBox = QCheckBox()
            celllayout.addWidget(checkBox)
            celllayout.setAlignment(checkBox, Qt.AlignCenter)
            checkBox.setChecked(i["status"])
            widget.setLayout(celllayout)
            self.todoTableWidget.setCellWidget(row, 1, widget)
            self.todoTableWidget.setItem(row, 2, QTableWidgetItem(i["details"]))
            self.todoTableWidget.setRowHeight(row, 35)
        layout_table = QVBoxLayout()
        layout_table.addWidget(self.todoTableWidget)
        self.tab2.setLayout(layout_table)


    def clickmini(self):
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.showMinimized()

    # 右键菜单槽
    def generateMenu(self,pos):
        print(pos)
        for i in self.todoTableWidget.selectionModel().selection().indexes():
            rowNum = i.row()
        print(rowNum)
        # 如果行索引小于2，弹出菜单。也就是前两行才弹出菜单

        menu = QMenu()
        item1 = menu.addAction('添加任务')
        item2 = menu.addAction('修改任务')
        item3 = menu.addAction('删除任务')
        screenPos = self.todoTableWidget.mapToGlobal(pos)
        # 被阻塞
        action = menu.exec(screenPos)
        # print('action',action)
        if action ==item1:
            print('添加任务')
            addtask = addTask()
            addtask.show()
            addtask.exec_()
        elif action ==item2:
            print('删除任务')
            modifytask = modifyTask()
            modifytask.show()
            modifytask.exec_()
        elif action ==item3:
            print('删除任务')
            self.todoTableWidget.removeRow(self.todoTableWidget.currentIndex().row())
            # print('选择了添加行2',self.todoTableWidget.item(rowNum,0).text())
        else:
            return

    def onTreeClick(self,index):
        # print(index.row())
        item = self.tree.currentItem()
        text1 = item.text(0)
        if text1=='待办事项':
            self.getTodoView()
            self.tabMain.setCurrentIndex(1)
        elif text1 == '提醒':
            self.tabMain.setCurrentIndex(2)
            # 显示表格
        elif text1=='事件记录':
            self.tabMain.setCurrentIndex(3)
        else:
            return

    def maxOrNormal(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()




# def initializeModel(model):
#     # 创建表
#     model.setTable('todo')
#     # 修改
#     model.setEditStrategy(QSqlTableModel.OnFieldChange)
#     model.select()
#     # model.setHeaderData(0,Qt.Horizontal,'ID')
#     model.setHeaderData(1,Qt.Horizontal,'任务内容')
#     model.setHeaderData(2,Qt.Horizontal,'完成状态')
#
# def createView(title,model):
#     view = QTableView()
#     view.setModel(model)
#     view.setWindowTitle(title)
#     return view
#
# def findrow(i):
#     delrow = i.row()
#     print('del row =%s' % str(delrow))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(Style)
    window = MainWindow()
    window.show()
    # 托盘图标
    ti = TrayIcon(window)
    ti.show()

    sys.exit(app.exec_())