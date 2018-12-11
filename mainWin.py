# coding:utf-8
# 界面的逻辑功能函数
# import sys
import os
# sys.path.append(r'..\.')
import pandas as pd
# import json
# import traceback

from mainWinUI import Ui_MainWindow

import myLogging as mylogger

from PyQt5.QtWidgets import QFileDialog,QTableWidgetItem,QMainWindow
# from PyQt5.QtCore import Qt
from PyQt5.Qt import QHeaderView


import cgitb
cgitb.enable( format = 'text',logdir=mylogger.err_path)

# Ui_MainWindow
class MyMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MyMainWindow,self).__init__(parent)
        # self.logger = myLogging()
        mylogger.logger.debug('mainWin>init..')
        self.setupUi(self)
        self.initUI()

        self.deal_taizhang =  ''    # deal_taizhang()
        self.fileList = {}
        # self.townList = ''
        self.workPath = os.getcwd()
        self.A = ''
        self.A_flag = False
        self.B = ''
        self.B_flag = False
        self.xiaoqu = ''
        self.xiaoqu_flag = False
        self.zhuzhai = ''
        self.zhuzhai_flag = False
        self.zhuhu = ''
        self.zhuhu_flag = False
        self.zy = ''
        self.zy_flag = False

        self.tz = ''
        self.tz_flag = False
        self.townTable = ''

        self.location = ''

        self.page_break_row = []

        #A、B、D审核结果输出表的表头
        self.A_table_head = {'year':[],'sid':[],'scode':[],'name':[],'code':[],'提示内容':[],'townname':[],'vname':[]}
        self.An_check_result = pd.DataFrame(self.A_table_head)
        self.An_check_result = self.An_check_result[['year','sid', 'scode', 'name', 'code', '提示内容', 'townname', 'vname']]
        self.As_check_result = pd.DataFrame(self.A_table_head)
        self.As_check_result = self.As_check_result[['year', 'sid', 'scode', 'name', 'code', '提示内容', 'townname', 'vname']]

        self.B_table_head = {'year':[], 'sid': [], 'scode': [], 'code': [], '提示内容': [], 'townname': [], 'vname': []}
        self.Bn_check_result = pd.DataFrame(self.B_table_head)
        self.Bn_check_result = self.Bn_check_result[['year', 'sid', 'scode', 'code', '提示内容', 'townname', 'vname']]
        self.Bs_check_result = pd.DataFrame(self.B_table_head)
        self.Bs_check_result = self.Bs_check_result[['year', 'sid', 'scode', 'code', '提示内容', 'townname', 'vname']]

        self.zy_table_head = {'year': [], 'task': [], 'month': [], 'scode': [], 'sid': [], 'person': [], 'name': [], 'code': [],'核实内容': [], 'townname': [], 'vname': []}
        self.zs_check_result = pd.DataFrame(self.zy_table_head)
        self.zs_check_result = self.zs_check_result[['year', 'month', 'task', 'scode', 'sid', 'person', 'name', 'code', '核实内容', 'townname', 'vname']]

        self.zn_check_result = pd.DataFrame(self.zy_table_head)
        self.zn_check_result = self.zn_check_result[['year', 'month', 'task', 'scode', 'sid', 'person', 'name', 'code', '核实内容', 'townname', 'vname']]

        self.now_show_table = ''
        # self.openTownList()
        self.connectSlot()
        mylogger.logger.debug('mainWin>init ok')


    # 重新设置UI界面
    def initUI(self):
        self.splitter.setStretchFactor(1,3)
        self.splitter_2.setStretchFactor(0,1)
        # self.tableData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableData.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # self.setWindowFlags(Qt.FramelessWindowHint)

    # 为组件绑定事件
    def connectSlot(self):
        # self.actionimportFile = QtWidgets.QAction("导入文件", self, triggered=self.openFile)
        self.actionimportFile.triggered.connect(self.showInTable)
        self.actionworkspace.triggered.connect(self.selectWorkDirecory)
        self.actionIntroduce.triggered.connect(self.helpText)


        self.open_tableA.clicked.connect(self.setTableA)
        self.open_zy.clicked.connect(self.setZy)
        self.xz_comboBox.currentIndexChanged.connect(self.townSelectChange)
        self.generateTz.clicked.connect(self.genTz)
        self.import_townList.clicked.connect(self.openTownList)
        self.export_taizhang.clicked.connect(self.save_to_csv)

        # self.importTable.clicked.connect(self.importTableFiles)
        self.importTable.clicked.connect(self.openImportFileDialog)
        self.questionCheck.clicked.connect(self.openQuestionCheckDialog)
        self.zyCheck.clicked.connect(self.openzyCheckDialog)
        self.file_list.itemClicked.connect(self.listSelection)

        self.searchButton.clicked.connect(self.search)

    def selectWorkDirecory(self):
        self.workPath = QFileDialog.getExistingDirectory(self,"选择工作目录",os.getcwd())

    def helpText(self):
        mylogger.logger.debug("help")
        with open("使用帮助.txt","r",encoding="utf-8") as f:
            # print("open")
            txt = f.read()
            # print("txt",txt)
            self.textEdit.setText(txt)
        # print("打开使用帮助")
        self.statusbar.showMessage("打开使用帮助",3000)

    def showMaximized(self):
        desktop = QApplication.desktop()
        rect = desktop.availableGeometry()
        self.setGeometry(rect)
        # self.show()

    def search(self):
        sid = self.searchlineEdit.text()
        if sid == "":
            self.statusbar.showMessage("请在输入框中填入要搜索户的SID")
        else:
            if self.A_flag == False:
                self.statusbar.showMessage("请先导入A表")
            else:
                family = self.A[self.A["SID"] == sid]
                if family.empty == False:
                    # 按照人码进行排序
                    family = family.sort_values(by='A100')
                    family.fillna('')
                    # print(family)
                    res = self.setFamily(family)
                    self.showData(res)
                    self.statusbar.showMessage("查找成功",3000)
                else:
                    self.statusbar.showMessage("A表中无此户数据")

    def setFamily(self,family):
        zhibiao_arr = ["成员编码","姓名","本期住户成员变动情况","与本户户主的关系","性别","出生年月","民族","户口登记地","户口性质","健康状况","参加何种医疗保险","是否在校学生","受教育程度","婚姻状况","是否持证残疾人","在本住宅居住时间","是否每月到其他住宅居住","是否每月到本住宅居住一天以上","是否打算居住本宅超过一个半月","是否常住人口", "成员编码","是否离退休人员","参加何种养老保险","是否丧失劳动能力","是否从业过","主要就业状况","主要行业","主要职业","工作总时间","工作地点","最远去哪里工作或学习(上大学)过","您认为自己主要属于下列哪个群体","您认为自己还属于下列哪个群体","您拥有的与当前职业相关的最高技能等级证书或职业技能证书","您拥有的与当前职业相关的最高技术职称"]
        code_arr = ["A100","A101","A102","A103","A104","A105","A107","A108","A109","A110","A111","A112","A113","A114","A120","A115","A116","A117","A118","A119", "A200","A201","A202","A203","A204","A205","A206","A207","A208","A209","A210","A211","A212","A213","A214"]
        index_arr = ['一', '二', '三', '四', '五', '六', '七', '八','九']
        data = {'指标': [], '编码': [], '一': [], '二': [], '三': [], '四': [], '五': [], '六': [], '七': [], '八': [],'九': []}
        result = pd.DataFrame(data)
        result = result[['指标', '编码', '一', '二', '三', '四', '五', '六', '七', '八','九']]
        # 一户总人数
        rowCount = family.iloc[:, 0].size
        for (zhibiao, code) in zip(zhibiao_arr, code_arr):
            dict = {"指标":zhibiao,"编码":code}
            code_data = family[code]
            # print("code_data",code_data,type(code_data))
            for i in range(rowCount):
                key = index_arr[i]
                # print(key,code_data.values[i])
                dict[key] = code_data.values[i]
            result = result.append(dict, ignore_index=True)
        return result

    # list点击触发事件
    def listSelection(self,index):
        try:
            tb = self.fileList[index.text()]
            if tb.empty == False:
                self.now_show_table = tb
                # print(tb)
                self.statusbar.showMessage("正在切换至表" + index.text() + ",请稍等...")
                self.showData(tb)
                self.statusbar.showMessage("切换成功",3000)

            else:
                self.statusbar.showMessage(index.text() + "为空？请确认")
        except Exception as e:
            self.statusbar.showMessage("程序异常，请重新操作")

    # 向列表中添加项
    def addToList(self,key,value):
        self.file_list.addItem(key)
        self.fileList[key] = value
    # 文件List选择
    def listSelect(self,item):
        if item.text() == "A表":
            self.showData(self.A)
        if item.text() == "B表":
            self.showData(self.B)
        if item.text() == "住宅名录":
            self.showData(self.zhuzhai)
        if item.text() == "小区名录":
            self.showData(self.xiaoqu)
        if item.text() == "住户名录":
            self.showData(self.zhuhu)
        if item.text() == "账页表":
            self.showData(self.zy)
        if item.text() == "台账结果":
            self.showData(self.now_show_table)

    # 打开csv文件 返回DataFrame对象
    def read_csv(self,path):
        with open(path, 'r') as f:
            mylogger.logger.debug('mainWin>openFile:' + path)
            file = pd.read_csv(f, header=0,low_memory=False)
        return file

    #导入相关文件
    def importTableFiles(self):
        if self.A_flag == False:
            self.A,self.A_flag = self.openFile("请导入A表")
            # if self.A_flag == True:
            #     self.file_list.addItem("A表")
            #     self.fileList.append(self.A)
        if self.B_flag == False:
            self.B,self.B_flag = self.openFile("请导入B表")
            # if self.B_flag == True:
            #     self.file_list.addItem("B表")
            #     self.fileList.append(self.B)

        if self.zhuzhai_flag == False:
            self.zhuzhai,self.zhuzhai_flag = self.openFile("请导入住宅名录")
            # if self.zhuzhai_flag == True:
            #     self.file_list.addItem("住宅名录")
            #     self.fileList.append(self.zhuzhai)

        if self.xiaoqu_flag == False:
            self.xiaoqu,self.xiaoqu_flag = self.openFile("请导入小区名录")
            # if self.xiaoqu_flag == True:
            #     self.file_list.addItem("小区名录")
            #     self.fileList.append(self.xiaoqu)

        if self.zhuhu_flag == False:
            self.zhuhu,self.zhuhu_flag = self.openFile("请导入住户名录")
            # if self.zhuhu_flag == True:
            #     self.file_list.addItem("住户名录")
            #     self.fileList.append(self.zhuhu)

        if self.zy_flag == False:
            self.zy,self.zy_flag = self.openFile("请导入账页数据")
            col = self.colUpper(self.zy.columns.values.tolist())
            self.zy = self.zy.rename(columns=col)
            # print(self.zy)
            # if self.zy_flag == True:
            #     self.file_list.addItem("账页表")
            #     self.fileList.append(self.zy)


    # 打开审核问卷对话框
    def openQuestionCheckDialog(self):
        from A_necessity_check import A_necessity_check
        from A_suggestion_check import A_suggestion_check
        from B_necessity_check import B_necessity_check
        from B_suggestion_check import B_suggestion_check
        from questionCheckDialog import QuestionCheckDialog
        qcd = QuestionCheckDialog(self)
        result = qcd.exec_()
        An, As, Bn, Bs, range = qcd.getData()

        if An == True or As == True:
            if self.A_flag == True and self.xiaoqu_flag == True:
                if An == True and self.zhuhu_flag == True:
                    An_outcome = A_necessity_check(self.A,self.zhuhu,self.xiaoqu,self.An_check_result)
                    # print(type(An_outcome))
                    Anfilename = 'A_necessity_result.xlsx'
                    An_outcome.to_excel('./A_necessity_result.xlsx',encoding="utf-8",index=False,sheet_name='Sheet')
                    self.addToList(Anfilename,An_outcome)
                    self.showData(An_outcome,100)

                if As == True:
                    As_outcome = A_suggestion_check(self.A,self.xiaoqu,self.As_check_result)
                    Asfilename = 'A_suggestion_result.xlsx'
                    As_outcome.to_excel('./A_suggestion_result.xlsx', encoding="utf-8", index=False,sheet_name='Sheet')
                    self.addToList(Asfilename, As_outcome)
                    self.showData(As_outcome, 100)

            else:
                if self.A_flag == False:
                    self.statusbar.showMessage("请先导入A表")
                if self.xiaoqu_flag == False:
                    self.statusbar.showMessage("请先导入小区表")
                if self.zhuhu_flag == False and An == True:
                    self.statusbar.showMessage("请先导入住户表")

        if Bn == True or Bs == True:
            if self.B_flag == True and self.zhuhu_flag == True and self.zhuzhai_flag == True and self.xiaoqu_flag == True:
                if Bn == True:
                    Bn_outcome = B_necessity_check(self.B,self.zhuhu,self.zhuzhai,self.xiaoqu,self.Bn_check_result)
                    Bnfilename = 'B_necessity_result.xlsx'
                    Bn_outcome.to_excel('./B_necessity_result.xlsx',encoding="utf-8",index=False,sheet_name='Sheet')
                    self.addToList(Bnfilename,Bn_outcome)
                    self.showData(Bn_outcome,100)
                if Bs == True:
                    Bs_outcome = B_suggestion_check(self.B, self.zhuhu, self.zhuzhai, self.xiaoqu,self.Bs_check_result)
                    Bsfilename = 'B_suggestion_result.xlsx'
                    Bs_outcome.to_excel('./B_suggestion_result.xlsx', encoding="utf-8", index=False,sheet_name='Sheet')
                    self.addToList(Bsfilename, Bs_outcome)
                    self.showData(Bs_outcome, 100)
            else:
                if self.B_flag == False:
                    self.statusbar.showMessage("请先导入B表")
                if self.zhuhu_flag == False:
                    self.statusbar.showMessage("请先导入住户表")
                if self.zhuzhai_flag == False:
                    self.statusbar.showMessage("请先导入住宅表")
                if self.xiaoqu_flag == False:
                    self.statusbar.showMessage("请先导入小区表")

        # print(An,As,Bn,Bs,range)
        # print("result:",result)
        # qcd.show()

    # 打开导入相关文件对话框
    def openImportFileDialog(self):
        from importFileDialog import importFileDialog
        importFile = importFileDialog(self,self.workPath)
        result = importFile.exec_()
        res_path = importFile.getPath()
        info = "打开"
        # print(res_path)
        if res_path["A"] != "":
            info += "A,"
            self.A,self.A_flag = self.openFileByPath(res_path["A"])

        if res_path["B"] != "":
            self.B, self.B_flag = self.openFileByPath(res_path["B"])
            info += "B,"

        if res_path["住户"] != "":
            self.zhuhu, self.zhuhu_flag = self.openFileByPath(res_path["住户"])
            info += "住户,"

        if res_path["住宅"] != "":
            self.zhuzhai, self.zhuzhai_flag = self.openFileByPath(res_path["住宅"])
            info += "住宅,"

        if res_path["小区"] != "":
            self.xiaoqu, self.xiaoqu_flag = self.openFileByPath(res_path["小区"])
            info += "住宅,"
        if res_path["账页表"] != "":
            self.zy, self.zy_flag = self.openFileByPath(res_path["账页表"])
            info += "账页表,"
        info += "成功"
        if info == "打开成功":
            self.statusbar.showMessage("未选择打开新文件")
        else:
            self.statusbar.showMessage(info)

    # 打开审核账页对话框
    def openzyCheckDialog(self):
        from zyCheckDialog import zyCheckDialog
        from zy_check_necessity import zy_check_necessity
        from zy_check_suggestion import zy_check_suggestion
        zcd = zyCheckDialog(self)
        result = zcd.exec_()
        Zn,Zs,Za,townRange,monthRange,directory = zcd.getData()
        if Zs == True or Zn == True or Za == True:
            if self.zy_flag == True and self.A_flag == True and self.B_flag == True and self.zhuhu_flag == True and \
               self.zhuzhai_flag == True and self.zhuhu_flag == True and self.xiaoqu_flag == True:
                if Zs == True:
                    Zs_outcome = zy_check_suggestion(self.A,self.B,self.zy,self.zhuzhai,self.zhuhu,self.xiaoqu,self.zs_check_result)
                    Zsfilename = 'zy_suggestion_result.xlsx'
                    Zs_outcome.to_excel(directory+'/'+Zsfilename, encoding="utf-8", index=False,sheet_name='Sheet')
                    self.addToList(Zsfilename, Zs_outcome)
                    self.showData(Zs_outcome, 100)
                if Zn == True:
                    Zn_outcome = zy_check_necessity(self.A,self.B,self.zy,self.zhuzhai,self.zhuhu,self.xiaoqu,self.zn_check_result)
                    Znfilename = 'zy_necessity_result.xlsx'
                    Zn_outcome.to_excel(directory+'/'+Znfilename, encoding="utf-8", index=False,sheet_name='Sheet')
                    self.addToList(Znfilename, Zn_outcome)
                    self.showData(Zn_outcome, 100)

            else:
                if self.zy_flag == False:
                    self.statusbar.showMessage("请先导入账页表")
                if self.A_flag == False:
                    self.statusbar.showMessage("请先导入A表")
                if self.B_flag == False:
                    self.statusbar.showMessage("请先导入B表")
                if self.zhuhu_flag == False:
                    self.statusbar.showMessage("请先导入住户表")
                if self.zhuzhai_flag == False:
                    self.statusbar.showMessage("请先导入住宅表")
                if self.xiaoqu_flag == False:
                    self.statusbar.showMessage("请先导入小区表")

    def openFileByPath(self,filePath):
        try:
            mylogger.logger.debug("mainWin>function:openFile:try")
            df = self.read_csv(filePath)
            filepath, name = os.path.split(filePath)
            self.addToList(name, df)
            col = self.colUpper(df.columns.values.tolist())
            df = df.rename(columns=col)
            return df, True
        except Exception as e:
            mylogger.logger.error("openFileByPath() exception")
            mylogger.logger.error(e)
            # print("openFile Error",e)
            return '', False
    # 将所有列名换成大写
    def colUpper(self,col):
        dict = {}
        for key in col:
            value = key.upper()
            # print(value)
            dict[key] = value
        return dict

    # 打开文件
    # 输入：打开文件的提示信息
    # 返回值：
    #   若选中文件，返回：已打开文件的pandas对象，是否打开文件标志位-True
    #   未选中文件，返回：空，False
    def openFile(self,tip="选取文件"):
        # print("openFile")
        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                                          tip,
                                                          self.workPath,
                                                          "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔

        # print("filename>",fileName1,"<",type(fileName1),"len:",fileName1)
        mylogger.logger.debug("mainWin>function:openFile:%s"%fileName1)
        # 若没有选中文件
        if fileName1.strip() != "":
            # print(fileName1, filetype)

            try:
                # print("try")
                mylogger.logger.debug("mainWin>function:openFile:try")
                df = self.read_csv(fileName1)

                # fileName = fileName1.split("/")[-1]
                filpath,name = os.path.split(fileName1)
                # print(fileName,name)
                self.addToList(name,df)
                col = self.colUpper(df.columns.values.tolist())
                df = df.rename(columns=col)
                return df,True
            except Exception as e:
                mylogger.logger.error("mainWin>function:openFile:exception")
                mylogger.logger.error(e)
                # print("openFile Error",e)
                return '',False
        else:
            self.statusbar.showMessage("未选择文件",3000)
            return '',False

    # 导入小区名录时触发
    def openTownList(self):
        # file_path = "D:/Document/Code/Python/AuditingApp/src/输入文件夹/小区名录310151.18.csv"
        # self.read_csv(file_path)
        self.townTable,flag = self.openFile("请导入小区名录")
        mylogger.logger.debug("openTownList openFile")
        if flag == False:
            mylogger.logger.debug("openTownList 未选中文件")
        else:
            mylogger.logger.debug("in openTownList else")
            # try:
            if self.townTable["TOWNNAME"].values[0].strip() == "乡镇名称":
                self.townTable = self.townTable.drop(0)
            # townList = self.townTable["townName"].drop_duplicates()
            townList = ["所有乡镇"]
            arr = list(self.townTable["TOWNNAME"].drop_duplicates())
            for i in arr:
                townList.append(i)
            self.xz_comboBox.clear()
            self.xz_comboBox.addItems(townList)
            # communityList = ["所有居委会"]
            # self.xq_comboBox.clear()
            # self.xq_comboBox.addItems(communityList)
            self.townSelectChange()
            # print("townList:",townList)
            mylogger.logger.debug('mainWin>function:openTownList')
            self.statusbar.showMessage("打开文件成功",5000)
            # except Exception as e:
            #     print(e)
            #     mylogger.logger.debug('mainWin>function:openTownList exception')
            #     self.statusbar.showMessage("打开的文件有误，请重新选择文件",5000)

    # 选取生成台账的小区触发函数
    def townSelectChange(self):
        mylogger.logger.debug("in townSelectChange")
        town = self.xz_comboBox.currentText()
        if town == "所有乡镇":
            communityList = ["所有居委会"]
            self.xq_comboBox.clear()
            self.xq_comboBox.addItems(communityList)
        else:
            # community = self.townTable[self.townTable["townName"] == town]

            community = self.townTable[self.townTable["TOWNNAME"] == town]
            # communityList = community["vName"].drop_duplicates()
            communityList = ["所有居委会"]
            arr = list(community["VNAME"].drop_duplicates())
            for i in arr:
                communityList.append(i)
            self.xq_comboBox.clear()
            self.xq_comboBox.addItems(communityList)

    def getCommunityCode(self):
        townName = self.xz_comboBox.currentText()
        communityName = self.xq_comboBox.currentText()
        code = str(self.townTable["VID"].values[0])

        if townName == "所有乡镇":
            # 310151101027001
            # 151101101214001
            communityCode = code[0:3]
            # self.location = townName
        else:
            code = str(self.townTable[self.townTable["TOWNNAME"] == townName]["VID"].values[0])
            if communityName == "所有居委会":
                if code[3:6] == code[6:9]:
                    communityCode = code[0:6]
                else:
                    communityCode = code[0:9]
            else:
                # communityList = self.townTable[self.townTable["vName"] == communityName]
                communityList = self.townTable[self.townTable["VNAME"] == communityName]
                # communityCode = str(communityList["vID"].values[0])
                communityCode = str(communityList["VID"].values[0])
                mylogger.logger.debug('mainWin>function:getCommunityCode')
        self.location = townName + communityName
        # location = townName + " " + communityName
        return communityCode

    def setTableA(self):
        # print('setA')
        mylogger.logger.debug('mainWin>function:setTableA')
        self.A,self.A_flag = self.openFile("请导入A表")

    def setZy(self):
        # print('setzy')
        mylogger.logger.debug('mainWin>function:setTableZy')
        self.zy,self.zy_flag = self.openFile("请导入账页表")

    def genTz(self):
        try:
            from deal_taizhang import deal_taizhang
            self.deal_taizhang = deal_taizhang()
            if self.xq_comboBox.currentText() == '':
                self.statusbar.showMessage("请先导入小区名录")
            else:
                if self.A_flag == False or self.zy_flag == False:
                    # print("请先导入A表与账页表")
                    self.statusbar.showMessage("请先导入A表与账页表")
                else:
                    # print('生成台账')
                    self.statusbar.showMessage("生成台账中...")
                    communityCode = self.getCommunityCode()
                    # print("communityCode:",communityCode)
                    # print("mainWin type:", type(communityCode))
                    self.now_show_table = self.deal_taizhang.getCommunity(communityCode,self.townTable,self.A,self.zy)
                    if self.now_show_table.empty == False:
                        # if self.tz_flag == False:
                        key = self.location + "台账"
                        self.addToList(key,self.now_show_table)
                        self.statusbar.showMessage("生成台账成功")
                        mylogger.logger.debug("获取到生成台账结果")
                        # self.clearTable()
                        self.showData(self.now_show_table,False)
                        # deal_taizhang.spliteFamily(self.A,self.zy)
                    else:
                        self.statusbar.showMessage("生成台账无数据，请确认是否正确选择对应乡镇")
        except Exception as e:
            # print(e)
            mylogger.logger.error(e)
            self.statusbar.showMessage("生成台账出错，请检查使用数据是否正确")

    def showInTable(self):
        self.statusbar.showMessage("正在打开文件")
        df,flag = self.openFile()
        # print(pd.isnull(df))
        if flag == False:
            print("空文件")
            self.statusbar.showMessage("空文件")

        else:
            self.statusbar.showMessage("获取数据中，请稍等")
            print('getData')
            # 获取表头
            df = df.fillna('')
            header = df.columns.values.tolist()  # [str(col) for col in df]
            # 获取表的行列数
            colCount = df.columns.size
            rowCount = df.iloc[:, 0].size
            # 设置表行数
            self.tableData.setRowCount(rowCount)
            # 设置表列数
            self.tableData.setColumnCount(colCount)
            self.tableData.clear()
            # 重新设置表头
            self.tableData.setHorizontalHeaderLabels(header)
            for r in range(rowCount):
                for c in range(colCount):
                    item = df.iat[r, c]
                    self.tableData.setItem(r, c, QTableWidgetItem(str(item)))
            self.statusbar.showMessage("打开文件成功")

    def clearTable(self):
        self.tableData.clear()
        rowCount = self.tableData.rowCount()
        # print(rowCount)
        for row in range(0,rowCount):
            self.tableData.removeRow(row)

    def showData(self,df,max=True):
        df = df.fillna('')
        mylogger.logger.debug("将结果显示在表上")
        header = df.columns.values.tolist()  # [str(col) for col in df]
        # 获取表的行列数
        colCount = df.columns.size
        rowCount = df.iloc[:, 0].size
        if max == True:
            if rowCount > 100:rowCount = 100
        # 设置表行数
        self.tableData.setRowCount(rowCount)
        # 设置表列数
        self.tableData.setColumnCount(colCount)
        self.tableData.clear()
        # 重新设置表头
        self.tableData.setHorizontalHeaderLabels(header)
        for r in range(0,rowCount):
            for c in range(colCount):
                item = df.iat[r, c]
                self.tableData.setItem(r, c, QTableWidgetItem(str(item)))

    def save_to_csv(self):
        try:
            from page_break_print import page_break_print
            path = './' + self.location + '台账结果.xlsx'
            self.now_show_table.to_excel(path,encoding="utf-8",index=False,sheet_name='Sheet')
            self.statusbar.showMessage("正在添加分页符...")
            page_break_print(path)
            self.statusbar.showMessage("生成文件" + path + "成功")

            # self.now_show_table.to_csv("台账结果.csv",encoding="utf-8",index=False)
            mylogger.logger.debug("生成台账结果成功")
        except Exception as e:
            self.statusbar.showMessage("生成台账出错，请检查操作步骤是否正确？")


    def saveFile(self):
        filename = QFileDialog.getSaveFileName(self, 'save file', '/home/jm/study')
        with open(filename[0], 'w') as f:
            my_text = self.textEdit.toPlainText()
            f.write(my_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywin = MyMainWindow()
    mywin.show()
    sys.exit(app.exec_())