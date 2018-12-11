import pandas as pd
import re
import datetime

def spliteFamily(table):
    sid_array = table["SID"].drop_duplicates()
    for sid_index in sid_array:
        # 获取相同sid的行即为同一户的成员
        hu_data = table[table["SID"] == sid_index]
        # 按照人码进行排序
        hu_data = hu_data.sort_values(by='CODE')
        yield hu_data

def Table(table,code):
    t = table[code]
    if t.empty == False:
        if type(t.values[0]) == type("str"):
            return int(t.values[0])
        return t.values[0]
    else:
        return 0

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
            return sum(result['MONEY'].apply(float))
    return -1.0

def judge_moneySum(x):
    if x > 0:
        return 1
    else:
        return 0

def Zy_check_addition(TableA,TableB,zy,zhuzhai,zhuhu):
    begin = datetime.datetime.now()
    zy = zy.drop(0)
    zhuzhai = zhuzhai.drop(0)
    zhuhu = zhuhu.drop(0)
    zy = zy.sort_values(by='SID')
    zy_families = spliteFamily(zy)

    for zy_family in zy_families:
        family_sid = zy_family['SID'].values[0]
        A = TableA[TableA['SID'] == family_sid]
        if A.empty == True:
            print("A表中无此户")
            continue
        one_zhuhu = zhuhu[zhuhu['HHID'] == family_sid]
        one_zhuzhai = zhuzhai[zhuzhai['HID'] == family_sid]
        B = TableB[TableB['SID'] == family_sid]
        ChangeH = 0
        LenM = 0
        # print(one_zhuhu)
        # print(A)
        # print(family_sid)
        surveyType = int(one_zhuhu['SURVEYTYPE'].values[0])
        TaskCode = B[B['SID'] == family_sid]['TASK'].values[0]
        Year = Table(zy_family,'YEAR')
        Month = Table(zy_family,'MONTH')
        openYear = Table(one_zhuhu,'OPENYEAR')
        if pd.isnull(openYear) == False:
            # openYear = int(one_zhuhu["OPENYEAR"].values[0])
            openMonth = Table(one_zhuhu,"OPENMONTH")     #int(one_zhuhu["OPENMONTH"].values[0])
        # 计算该用户是否报告期内新进住宅
        if TaskCode <= 4:
            lenM = 3
            if openYear == Year and openMonth <= Month and openMonth > Month -2:
                ChangeH = 1
        else:
            lenM = Month + 1
            if openYear == Year and openMonth <= Month:
                ChangeH = 1

        if (TaskCode >= 1 and TaskCode <= 7)and A['A102'].values[0] != 3 and surveyType == 1:
            # 收入、成本相关
            if TaskCode == 7 and ChangeH == 0 and one_zhuhu['M211'].values[0] == 2:
                if moneySum(zy_family,"11") + moneySum(zy_family,"12") + moneySum(zy_family,"13") + moneySum(zy_family,"14") > 500:
                    print("不是农业经营户有超过500元的农业生产经营账页数据")
            if ChangeH == 0 and one_zhuhu['M212'].values[0] == 2 and moneySum(zy_family,"22") + moneySum(zy_family,"51") > 0:
                print("不是二三产经营户有二三产经营账页数据")

            # 消费相关,家庭中个人账
            for row in A.iterrows():
                A_member = row[1]
                person = A_member['A100']
                if person > 0:
                    person_zy = zy_family[zy_family['PERSON'] == person]
                    sum1 = 0
                    sum2 = 0
                    for i in range(2201,2211):
                        sum1 += judge_moneySum(moneySum(person_zy,str(i)))
                        i += 1
                    for j in range(24011,24013):
                        sum2 += judge_moneySum(moneySum(person_zy,str(j)))
                        j += 1
                    if ChangeH == 0:
                        if judge_moneySum(moneySum(person_zy,"21")) + sum1 + sum2 >= 3:
                            print("一人有三种及以上收入来源")
                        if sum1 >= 2:
                            print("一人有两种及以上经营收入")
                        if sum2 >= 2:
                            print("一人有两种及以上养老收入（不含其他商业保险养老情况）")
                        if TaskCode <= 4:
                            if A_member['A204'] == 2 and moneySum(person_zy,"210111") > 0:
                                print("本季度末未就业有按月发放的工资")
                            if A_member['A202'] != 1 and A_member['A201'] == 3 and moneySum(person_zy,"240111") > 0:
                                print("本季度末退休有离退休金")
                            if A_member['A108'] < 1.5 and moneySum(person_zy,"21")+moneySum(person_zy,"22") > 15000:
                                print("本季度工作时间段，但按月收入很高")
                            if A_member['A119'] == 2 and moneySum(person_zy,"21")+moneySum(person_zy,"22")+moneySum(person_zy,"2401") > 0:
                                print("本季度非常住人员有工资性收入、经营性收入和离退休金")
                            if A_member['A119'] == 1 and moneySum(person_zy,"2406") > 0:
                                print("本季度常住人员有寄带回收入")
                            if A_member['A119'] == 2 and moneySum(person_zy,"2406") > 12000:
                                print("本季度非常住人员大量寄带回，请核实")
    end = datetime.datetime.now()
    print("运行时间：",end - begin)

# 打开csv文件 返回DataFrame对象
def read_csv(path):
    with open(path, 'r') as f:
        file = pd.read_csv(f, header=0)
    return file

if __name__ == '__main__':
    A_path = u"D:/研一/项目/CheckProgram/Auditing/输入文件夹/A卷310151.182.20181015.csv"
    B_path = u"D:/研一/审核程序/src/输入文件夹/B310151.18.csv"
    zy_path = u"D:/研一/项目/CheckProgram/Auditing/输入文件夹/03账页310151.1803.csv"
    zhuhu_path = u"D:/研一/项目/CheckProgram/Auditing/输入文件夹/住户样本310151.182.20181015.csv"
    zhuzhai_path = u"D:/研一/审核程序/src/输入文件夹/住宅名录310151.18.csv"

    TableA = read_csv(A_path)
    TableB = read_csv(B_path)
    zy = read_csv(zy_path)
    zhuzhai = read_csv(zhuzhai_path)
    zhuhu = read_csv(zhuhu_path)

    Zy_check_addition(TableA,TableB,zy,zhuzhai,zhuhu)