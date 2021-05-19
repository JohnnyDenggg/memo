import sys
from PyQt5.QtWidgets import *
from getData import *

class Table(QWidget):
    def __init__(self):
        super(Table, self).__init__()
        self.initUI()
        self.todo()
    def initUI(self):
        self.setWindowTitle("QTableWidget例子")
        self.resize(400,600)
        self.layout=QVBoxLayout()

        self.todoTableWidget = QTableWidget()
        self.todoTableWidget.clicked.connect(self.findrow)
        # self.todoTableWidget.setEditTriggers()
        # self.todoTableWidget.itemChanged()


    def todo(self):
        # 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果
        data, num = getTodoData()
        self.todoTableWidget.setRowCount(num)
        self.todoTableWidget.setColumnCount(3)
        self.todoTableWidget.setHorizontalHeaderLabels(['任务名', '状态', '任务内容'])
        self.todoTableWidget.setColumnWidth(1, 20)
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
            # celllayout.addWidget(checkBox)
            # celllayout.setAlignment(checkBox, Qt.AlignCenter)
            checkBox.setChecked(i["status"])
            # widget.setLayout(celllayout)
            self.todoTableWidget.setCellWidget(row, 1, checkBox)
            self.todoTableWidget.setItem(row, 2, QTableWidgetItem(i["details"]))
            self.todoTableWidget.setRowHeight(row, 35)

        # # 允许右键产生菜单
        # self.todoTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # # 将右键菜单绑定到槽函数generateMenu
        # self.todoTableWidget.customContextMenuRequested.connect(self.generateMenu)

        self.layout.addWidget(self.todoTableWidget)
        self.button = QPushButton('删除')
        self.button.clicked.connect(self.removerow)
        self.layout.addWidget(self.button)

        self.button1 = QPushButton('添加行')
        self.button1.clicked.connect(self.addrow)
        self.layout.addWidget(self.button1)
        # 进度条
        self.bar = QProgressBar()
        self.bar.setValue(50)
        self.layout.addWidget(self.bar)


        self.setLayout(self.layout)

    def findrow(self,i):
        delrow = i.row()
        print('delrow =%s' % str(delrow))
        print(self.todoTableWidget.item(delrow, 0).text(),
              self.todoTableWidget.cellWidget(delrow,1).isChecked(),
              self.todoTableWidget.item(delrow, 2).text())


    def removerow(self):
        self.todoTableWidget.removeRow(self.todoTableWidget.currentIndex().row())

    def addrow(self):
        self.todoTableWidget.insertRow(self.todoTableWidget.rowCount(),1)
        # print('insertRow=%s' % str(ret))


if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=Table()
    win.show()
    sys.exit(app.exec_())
