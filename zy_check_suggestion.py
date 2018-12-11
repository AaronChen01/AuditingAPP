import pandas as pd
import re
import datetime
from decimal import Decimal
import myLogging as mylogger

zy_suggestion_result = pd.DataFrame()

def spliteFamily(table):
    sid_array = table["SID"].drop_duplicates()
    for sid_index in sid_array:
        # 获取相同sid的行即为同一户的成员
        hu_data = table[table["SID"] == sid_index]
        # 按照人码进行排序
        hu_data = hu_data.sort_values(by='CODE')
        yield hu_data


def Table(table, code):
    t = table[code]
    # print("tabledata:",t)
    if t.empty == False:
        if pd.isnull(t.values[0]) == True:
            return 0
        if type(t.values[0]) == type("str"):
            # print("字符串类型：",type(t.values[0]))
            return int(t.values[0])
        return t.values[0]
    else:
        return 0

# 获取某个编码的金额 2
def moneySum(zy,code):
    pattern = code + "(.*)"
    code = [x for x in zy['CODE'] if re.match(pattern, x)]
    if len(code) != 0:
        code = set(code)
        code = list(code)
        code.sort()
        frames = []
        for index in code:
            df = zy[zy['CODE'] == index]
            frames.append(df)
        if len(frames) != 0:
            result = pd.concat(frames)
            return sum(result['MONEY'].apply(Decimal))
            # return Decimal(str(sum(result['MONEY'].apply(Decimal))))
    return 0

# 获取某个编码的数量 AMOUNT 1
def amountSum(zy,code,person=0):
    # if person != 0:
    #     zy = zy[zy["PERSON"] == person]
    pattern = code + "(.*)"
    code = [x for x in zy["CODE"] if re.match(pattern, x)]
    if len(code) != 0:
        code = set(code)
        code = list(code)
        code.sort()
        frames = []
        for index in code:
            df = zy[zy["CODE"] == index]
            frames.append(df)
        if len(frames) != 0:
            result = pd.concat(frames)
            # print(result["CODE"],result["MONEY"])
            return sum(result["AMOUNT"].apply(Decimal))
    # print("无此记录")
    return 0


def insert_to_pd(data):
    global zy_suggestion_result
    zy_suggestion_result = zy_suggestion_result.append(data, ignore_index=True)

def zy_check_suggestion(TableA,TableB,zy,zhuzhai,zhuhu,xiaoqu,result):
    mylogger.logger.debug("zy_check_suggestion init..")
    begin = datetime.datetime.now()
    if zy['COUN'].values[0].strip() == "县码":
        zy = zy.drop(0)
    if zhuzhai['COUN'].values[0].strip() == "县区代码":
        zhuzhai = zhuzhai.drop(0)
    if zhuhu['COUN'].values[0].strip() == "县区代码":
        zhuhu = zhuhu.drop(0)

    global zy_suggestion_result
    zy_suggestion_result.drop(zy_suggestion_result.index,inplace=True)
    zy_suggestion_result = result

    zy = zy.sort_values(by='SID')
    zy_families = spliteFamily(zy)
    for zy_family in zy_families:
        family_sid = zy_family['SID'].values[0]
        # family_sid = Table(zy_family,'SID')
        HID = family_sid[0:19]
        A = TableA[TableA['SID'] == family_sid]
        if A.empty == True:
            # print(family_sid+"A表中无此户")
            continue

        one_zhuhu = zhuhu[zhuhu['HHID'] == family_sid]
        one_zhuzhai = zhuzhai[zhuzhai['HID'] == HID]
        B = TableB[TableB['SID'] == family_sid]
        qu_vid = family_sid[0:15]
        # print(qu_vid)
        qu = xiaoqu[xiaoqu['VID'] == qu_vid]
        # print(xiaoqu)
        townname = qu['TOWNNAME'].values[0]
        vname = qu['VNAME'].values[0]
        # print(townname)
        ChangeH = 0
        # surveyType = int(one_zhuhu['SURVEYTYPE'].values[0])
        surveyType = Table(one_zhuhu,"SURVEYTYPE")
        Year = Table(zy_family, 'YEAR')
        Month = Table(zy_family, 'MONTH')
        TaskCode = Table(B,'TASK')
        task = TaskCode
        scode = zy_family['SCODE'].values[0]
        # print(scode)
        openYear = Table(one_zhuhu, 'OPENYEAR')

        dict = {'year': str(Year), 'month': str(Month), 'task': str(task), 'scode': scode, 'sid': family_sid,'person':str(99),\
                'townname':townname,'vname':vname}

        if pd.isnull(openYear) == False:
            # openYear = int(one_zhuhu["OPENYEAR"].values[0])
            openMonth = Table(one_zhuhu, "OPENMONTH")  # int(one_zhuhu["OPENMONTH"].values[0])
        # 计算该用户是否报告期内新进住宅
        if TaskCode <= 4:
            lenM = 3
            if openYear == Year and openMonth <= Month and openMonth > Month - 2:
                ChangeH = 1
        else:
            lenM = Month + 1
            if openYear == Year and openMonth <= Month:
                ChangeH = 1
        # print(TaskCode,Table(A, 'A102'),Table(one_zhuzhai,"M105"),surveyType,family_sid,Table(A, "A206"), Table(A, "A205"),moneySum(zy_family,"22"))
        if (TaskCode >= 1 and TaskCode <= 7) and Table(A, 'A102') != 3 and Table(one_zhuzhai,"M105") == 1 and surveyType != 2:
            # print(family_sid)
            #收入成本相关
            # print(family_sid,Table(B,'B126'),Table(B,'B139'),moneySum(zy_family,"560611"),moneySum(zy_family,"521111"))
            sum1 = moneySum(zy_family,"560611")
            sum2 = moneySum(zy_family,"521111")
            if Table(B,'B126') != 1 and Table(B,'B139') == 0 and sum1+sum2 > 0:
                value = "B126={},B139={},'560611'={},'521111'={}".format(Table(B,'B126'),Table(B,'B139'),sum1,sum2)
                dict['code'] = value
                dict['核实内容'] = "有住房还贷支出或利息支出 ,本宅B表无还贷情况且期内没有新购住房(B126,b139)，核实是否1年前贷款购买本宅外住房"
                insert_to_pd(dict)

            b1 = Table(B,"B128")
            b2 = Table(B,"B131")
            if b1 + b2 > 0 and moneySum(zy_family,"230511") == 0:
                value = "B128={},B131={},'230511'={}".format(b1,b2,moneySum(zy_family,"230511"))
                dict['code'] = value
                dict['核实内容'] = "b表有房屋出租信息(b128,b131),但没有租金收入"
                insert_to_pd(dict)
                # print("b表有房屋出租信息(b128,b131),但没有租金收入")

            # 消费相关
            if surveyType == 1:
                if amountSum(zy_family,"311015") > lenM * 300:
                    value = "code=311015,amount={}".format(amountSum(zy_family,"311015"))
                    dict['code'] = value
                    dict['核实内容'] = "有可能将玉米作为饲料编入食品消费中,请核实是否编码错误！"
                    insert_to_pd(dict)
                    # print("有可能将玉米作为饲料编入食品消费中,请核实是否编码错误！")
                if amountSum(zy_family, "31102") > lenM * 200:
                    value = "code=31102,amount={}".format(amountSum(zy_family, "31102"))
                    dict['code'] = value
                    dict['核实内容'] = "有可能将薯类作为饲料编入食品消费中,请核实是否编码错误"
                    insert_to_pd(dict)
                    # print("有可能将薯类作为饲料编入食品消费中,请核实是否编码错误")
                if amountSum(zy_family, "311031") > lenM * 50:
                    value = "code=311031,amount={}".format(amountSum(zy_family, "311031"))
                    dict['code'] = value
                    dict['核实内容'] = "有可能将大豆作为豆制品编入食品消费中,请核实是否编码错误"
                    insert_to_pd(dict)
                    # print("有可能将大豆作为豆制品编入食品消费中,请核实是否编码错误")
                if amountSum(zy_family, "31104") > lenM * 100:
                    value = "code=31104,amount={}".format(amountSum(zy_family, "31104"))
                    dict['code'] = value
                    dict['核实内容'] = "食用油消费过大,请核实是否编码错误"
                    insert_to_pd(dict)
                    # print("食用油消费过大,请核实是否编码错误")
                if amountSum(zy_family, "31105") > lenM * 500:
                    value = "code=31105,amount={}".format(amountSum(zy_family, "31105"))
                    dict['code'] = value
                    dict['核实内容'] = "蔬菜和食用菌消费过大,请核实是否编码错误"
                    insert_to_pd(dict)
                    # print("蔬菜和食用菌消费过大,请核实是否编码错误")
                if amountSum(zy_family, "31106") > lenM * 300:
                    value = "code=31106,amount={}".format(amountSum(zy_family, "31106"))
                    dict['code'] = value
                    dict['核实内容'] = "畜肉类消费过大,有可能将宴请支出编入食品消费中,请核实是否编码错误！"
                    insert_to_pd(dict)
                    # print("畜肉类消费过大,有可能将宴请支出编入食品消费中,请核实是否编码错误！")
                if amountSum(zy_family, "31107") > lenM * 100:
                    value = "code=31107,amount={}".format(amountSum(zy_family, "31107"))
                    dict['code'] = value
                    dict['核实内容'] = "禽肉类消费过大,有可能将宴请支出编入食品消费中,请核实是否编码错误！"
                    insert_to_pd(dict)
                    # print("禽肉类消费过大,有可能将宴请支出编入食品消费中,请核实是否编码错误！")
                if amountSum(zy_family, "31108") > lenM * 100:
                    value = "code=31108,amount={}".format(amountSum(zy_family, "31108"))
                    dict['code'] = value
                    dict['核实内容'] = "水产品消费过大,有可能将宴请支出编入食品消费中,请核实是否编码错误！"
                    insert_to_pd(dict)
                    # print("水产品消费过大,有可能将宴请支出编入食品消费中,请核实是否编码错误！")
                if amountSum(zy_family, "31109") > lenM * 100:
                    value = "code=31109,amount={}".format(amountSum(zy_family, "31109"))
                    dict['code'] = value
                    dict['核实内容'] = "蛋类消费过大,有可能将宴请支出编入食品消费中,请核实是否编码错误！"
                    insert_to_pd(dict)
                    # print("蛋类消费过大,有可能将宴请支出编入食品消费中,请核实是否编码错误！")
                if amountSum(zy_family, "31110") > lenM * 300:
                    value = "code=31110,amount={}".format(amountSum(zy_family, "31110"))
                    dict['code'] = value
                    dict['核实内容'] = "奶类的消费过大,请核实！"
                    insert_to_pd(dict)
                    # print("奶类的消费过大,请核实！")
                if amountSum(zy_family, "31111") > lenM * 500:
                    value = "code=31111,amount={}".format(amountSum(zy_family, "31111"))
                    dict['code'] = value
                    dict['核实内容'] = "干鲜瓜果消费过大,有可能将宴请支出编入食品消费中,请核实是否编码错误！"
                    insert_to_pd(dict)
                    # print("干鲜瓜果消费过大,有可能将宴请支出编入食品消费中,请核实是否编码错误！")
                if amountSum(zy_family, "31112") > lenM * 150:
                    value = "code=31112,amount={}".format(amountSum(zy_family, "31112"))
                    dict['code'] = value
                    dict['核实内容'] = "糖果糕点类消费过大，有可能将宴请支出编入食品消费中,请核实是否编码错误！"
                    insert_to_pd(dict)
                    # print("糖果糕点类消费过大，有可能将宴请支出编入食品消费中,请核实是否编码错误！")
                if amountSum(zy_family, "312111") > lenM * 400:
                    value = "code=312111,amount={}".format(amountSum(zy_family, "312111"))
                    dict['code'] = value
                    dict['核实内容'] = "卷烟消费过大，有可能将宴请支出编入食品消费中,请核实是否编码错误！"
                    insert_to_pd(dict)
                    # print("卷烟消费过大，有可能将宴请支出编入食品消费中,请核实是否编码错误！")
                if amountSum(zy_family, "312211") > lenM * 150:
                    value = "code=312211,amount={}".format(amountSum(zy_family, "312211"))
                    dict['code'] = value
                    dict['核实内容'] = "啤酒消费过大，有可能将宴请支出编入食品消费中,请核实是否编码错误！"
                    insert_to_pd(dict)
                    # print("啤酒消费过大，有可能将宴请支出编入食品消费中,请核实是否编码错误！")
                if amountSum(zy_family, "312221") > lenM * 200:
                    value = "code=312221,amount={}".format(amountSum(zy_family, "312221"))
                    dict['code'] = value
                    dict['核实内容'] = "白酒消费过大，有可能将宴请支出编入食品消费中,请核实是否编码错误！"
                    insert_to_pd(dict)
                    # print("白酒消费过大，有可能将宴请支出编入食品消费中,请核实是否编码错误！")

            for row in A.iterrows():
                A_member = row[1]
                person = int(A_member['A100'])
                name = A_member['A101']
                if person > 0:
                    person_zy = zy_family[zy_family["PERSON"] == str(person)]
                    money = moneySum(person_zy,"2") - moneySum(person_zy,"240511")
                    if Table(A,"A106") < 16 and money > 0:
                        dict['person'] = str(person)
                        dict['name']= name
                        value = "A106={},'2'-'240511'={}".format(Table(A,"A106"),money)
                        dict['code'] = value
                        dict['核实内容'] = "年龄低于16岁，有工资、经营等收入，核实是否为童工？"
                        insert_to_pd(dict)
                        # print("年龄低于16岁，有工资、经营等收入，核实是否为童工？")

                    # sum1=0
                    # sum2=0
                    # sum1 = moneySum(person_zy,"22")
                    # sum2 = moneySum(person_zy,"2201") + moneySum(person_zy,"2202") + moneySum(person_zy,"2203") + \
                    #        moneySum(person_zy,"2204") + moneySum(person_zy,"2206")
                    # print(person, Table(A, "A206"), Table(A, "A205"), moneySum(zy_family,"220511"))
                    # if 5 < Table(A, "A206") < 21 and Table(A,"A205") == 7 and sum1 - sum2 == 0:
                    money = moneySum(person_zy,"220511")
                    if 5 < Table(A, "A206") < 21 and Table(A, "A205") == 7 and money == 0:
                        dict['person'] = str(person)
                        dict['name'] = name
                        value = "A206={},A205={},'220511'={}".format(Table(A, "A206"),Table(A, "A205"),money)
                        dict['code'] = value
                        dict['核实内容'] = "从事第三产业经营（a206）的就业人员（a205）无第三产业收入"
                        insert_to_pd(dict)
                        # print("从事第三产业经营（a206）的就业人员（a205）无第三产业收入")
                    # if 5 < Table(A, "A206") < 21 and Table(A,"A205") == 7 and sum1 - sum2 == 0:
                    #     print("本期内从事第三产业经营（a206）的就业人员（a205）无第三产业收入")

    return zy_suggestion_result

# 打开csv文件 返回DataFrame对象
def read_csv(path):
    with open(path, 'r') as f:
        file = pd.read_csv(f, header=0,low_memory=False)
    return file

if __name__ == '__main__':
    # A_path = u"D:/研一/项目/CheckProgram/Auditing/输入文件夹/A310151.18.csv"
    # B_path = u"D:/研一/审核程序/src/输入文件夹/B310151.18.csv"
    # zy_path = u"D:/研一/项目/CheckProgram/Auditing/输入文件夹/D310151.1806.csv"
    # global result
    A_path = u"D:\研一\项目\测试数据\国家点6月A问卷.csv"
    B_path = u"D:\研一\项目\测试数据\国家点B问卷.csv"
    zy_path = u"D:\研一\项目\测试数据\国家点12-6月账页数据.csv"

    zhuhu_path = u"D:/研一/项目/CheckProgram/Auditing/输入文件夹/住户样本310151.18.csv"
    zhuzhai_path = u"D:/研一/项目/CheckProgram/Auditing/输入文件夹/住宅名录310151.18.csv"
    xiaoqu_path = u"D:\研一\项目\CheckProgram\Auditing\输入文件夹\小区名录310151.18.csv"

    TableA = read_csv(A_path)
    TableB = read_csv(B_path)
    zy = read_csv(zy_path)
    zhuzhai = read_csv(zhuzhai_path)
    zhuhu = read_csv(zhuhu_path)
    xiaoqu = read_csv(xiaoqu_path)

    head = {'year': [], 'task': [], 'month': [], 'scode': [], 'sid': [], 'person': [], 'name': [], 'code': [],
            '核实内容': [], 'townname': [], 'vname': []}  # , 'haddr': []}
    result = pd.DataFrame(head)
    result = result[['year', 'month', 'task', 'scode', 'sid', 'person', 'name', 'code', '核实内容', 'townname', 'vname']]  # , 'haddr']]

    zy_check_suggestion(TableA,TableB,zy,zhuzhai,zhuhu,xiaoqu,result)
    # result.to_csv('zyCheckSuggestionResult.csv',encoding='utf_8_sig')
