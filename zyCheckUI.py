# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zyCheckUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_zyCheckDialog(object):
    def setupUi(self, zyCheckDialog):
        zyCheckDialog.setObjectName("zyCheckDialog")
        zyCheckDialog.resize(527, 404)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(zyCheckDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(zyCheckDialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.allTownRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.allTownRadioButton.setChecked(True)
        self.allTownRadioButton.setObjectName("allTownRadioButton")
        self.verticalLayout_4.addWidget(self.allTownRadioButton)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.partTownRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.partTownRadioButton.setChecked(False)
        self.partTownRadioButton.setObjectName("partTownRadioButton")
        self.verticalLayout.addWidget(self.partTownRadioButton)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.townLowSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.townLowSpinBox.setObjectName("townLowSpinBox")
        self.horizontalLayout_5.addWidget(self.townLowSpinBox)
        self.label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.townUpperSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.townUpperSpinBox.setProperty("value", 13)
        self.townUpperSpinBox.setObjectName("townUpperSpinBox")
        self.horizontalLayout_5.addWidget(self.townUpperSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.allMonthRadioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.allMonthRadioButton.setObjectName("allMonthRadioButton")
        self.verticalLayout_5.addWidget(self.allMonthRadioButton)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.partMonthRadioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.partMonthRadioButton.setChecked(True)
        self.partMonthRadioButton.setObjectName("partMonthRadioButton")
        self.verticalLayout_3.addWidget(self.partMonthRadioButton)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.monthLowSpinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.monthLowSpinBox.setObjectName("monthLowSpinBox")
        self.horizontalLayout_4.addWidget(self.monthLowSpinBox)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.monthUpperSpinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.monthUpperSpinBox.setObjectName("monthUpperSpinBox")
        self.horizontalLayout_4.addWidget(self.monthUpperSpinBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.verticalLayout_2.addWidget(self.widget)
        self.groupBox_3 = QtWidgets.QGroupBox(zyCheckDialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.zy_necessity = QtWidgets.QRadioButton(self.groupBox_3)
        self.zy_necessity.setChecked(True)
        self.zy_necessity.setObjectName("zy_necessity")
        self.horizontalLayout_2.addWidget(self.zy_necessity)
        self.zy_suggestion = QtWidgets.QRadioButton(self.groupBox_3)
        self.zy_suggestion.setObjectName("zy_suggestion")
        self.horizontalLayout_2.addWidget(self.zy_suggestion)
        self.zy_addition = QtWidgets.QRadioButton(self.groupBox_3)
        self.zy_addition.setObjectName("zy_addition")
        self.horizontalLayout_2.addWidget(self.zy_addition)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.widget_2 = QtWidgets.QWidget(zyCheckDialog)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.dirlineEdit = QtWidgets.QLineEdit(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dirlineEdit.sizePolicy().hasHeightForWidth())
        self.dirlineEdit.setSizePolicy(sizePolicy)
        self.dirlineEdit.setObjectName("dirlineEdit")
        self.horizontalLayout_6.addWidget(self.dirlineEdit)
        self.selectPathButton = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectPathButton.sizePolicy().hasHeightForWidth())
        self.selectPathButton.setSizePolicy(sizePolicy)
        self.selectPathButton.setObjectName("selectPathButton")
        self.horizontalLayout_6.addWidget(self.selectPathButton)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(zyCheckDialog)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(self.buttonBox.Ok).setText("开始审核")
        self.buttonBox.button(self.buttonBox.Cancel).setText("取消")
        self.horizontalLayout_7.addWidget(self.buttonBox)
        self.verticalLayout_2.addWidget(self.widget_3)

        self.retranslateUi(zyCheckDialog)
        self.buttonBox.accepted.connect(zyCheckDialog.accept)
        self.buttonBox.rejected.connect(zyCheckDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(zyCheckDialog)

    def retranslateUi(self, zyCheckDialog):
        _translate = QtCore.QCoreApplication.translate
        zyCheckDialog.setWindowTitle(_translate("zyCheckDialog", "审核账页"))
        self.groupBox.setTitle(_translate("zyCheckDialog", "小区范围"))
        self.allTownRadioButton.setText(_translate("zyCheckDialog", "全部"))
        self.partTownRadioButton.setText(_translate("zyCheckDialog", "指定样本"))
        self.label.setText(_translate("zyCheckDialog", "到"))
        self.groupBox_2.setTitle(_translate("zyCheckDialog", "审核对象"))
        self.allMonthRadioButton.setText(_translate("zyCheckDialog", "归并账页"))
        self.partMonthRadioButton.setText(_translate("zyCheckDialog", "分月账页"))
        self.label_2.setText(_translate("zyCheckDialog", "到"))
        self.groupBox_3.setTitle(_translate("zyCheckDialog", "审核方式"))
        self.zy_necessity.setText(_translate("zyCheckDialog", "必要性审核"))
        self.zy_suggestion.setText(_translate("zyCheckDialog", "提示性审核"))
        self.zy_addition.setText(_translate("zyCheckDialog", "附加审核"))
        self.label_3.setText(_translate("zyCheckDialog", "输出路径："))
        self.selectPathButton.setText(_translate("zyCheckDialog", "浏览"))

