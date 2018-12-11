# 指标行数:100
# ********************************
# *   全国住户生活状况调查季报   *
# *         问卷A审核公式        *
# *        2015年08月23日        *
# ********************************
import pandas as pd
# import numpy as np
import datetime
from deal_hu import spliteFamily
import myLogging as mylogger


Year = datetime.datetime.now().year
Month = datetime.datetime.now().month
A_suggestion_result = pd.DataFrame()
def insert_to_pd(data):
    global A_suggestion_result
    A_suggestion_result = A_suggestion_result.append(data, ignore_index=True)


def spliteFamily(table):
    sid_array = table["SID"].drop_duplicates()
    for sid_index in sid_array:
        # 获取相同sid的行即为同一户的成员
        hu_data = table[table["SID"] == sid_index]
        # 按照人码进行排序
        hu_data = hu_data.sort_values(by='A103')
        yield hu_data


def Table(table,code):
    t = table[code]
    if t.empty == False:
        if type(t.values[0]) == type("str"):
            return int(t.values[0])
        return t.values[0]
    else:
        return 0


def read_file(path):
    with open(path) as f:
        return pd.read_csv(f, header=0)


def A_suggestion_check(TableA,xiaoqu,result_table):
    # A,psA,psB,hzAge,xb,hz,po
    # while(A < 9120):
    mylogger.logger.debug("A_suggestion_check init..")
    # result = open(r'D:\研一\审核程序\src\审核结果输出\A_suggestion_check_result.txt', 'w')
    global A_suggestion_result
    A_suggestion_result.drop(A_suggestion_result.index, inplace=True)
    A_suggestion_result = result_table

    hu_total = spliteFamily(TableA)
    for hu in hu_total:
        family_sid = TableA['SID'].values[0]
        scode = TableA['SCODE'].values[0]
        qu_vid = family_sid[0:15]
        qu = xiaoqu[xiaoqu['VID'] == qu_vid]
        townname = qu['TOWNNAME'].values[0]
        vname = qu['VNAME'].values[0]

        dict = {'sid': family_sid, 'scode': scode, 'townname': townname, 'vname': vname}

        A, M = 9101, 993
        psA, psB = 0, 0
        hzAge, xb, hz, po = 0, 0, 0, 0
        for index,table in hu.iterrows():
            # print(table['A101'])
            # result.write(table['SID']+table['A101'] + ':\n')
            person = table['A100']
            name = table['A101']
            dict['name'] = name
            dict['person'] = person
            if A == 9101 and person == 0:
                dict['code'] = "A={},A100={}".format(A,person)
                dict['提示内容'] = "请更新家庭成员情况(A1)"
                insert_to_pd(dict)

            if person > 0:
                psA += 1
                if pd.isnull(table['A200']) == False:
                    if person != table['A200']:
                        dict['code'] = "A100={},A200={}".format(person, table['A200'])
                        dict['提示内容'] = "问卷A有问题请在问卷录入窗口修正!"
                        insert_to_pd(dict)

                if table['A102'] % 4 == 3:
                    A += 1
                    continue
                psB += 1
                if table['A103'] == 1: hzAge = table['A106']
                if table['A103'] == 1: hz += 1
                if table['A103'] == 2: po += 1
                if table['A103'] == 1: xb = table['A104']

                AAAAAAAA = 1
                tbAge = table['A106'] #填报的年龄
                tbYear = table['A105_1']
                tbMonth = table['A105_2']
                Age = Year-tbYear
                if Month < tbMonth: Age -= 1    #实际年龄

            #******A1部分******

                # if table['A103'] == 2 and abs(hzAge-Age) > 20:
                if table['A103'] == 2 and (hzAge - Age > 20 or Age - hzAge > 20):
                    dict['提示内容'] = "|户主的年龄－配偶的年龄|>20"
                    insert_to_pd(dict)
                if table['A103'] == 3 and hzAge-Age < 8:
                    dict['提示内容'] = "户主的年龄－子女的年龄<8"
                    insert_to_pd(dict)
                if table['A103'] == 7 and abs(Age-hzAge) < 8:
                    dict['提示内容'] = "户主的年龄－媳婿的年龄<8"
                    insert_to_pd(dict)
                if table['A103'] == 9 and abs(Age - hzAge) >= 20:
                    dict['提示内容'] = "户主的年龄－兄弟姐妹的年龄≥20"
                    insert_to_pd(dict)
                if table['A103'] == 4 and Age - hzAge < 8:
                    dict['提示内容'] = "父母的年龄－户主的年龄<8"
                    insert_to_pd(dict)
                if table['A103'] == 5 and Age - hzAge < 8:
                    dict['提示内容'] = "岳父母的年龄－户主的年龄<8"
                    insert_to_pd(dict)
                if table['A103'] == 6 and Age - hzAge < 15:
                    dict['提示内容'] = "祖父母的年龄－户主的年龄<15"
                    insert_to_pd(dict)
                if table['A103'] == 8 and hzAge - Age < 15:
                    dict['提示内容'] = "户主的年龄－孙子女的年龄<15"
                    insert_to_pd(dict)
                if table['A110'] == 4:
                    if table['A112'] == 1 or table['A112'] == 2:
                        dict['提示内容'] = "生活不能自理，是否在校生，请确认"
                        insert_to_pd(dict)
                if table['A112'] == 3:
                    if 14 >= table['A106'] >= 8:
                        if table['A110'] != 1 and table['A110'] != 2:
                            dict['提示内容'] = "义务教育年龄且健康，辍学？"
                            insert_to_pd(dict)

                # if table['A111'] is None:
                #     dict['提示内容']"医疗保险漏填！")
                # else:
                #     medicalType = (0, 0, 0, 0, 0, 0, 0, 0)
                #     p = table['A111']
                #     for i in range(0,6):
                #         Q = p[i]
                #         if Q > 0 and Q < 7:
                #             medicalType[Q] += 1
                #     #j = 1 + +7
                #     if table['109'] == 2 and table['A111'] == 1:
                #         result.write(" 参加的医疗保险中（A111=[A111]），非农业户口不应出现选项1")

                if table['A112'] == 1 or table['A112'] == 2:
                    if table['A106'] > 32:
                        dict['提示内容'] = "32周岁以上还是在校生？"
                        insert_to_pd(dict)
                    if table['A113'] == 7 and table['A106'] <= 20:
                        dict['提示内容'] = "不到20岁就读研究生？"
                        insert_to_pd(dict)
                    if table['A113'] == 6 or table['A113'] == 5:
                        if table['A106'] <16:
                            dict['提示内容'] = "不到16岁就上大学？"
                            insert_to_pd(dict)
                    if table['A113'] == 4 and table['A106'] <= 14:
                        dict['提示内容'] = "不到14岁就上高中？"
                        insert_to_pd(dict)
                    if table['A113'] == 3 and table['A106'] <= 10:
                        dict['提示内容'] = "不到10岁就上初中？"
                        insert_to_pd(dict)


            #***************A2部分****************
            #劳动力部分全部都是A，跟第一部分A不一样。
                if table['A200'] is None:
                    dict['提示内容'] = "劳动力成员的编码未填"
                    insert_to_pd(dict)
                else:
                    if Age >= 16 and table['A112'] == 3:
                        if table['A201'] == 1 and Age < 50:
                            dict['提示内容'] = "不到50岁就离退休，请核实"
                            insert_to_pd(dict)
            A += 1
            # dict['提示内容']str)
            # result.write(hzAge,xb,hz,po)

    return A_suggestion_result

if __name__ == "__main__":

    A_path = "D:/研一/项目/CheckProgram/Auditing/输入文件夹/A310151.18.csv"
    xiaoqu_path = u"D:\研一\项目\CheckProgram\Auditing\输入文件夹\小区名录310151.18.csv"
    # zhuhu_path = u"D:/研一/项目/CheckProgram/Auditing/输入文件夹/住户样本310151.18.csv"
    TableA = read_file(A_path)
    xiaoqu = read_file(xiaoqu_path)
    # zhuhu = read_file(zhuhu_path)

    A_suggestion_data = {'year':[],'sid': [], 'scode': [], 'name': [], 'code': [], '提示内容': [], 'townname': [], 'vname': []}
    A_suggestion_result = pd.DataFrame(A_suggestion_data)
    A_suggestion_result = A_suggestion_result[['year','sid', 'scode', 'name', 'code', '提示内容', 'townname', 'vname']]

    A_suggestion_check(TableA, xiaoqu,A_suggestion_result)
    A_suggestion_result.to_csv('A_suggestion_result.csv', encoding='utf_8_sig')