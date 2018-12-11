# coding:utf-8
# 导入相关文件界面的逻辑功能函数
import sys,os
# import pandas as pd

from importFileUI import Ui_importFileDialog
import myLogging as mylogger
from PyQt5.QtWidgets import QDialog,QWidget,QFileDialog
from PyQt5.QtCore import Qt


# Ui_MainWindow
class importFileDialog(QDialog,Ui_importFileDialog):
    def __init__(self,win,workPath,parent=None):
        # mylogger.logger.debug("QuestionCheckDialog init")
        super(importFileDialog,self).__init__(parent)
        mylogger.logger.debug("importFileDialog init..")
        self.workPath = workPath
        self.win = win

        self.res_path = {"A":"","B":"","住户":"","住宅":"","小区":""}
        self.setupUi(self)
        self.connectSlot()
        mylogger.logger.debug("importFileDialog init ok")

        # self.checkBox = ''

    def connectSlot(self):
        self.A_pushButton.clicked.connect(lambda :self.openFile("A"))
        self.B_pushButton.clicked.connect(lambda :self.openFile("B"))
        self.zhuhu_pushButton.clicked.connect(lambda :self.openFile("住户"))
        self.zhuzhai_pushButton.clicked.connect(lambda :self.openFile("住宅"))
        self.xiaoqu_pushButton.clicked.connect(lambda :self.openFile("小区"))
        self.zy_pushButton.clicked.connect(lambda :self.openFile("账页表"))

    def openFile(self,info=""):
        print("openFile")
        # print(self.win)
        # print(self.workPath)
        filePath, filetype = QFileDialog.getOpenFileName(parent=self.win,caption=info,directory=self.workPath,filter="All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        if filePath.strip() != "":
            if info == "A":
                self.A_path.setText(filePath)
                self.res_path[info] = filePath
            if info == "B":
                self.B_path.setText(filePath)
                self.res_path[info] = filePath
            if info == "住户":
                self.zhuhu_path.setText(filePath)
                self.res_path[info] = filePath
            if info == "住宅":
                self.zhuzhai_path.setText(filePath)
                self.res_path[info] = filePath
            if info == "小区":
                self.xiaoqu_path.setText(filePath)
                self.res_path[info] = filePath
            if info == "账页表":
                self.zy_path.setText(filePath)
                self.res_path[info] = filePath

    def getPath(self):
        return self.res_path



if __name__ == '__main__':
    app = QApplication(sys.argv)
    qcd = QuestionCheckDialog()
    qcd.show()
    sys.exit(app.exec_())