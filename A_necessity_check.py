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

# A_necessity_data = {'sid':[],'scode':[],'name':[],'code':[],'提示内容':[],'townname':[],'vname':[]}
# A_necessity_result = pd.DataFrame(A_necessity_data)
# A_necessity_result = A_necessity_result[['sid','scode','name','code','提示内容','townname','vname']]
# A_necessity_result = ''
A_necessity_result = pd.DataFrame()


def insert_to_pd(data):
    global A_necessity_result
    A_necessity_result = A_necessity_result.append(data, ignore_index=True)

def read_file(path):
    with open(path) as f:
        return pd.read_csv(f, header=0)

# 将A表中的数据按户进行划分
def spliteFamily(TableA):

    # 按照sid区分每一户
    # 先取sid，去掉重复值
    sid_array = TableA['SID'].drop_duplicates()
    # print(sid_array)
    i = 0
    for sid_index in sid_array:
        # 获取相同sid的行即为同一户的成员
        hu_data = TableA[TableA['SID'] == sid_index]
        # zy_data = TableD[TableD["SID"] == sid_index]

        hu_data = hu_data.sort_values(by='A103')#按照与本户户主关系排序
        yield hu_data


def Table(table,code):
    t = table[code]
    if t.empty == False:
        if type(t.values[0]) == type("str"):
            return int(t.values[0])
        return t.values[0]
    else:
        return 0


def A_necessity_check(TableA,zhuhu,xiaoqu,result_table):
    mylogger.logger.debug("A_necessity_check init..")
    global A_necessity_result
    A_necessity_result.drop(A_necessity_result.index, inplace=True)
    A_necessity_result = result_table

    # result = open(r'..\Auditing\审核结果输出\A_necessity_check_result.txt', 'w')
    hu_total = spliteFamily(TableA)
    for hu in hu_total:
        A,M=9101,993
        psA,psB=0,0
        hzAge,xb,hz,po=0,0,0,0
        # print(hu)
        family_sid = TableA['SID'].values[0]
        # print(type(zhuhu["HHID"].values[0]),type(family_sid))
        one_zhuhu = zhuhu[zhuhu["HHID"] == family_sid]
        scode = TableA['SCODE'].values[0]
        qu_vid = family_sid[0:15]
        qu = xiaoqu[xiaoqu['VID'] == qu_vid]
        townname = qu['TOWNNAME'].values[0]
        vname = qu['VNAME'].values[0]

        dict = {'sid':family_sid,'scode':scode,'townname':townname,'vname':vname}

        for index, A_table in hu.iterrows():
            # result.write(A_table['SID']+A_table['A101'] + '\n')
            # if A_table['A102'] == 3:
            #     continue
            # print(A_table['SID'])
            # print(index)
            # print(A_table)
            # while(A < 9120):
            person = A_table['A100']
            name = A_table['A101']
            dict['name'] = name

            if person == 0:
                # result.write("请更新家庭成员情况(A1)\n")
                value = "A100={}".format(person)
                dict['code'] = value
                dict['提示内容'] = "请更新家庭成员情况（A1）"
                insert_to_pd(dict)
            # else:
            #     # result.write('')

            if person > 0:
                psA += 1
                if pd.isnull(A_table['A200']) == False:
                    if person != A_table['A200']:
                        value = "A200={}".format(A_table['A200'])
                        dict['code'] = value
                        dict['提示内容'] = "问卷A有问题请在问卷录入窗口,请修正!"
                if A_table['A102'] % 4 == 3:
                    A += 1
                    continue
                psB += 1
                if A_table['A103'] == 1:
                    hzAge = A_table['YEAR'] - A_table['A105_1']
                    hz += 1
                    xb = A_table['A104']

                data = A_table['A103']
                if data == 2: po += 1
                if data == 2:
                    if A_table['A104'] == xb:
                        value = "A104={}".format(A_table['A104'])
                        dict['code'] = value
                        dict['提示内容'] = "户主与配偶性别相同"
                        insert_to_pd(dict)

                AAAAAAAA = 1
                if A_table['A105'] is None:
                    dict['code'] = "A105={}".format(A_table['A105'])
                    dict['提示内容'] = "请补填年龄，不足1岁请填写0"
                    insert_to_pd(dict)
                tbAge = Year - A_table['A105_1'] #填报的年龄
                tbYear = A_table['A105_1']
                tbMonth = A_table['A105_2']
                Age = Year-tbYear
                # 实际年龄
                if Month < tbMonth: Age -= 1

                # A1部分
                # 应该填报内容
                # A102开户时填4，其他时间非4，但每个报告期都可能开户
                # A102 == c4 ?: "人员增减情况越界，请填写(4)"
                # 开户时，应直接填报"4"
                data = A_table['A102']
                if data < 1 or data > 4:
                    dict['code'] = "A102={}".format(data)
                    dict['提示内容'] = "人员增减情况越界，请填写(1-4)"
                    insert_to_pd(dict)

                data = A_table['A103']
                if data < 1 or data > 10:
                    dict['code'] = "A103={}".format(data)
                    dict['提示内容'] = "与本户户主的关系越界，请填写(1-10)"
                    insert_to_pd(dict)

                data = A_table['A104']
                if data != 1 and data != 2:
                    dict['code'] = "A104={}".format(A_table['A104'])
                    dict['提示内容'] = "性别越界，请填写(1-2)"
                    insert_to_pd(dict)

                if tbYear == Year:
                    if tbMonth > Month:
                        dict['code'] = "tbYear={},tbMonth={}".format(Year,tbMonth)
                        dict['提示内容'] = "出生月份越界"
                        insert_to_pd(dict)

                data = A_table['A105']
                if data < 191001 or data > Year * 100 + Month:
                    dict['提示内容'] = "出生年月越界"
                    insert_to_pd(dict)

                if A_table['A107'] < 1 or A_table['A107'] > 9:
                    dict['提示内容'] = "民族越界，请填写(1-9)"
                    insert_to_pd(dict)

                data = A_table['A108']
                if data != 1 and data != 2 and data != 3 and data !=  4 and\
                        data != 5 and data != 7 and data != 11 and data != 12\
                        and data != 13 and data != 14 and data != 15 and data != 21\
                        and data != 22 and data != 23 and data != 31 and data != 32\
                        and data != 33 and data != 34 and data != 35 and data != 36\
                        and data != 37 and data != 41 and data != 42 and data != 43\
                        and data != 44 and data != 45 and data != 46 and data != 50\
                        and data != 51 and data != 52 and data != 53 and data != 54\
                        and data != 61 and data != 62 and data != 63 and data != 64\
                        and data != 65 and data != 71 and data != 81 and data != 82:
                    dict['提示内容'] = "户口登记地越界，请重新填写"
                    insert_to_pd(dict)

                if A_table['A109'] < 1 or A_table['A109'] > 3:
                    dict['code'] = "A109={}".format(A_table['A109'])
                    dict['提示内容'] = "户口性质越界，请填写(1-3)"
                    insert_to_pd(dict)

                data = A_table['A110']
                if data < 1 or data > 4:
                    dict['code'] = "A110={}".format(data)
                    dict['提示内容'] = "健康状况越界，请填写(1-4)"
                    insert_to_pd(dict)

                if Table(one_zhuhu,'M205') == 4:
                    if data == 4:
                        # dict['code'] = "A110={}".format(data)
                        dict['提示内容'] = "住家保姆、帮工,生活不能自理？"
                        insert_to_pd(dict)

                    if A_table['A112'] != 3:
                        dict['提示内容'] = "住家保姆、帮工,不能是在校生？"
                        insert_to_pd(dict)

                if A_table['A111'] is None:
                    dict['code'] = "A111={}".format(A_table['A111'])
                    dict['提示内容'] = "A111漏填，若没有参加医疗保险请填7"
                    insert_to_pd(dict)

                if Age >= 6:
                    if A_table['A112'] < 1 or A_table['A112'] > 3:
                        dict['code'] = "age={},A112={}".format(Age,A_table['A112'])
                        dict['提示内容'] = "是否在校生越界，请填写(1-3)"
                        insert_to_pd(dict)

                    if A_table['A113'] < 1 or A_table['A113'] > 7:
                        dict['code'] = "age={},A113={}".format(Age, A_table['A113'])
                        dict['提示内容'] = "教育程度越界，请填写(1-7)"
                        insert_to_pd(dict)

                if Age >= 15:
                    if A_table['A114'] < 1 or A_table['A114'] > 4:
                        dict['code'] = "age={},A114={}".format(Age, A_table['A114'])
                        dict['提示内容'] = "婚姻状况越界，请填写(1-4)"
                        insert_to_pd(dict)

                data = A_table['A115']
                if data is None:
                    dict['code'] = "A115={}".format(data)
                    dict['提示内容'] = "A115漏填，若本季度未在家居住请填0"
                    insert_to_pd(dict)

                if data > 3:
                    dict['code'] = "A115={}".format(data)
                    dict['提示内容'] = "本季度居住时间越界"
                    insert_to_pd(dict)

                if A_table['A116'] != 1 and A_table['A116'] != 2:
                    dict['code'] = "A116={}".format(A_table['A116'])
                    dict['提示内容'] = "是否其它住宅居住越界，请填写(1-2)"
                    insert_to_pd(dict)

                if A_table['A117'] != 1 and A_table['A117'] != 2:
                    dict['code'] = "A117={}".format(A_table['A117'])
                    dict['提示内容'] = "是否在本住宅居住一天以上越界，请填写(1-2)"
                    insert_to_pd(dict)

                if A_table['A118'] != 1 and A_table['A118'] != 2:
                    dict['code'] = "A118={}".format(A_table['A118'])
                    dict['提示内容'] = "是否打算居住一个半月以上越界，请填写(1-2)"
                    insert_to_pd(dict)

                if A_table['A119'] != 1 and A_table['A119'] != 2:
                    dict['code'] = "A119={}".format(A_table['A119'])
                    dict['提示内容'] = "是否常住人口越界，请填写(1-2)"
                    insert_to_pd(dict)

                if A_table['A120'] != 1 and A_table['A120'] != 2:
                    dict['code'] = "A120={}".format(A_table['A120'])
                    dict['提示内容'] = "是否是否持证残疾人越界，请填写(1-2))"
                    insert_to_pd(dict)

                # 应该跳转内容
                if A_table['A112'] + A_table['A113'] > 0:
                    if Age < 6:
                        dict['code'] = "age={},A112{}+A113{}={}".format(Age,A_table['A112'],A_table['A113'],A_table['A112']+A_table['A113'])
                        dict['提示内容'] = "小于6岁，不用填报A112|A113"
                        insert_to_pd(dict)

                if A_table['A114'] > 0:
                    if Age < 15:
                        dict['code'] = "age={},A114={}".format(Age,A_table['A114'])
                        dict['提示内容'] = "小于15岁，不用填报A114"
                        insert_to_pd(dict)

                data = A_table['A112']
                if Age < 15 or data != 3:
                    if A_table['A201'] + A_table['A208'] > 0:
                        dict['code'] = "age={},A112={},A201{}+A208{}={}".format(Age,data,A_table['A201'],A_table['A208'],A_table['A201']+A_table['A208'])
                        dict['提示内容'] = "小于15岁或在校生，不用填报A2问卷"
                        insert_to_pd(dict)
                if data != 3:
                    data1 = A_table['A113']
                    if data1 == 1:
                        dict['code'] = "A112={},A113={}".format(data,data1)
                        dict['提示内容'] = "在校生没上过学？"
                        insert_to_pd(dict)
                    else:
                        if Age > 14 and data1 < 3:
                            dict['code'] = "age={},A112={},A113={}".format(Age,data, data1)
                            dict['提示内容'] = "14周岁以上在校生，学历低于小学？"
                            insert_to_pd(dict)

                        if Age > 17 and data1 < 4:
                            dict['code'] = "age={},A112={},A113={}".format(Age, data, data1)
                            dict['提示内容'] = "17周岁以上在校生，学历低于初中？"
                            insert_to_pd(dict)
                        if Age > 20 and data1 < 5:
                            dict['code'] = "age={},A112={},A113={}".format(Age, data, data1)
                            dict['提示内容'] = "20周岁以上在校生，学历低于高中？"
                            insert_to_pd(dict)
                        if Age > 24 and data1 < 6:
                            dict['code'] = "age={},A112={},A113={}".format(Age, data, data1)
                            dict['提示内容'] = "24周岁以上在校生，学历低于大学？"
                            insert_to_pd(dict)

                if A_table['A108'] == 'U':
                    dict['code'] = "A108={}".format(A_table['A108'])
                    dict['提示内容'] = "户口在本省，不 用填省码"
                    insert_to_pd(dict)

                data = A_table['A119']
                if A_table['A119'] != 1:
                    if A_table['A115'] >= 1.5 or A_table['A118'] == 1:
                        dict['code'] = "A119={},A115={},A118={}".format(data,A_table['A115'],A_table['A118'])
                        dict['提示内容'] = "满足条件A，应视为常住人口"
                        insert_to_pd(dict)

                    if A_table['A116'] == 2 and A_table['A117'] == 1:
                        dict['code'] = "A119={},A116={},A117={}".format(data, A_table['A116'], A_table['A117'])
                        dict['提示内容'] = "满足条件A，应视为常住人口"
                        insert_to_pd(dict)

                    if A_table['A112'] == 1:
                        dict['code'] = "A119={},A112={}".format(data, A_table['A112'])
                        dict['提示内容'] = "满足条件C，应视为常住人口"
                        insert_to_pd(dict)

                # //***************A2部分*****************
                # //劳动力部分全部都是A，跟第一部分A不一样。

                data1 = A_table['A112']
                data2 = A_table['A200']
                if Age >= 16 and data1 == 3 and pd.isnull(data2) is None:
                    dict['code'] = "age={},A112={},A200={}".format(Age, data1,data2)
                    dict['提示内容'] = "16岁及以上非在校生应填写A2部分"
                    insert_to_pd(dict)
                    A += 1
                if Age >= 16 and data1 == 3 and pd.isnull(data2)==False:
                    #应该填报内容
                    if A_table['A201'] != 1 and A_table['A201'] != 2 and A_table['A201'] != 3:
                        dict['code'] = "age={},A112={},A200={},A201={}".format(Age, data1,data2, A_table['A201'])
                        dict['提示内容'] = "是否离退休越界，请填写(1-3)"
                        insert_to_pd(dict)

                    if pd.isnull(A_table['A202']) == True:
                        dict['code'] = "age={},A112={},A200={},A202={}".format(Age, data1, data2, A_table['A202'])
                        dict['提示内容'] = "A202漏填，若没有参加养老保险请填6"
                        insert_to_pd(dict)

                    if A_table['A203'] != 1 and A_table['A203'] != 2:
                        dict['code'] = "age={},A112={},A200={},A203={}".format(Age, data1, data2, A_table['A203'])
                        dict['提示内容'] = "是否丧失劳动力越界，请填写(1-2)"
                        insert_to_pd(dict)

                    data3 = A_table['A203']
                    data4 = A_table['A204']
                    if data3 == 2:
                        if data4 != 1 and data4 != 2:
                            dict['code'] = "age={},A112={},A200={},A203={},A204={}".format(Age, data1, data2, data3,data4)
                            dict['提示内容'] = "是否从业过越界，请填写(1-2)"
                            insert_to_pd(dict)

                        if data4 == 1:
                            if A_table['A205'] < 1 or A_table['A205'] > 7:
                                dict['code'] = "age={},A112={},A200={},A201={},A203={},A204={},A205={}".format(Age,data, data1, data2,data3,data4,A_table['A205'])
                                dict['提示内容'] = "就业类型越界，请填写(1-7)"
                                insert_to_pd(dict)

                            if A_table['A206'] < 1 or A_table['A206'] > 20:
                                dict['code'] = "age={},A112={},A200={},A201={},A203={},A204={},A206={}".format(Age,data,data1,data2,data3,data4,A_table['A206'])
                                dict['提示内容'] = "行业越界，请填写(1-20)"
                                insert_to_pd(dict)

                            if A_table['A207'] < 1 or A_table['A207'] > 8:
                                dict['code'] = "age={},A112={},A200={},A201={},A203={},A204={},A207={}".format(Age,data,data1,data2,data3,data4,A_table['A207'])
                                dict['提示内容'] = "工作种类越界，请填写(1-8)"
                                insert_to_pd(dict)

                            if A_table['A208'] < 0.1 or A_table['A208'] > 3:
                                dict['code'] = "age={},A112={},A200={},A201={},A203={},A204={},A208={}".format(Age,data,data1,data2,data3,data4,A_table['A208'])
                                dict['提示内容'] = "工作总时间越界"
                                insert_to_pd(dict)

                            data9 = A_table['A209']
                            if data9 != 1 and data9 != 2 and data9 != 3 and data9 != 4 and data9 != 5 and data9 != 7 and\
                                data9 != 11 and data9 != 12 and data9 != 13 and data9 != 14 and data9 != 15 and \
                                data9 != 21 and data9 != 22 and data9 != 23 and data9 != 31 and \
                                data9 != 32 and data9 != 33 and data9 != 34 and data9 != 35 and \
                                data9 != 36 and data9 != 37 and data9 != 41 and data9 != 42 and \
                                data9 != 43 and data9 != 44 and data9 != 45 and data9 != 46 and \
                                data9 != 50 and data9 != 51 and data9 != 52 and data9 != 53 and \
                                data9 != 54 and data9 != 61 and data9 != 62 and data9 != 63 and \
                                data9 != 64 and data9 != 65 and data9 != 71 and data9 != 81 and \
                                data9 != 82 and data9 != 83:
                                dict['code'] = "age={},A112={},A200={},A201={},A203={},A204={},A209={}".format(Age,data1,data2,data3,data4,data9)
                                dict['提示内容'] = "本季度工作地点越界，请重新填写"
                                insert_to_pd(dict)

                            data10 = A_table['A210']
                            if data10 != 1 and data10 != 2 and data10 != 3 and data10 != 11\
                                and data10 != 12 and data10 != 13 and data10 != 14 and data10 != 15\
                                and data10 != 21 and data10 != 22 and data10 != 23 and data10 != 31\
                                and data10 != 32 and data10 != 33 and data10 != 34 and data10 != 35\
                                and data10 != 36 and data10 != 37 and data10 != 41 and data10 != 42\
                                and data10 != 43 and data10 != 44 and data10 != 45 and data10 != 46\
                                and data10 != 50 and data10 != 51 and data10 != 52 and data10 != 53\
                                and data10 != 54 and data10 != 61 and data10 != 62 and data10 != 63\
                                and data10 != 64 and data10 != 65 and data10 != 71 and data10 != 81\
                                and data10 != 82 and data10 != 83:
                                dict['code'] = "age={},A112={},A200={},A201={},A203={},A204={},A210={}".format(Age,data1,data2,data3,data4,data10)
                                dict['提示内容'] = "最远工作或学习地点越界，请重新填写"
                                insert_to_pd(dict)

                            if A_table['A211'] < 1 or A_table['A211'] > 8:
                                dict['code'] = "age={},A112={},A200={},A201={},A203={},A204={},A211={}".format(Age,data1,data2,data3,data4,A_table['A211'])
                                dict['提示内容'] = "主要群体种类越界，请填写(1-8)"
                                insert_to_pd(dict)

                            if A_table['A212'] < 1 or A_table['A212'] > 8:
                                dict['code'] = "age={},A112={},A200={},A201={},A203={},A204={},A212={}".format(Age,data1,data2,data3,data4,A_table['A212'])
                                dict['提示内容'] = "次要群体种类越界，请填写(1-8)"
                                insert_to_pd(dict)

                            if A_table['A213'] < 1 or A_table['A213'] > 4:
                                dict['code'] = "age={},A112={},A200={},A201={},A203={},A204={},A213={}".format(Age,data1,data2,data3,data4,A_table['A213'])
                                dict['提示内容'] = "最高技能证书越界，请填写(1-4)"
                                insert_to_pd(dict)

                            if A_table['A214'] < 1 or A_table['A214'] > 4:
                                dict['code'] = "age={},A112={},A200={},A201={},A203={},A204={},A214={}".format(Age,data1,data2,data3,data4,A_table['A214'])
                                dict['提示内容'] = "最高证书职称越界，请填写(1-4)"
                                insert_to_pd(dict)

                            if A_table['A211'] == 8 and A_table['A212'] < 8:
                                dict['code'] = "age={},A112={},A200={},A201={},A203={},A204={},A211={},A212={}".format(Age,data1,data2,data3,data4,A_table['A211'],A_table['A212'])
                                dict['提示内容'] = "主要群体种类为不属于任何群体，次要群体种类也应不属于任何群体"
                                insert_to_pd(dict)

                            if 8 > A_table['A211'] > 0  and A_table['A211'] == A_table['A212']:
                                dict['code'] = "age={},A112={},A200={},A201={},A203={},A204={},A211={},A212={}".format(
                                    Age, data1, data2, data3, data4, A_table['A211'], A_table['A212'])
                                dict['提示内容'] = "主要群体和次要群体填写内容一致"
                                insert_to_pd(dict)

                    data = Table(one_zhuhu,'M205')
                    if data == 4:
                        if A_table['A203'] != 2:
                            dict['code'] = "age={},A112={},A200={},M205={},A203={}".format(data, data1, data2, data,A_table['A203'])
                            dict['提示内容'] = "住家保姆、帮工,或集体居住户,不能丧失劳动能力"
                            insert_to_pd(dict)

                        if A_table['A204'] != 1:
                            dict['code'] = "age={},A112={},A200={},M205={},A204={}".format(data, data1, data2,data, A_table['A204'])
                            dict['提示内容'] = "住家保姆、帮工,A204要填从业"
                            insert_to_pd(dict)

                        if A_table['A205'] != 5:
                            dict['code'] = "age={},A112={},A200={},M205={},A205={}".format(data, data1, data2, data,
                                                                                           A_table['A205'])
                            dict['提示内容'] = "住家保姆、帮工,应该是其他雇员"
                            insert_to_pd(dict)

                    # 应该跳转内容
                    sum = A_table['A205'] + A_table['A206'] + A_table['A207'] + A_table['A208']
                    if A_table['A204'] + sum > 0:
                        if A_table['A203'] == 1:
                            dict['提示内容'] = "丧失劳动力，不用填报A204-A208"

                    if sum > 0 and A_table['A204'] == 2:
                        dict['提示内容'] = "本季未从业，不用填报A205-A208"

                    # 逻辑关系
                    if (A_table['A203'] == 2 or A_table['A204'] == 1) and A_table['A110'] == 4:
                        dict['code'] = "A203={},A204={}，A110={}".format(A_table['A203'],A_table['A204'],A_table['A110'])
                        dict['提示内容'] = "生活不能自理，还具有劳动能力?"
                        insert_to_pd(dict)

                    if A_table['A204'] == 1 and A_table['A208'] == 0:
                        dict['code'] = "A204={}，A208={}".format(A_table['A204'], A_table['A208'])
                        dict['提示内容'] = "本季度从业过，则从事工作的时间不能为0"
                        insert_to_pd(dict)
            A += 1

        if psA > 0 and psB > 0:
            if hz > 1:
                dict['提示内容'] = "两个以上户主？"
            if po > 1:
                dict['提示内容'] = "户主有两个配偶？"
            if 1 < hzAge <= 12:
                dict['提示内容'] = "户主为小孩？"
            if hzAge < 1:
                dict['提示内容'] = "没有户主？"

    return A_necessity_result

    # result.write("ok")

# result.write(str)
    # result.write(hzAge,xb,hz,po)


if __name__ == "__main__":
    A_path = "D:/研一/项目/CheckProgram/Auditing/输入文件夹/A310151.18.csv"
    xiaoqu_path = u"D:\研一\项目\CheckProgram\Auditing\输入文件夹\小区名录310151.18.csv"
    zhuhu_path = u"D:/研一/项目/CheckProgram/Auditing/输入文件夹/住户样本310151.18.csv"
    TableA = read_file(A_path)
    xiaoqu = read_file(xiaoqu_path)
    zhuhu = read_file(zhuhu_path)

    A_necessity_data = {'sid':[],'scode':[],'name':[],'code':[],'提示内容':[],'townname':[],'vname':[]}
    A_necessity_resut = pd.DataFrame(A_necessity_data)
    A_necessity_resut = A_necessity_resut[['sid','scode','name','code','提示内容','townname','vname']]

    A_necessity_check(TableA,zhuhu,xiaoqu,A_necessity_resut)
    # global A_necessity_result
    A_necessity_result.to_csv('A_necessity_result.csv',encoding='utf_8_sig')
