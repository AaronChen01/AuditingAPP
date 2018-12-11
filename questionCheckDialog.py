# coding:utf-8
# 审核问卷界面的逻辑功能函数
import sys,os
import pandas as pd
import numpy as np
import json
from questionCheckUI import Ui_questionCheck
import myLogging as mylogger
from PyQt5.QtWidgets import QApplication, QMainWindow,QDialog
from PyQt5.QtWidgets import QDesktopWidget,QFileDialog,QTableWidgetItem,QMainWindow
from PyQt5.QtCore import Qt


# Ui_MainWindow
class QuestionCheckDialog(QDialog,Ui_questionCheck):
    def __init__(self,parent=None):
        # mylogger.logger.debug("QuestionCheckDialog init")
        super(QuestionCheckDialog,self).__init__(parent)
        mylogger.logger.debug("QuestionCheckDialog init..")
        self.setupUi(self)
        self.connectSlot()
        mylogger.logger.debug("QuestionCheckDialog init ok")

        # self.checkBox = ''

    def connectSlot(self):
        self.allRadioButton.toggled.connect(self.setDisable)
        self.partRadioButton.toggled.connect(self.setEnable)

    def setDisable(self):
        self.lowSpinBox.setEnabled(False)
        self.upperSpinBox.setEnabled(False)
    def setEnable(self):
        self.lowSpinBox.setEnabled(True)
        self.upperSpinBox.setEnabled(True)

    def getData(self):
        An = self.A_necessity.isChecked()
        As = self.A_suggestion.isChecked()
        Bn = self.B_necessity.isChecked()
        Bs = self.B_suggestion.isChecked()

        if self.partRadioButton.isChecked() == True:

            lower = self.lowSpinBox.value()
            upper = self.upperSpinBox.value()
            print(lower,upper)
            range = lower * 100 + upper
            return An,As,Bn,Bs,range
        return An, As, Bn, Bs, 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qcd = QuestionCheckDialog()
    qcd.show()
    sys.exit(app.exec_())