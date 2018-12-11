# coding:utf-8
# 审核账页界面的逻辑功能函数

import sys,os
# import pandas as pd
# import numpy as np
# import json
from zyCheckUI import Ui_zyCheckDialog
import myLogging as mylogger
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog,QApplication
from PyQt5.QtCore import Qt


# Ui_MainWindow
class zyCheckDialog(QDialog,Ui_zyCheckDialog):
    def __init__(self,parent=None):
        super(zyCheckDialog,self).__init__(parent)
        mylogger.logger.debug("zyCheckDialog init..")
        self.setupUi(self)
        self.townLowSpinBox.setEnabled(False)
        self.townUpperSpinBox.setEnabled(False)
        self.connectSlot()
        mylogger.logger.debug("zyCheckDialog init ok")

    def connectSlot(self):
        # 小区范围
        self.allTownRadioButton.toggled.connect(self.setTownDisabled)
        self.partTownRadioButton.toggled.connect(self.setTownEnabled)
        # 审核月份
        self.allMonthRadioButton.toggled.connect(self.setMonthDisabled)
        self.partMonthRadioButton.toggled.connect(self.setMonthEnabled)
        # 浏览路径
        self.selectPathButton.clicked.connect(self.selectFileSavePath)

    def setTownDisabled(self):
        self.townLowSpinBox.setEnabled(False)
        self.townUpperSpinBox.setEnabled(False)

    def setTownEnabled(self):
        self.townLowSpinBox.setEnabled(True)
        self.townUpperSpinBox.setEnabled(True)

    def setMonthDisabled(self):
        self.monthLowSpinBox.setEnabled(False)
        self.monthUpperSpinBox.setEnabled(False)

    def setMonthEnabled(self):
        self.monthLowSpinBox.setEnabled(True)
        self.monthLowSpinBox.setEnabled(True)

    def selectFileSavePath(self):
        dir = QFileDialog.getExistingDirectory(self,"选取文件夹",os.getcwd())
        self.dirlineEdit.setText(dir)

    def getData(self):
        Zn = self.zy_necessity.isChecked()
        Zs = self.zy_suggestion.isChecked()
        Za = self.zy_addition.isChecked()
        townRange = 0
        monthRange = 0
        directory = self.dirlineEdit.text()

        if self.partTownRadioButton.isChecked() == True:
            townLowValue = self.townLowSpinBox.value()
            townUpperValue = self.townUpperSpinBox.value()
            townRange = townLowValue * 100 + townUpperValue
            # print(townRange)

        if self.partMonthRadioButton.isChecked() == True:
            monthLowValue = self.monthLowSpinBox.value()
            monthUpperValue = self.monthUpperSpinBox.value()
            monthRange = monthLowValue * 100 + monthUpperValue

        return Zn,Zs,Za,townRange,monthRange,directory


if __name__ == '__main__':
    app = QApplication(sys.argv)
    zy_check = zyCheckDialog()
    zy_check.show()
    sys.exit(app.exec_())





