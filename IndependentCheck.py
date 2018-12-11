import pandas as pd
import re
from decimal import Decimal
import datetime
import myLogging as mylogger

zy_independent_result = pd.DataFrame()

def insert_to_pd(data):
    global zy_independent_result
    zy_independent_result = zy_independent_result.append(data, ignore_index=True)

def spliteFamily(table):
    sid_array = table["SID"].drop_duplicates()
    for sid_index in sid_array:
        # 获取相同sid的行即为同一户的成员
        hu_data = table[table["SID"] == sid_index]
        # 按照人码进行排序
        hu_data = hu_data.sort_values(by='CODE')
        yield hu_data

def fill4(x):
    return x.zfill(4)

def add_column(zy,codes):
    #在账页表中添加列Sidr,Sidrm,Note4，NNote11，Note22，Note33,Note44
    zy.insert(12,'Sidr',zy['SID']+'p'+zy['PERSON'])
    zy.insert(13,'Sidrm',zy['SID']+'p'+zy['PERSON']+zy['MONTH'])
    pd.set_option('display.width', None)  # 显示所有数据
    # print(zy)
    #为账页中出现的编码添加录入控制码信息
    codes = codes.drop(0)
    # zy = zy.drop(0)
    # print(codes['CODE'])
    x = codes[['CODE', 'note4', 'markyc']]
    df = pd.merge(zy, x, how='left', on=['CODE'])
    df["note4"] = df["note4"].apply(fill4)
    # print(type(df['note4']))
    zy.insert(14,'note4',df['note4'])
    zy.insert(15,'note11',df['note4'].apply(lambda x: x[0]))
    zy.insert(16,'note22',df['note4'].apply(lambda x: x[1]))
    zy.insert(17, 'note33', df['note4'].apply(lambda x: x[2]))
    zy.insert(18, 'note44', df['note4'].apply(lambda x: x[3]))
    # zy["note11"] = zy["note11"].apply(lambda x: x[0])
    # zy["note22"] = zy["note22"].apply(lambda x: x[1])
    # zy["note33"] = zy["note33"].apply(lambda x: x[2])
    # zy["note44"] = zy["note44"].apply(lambda x: x[3])

    zy.insert(19,'markyc',df['markyc'])
    # print(zy)
    return zy

def Table(table,code):
    t = table[code]
    if t.empty == False:
        if type(t.values[0]) == type("str"):
            return int(t.values[0])
        return t.values[0]
    else:
        return 0

def code_match(table,code):
    pattern = code + "(.*)"
    flag = 0
    for x in table['CODE']:
        if re.match(pattern,x):
            flag = 1
            break
    return flag

# 累计相同类型的账页
def num_same_zy(zy,code):
    pattern = code + "(.*)"
    num = 0
    code = [x for x in zy['CODE'] if re.match(pattern, x)]
    num = len(code)
    return num

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
    return Decimal(0)


#家庭人口
def sum_people(family):
    return len(family.index)


def IndependentCheck(tableA,tableB,zy,zhuhu,xiaoqu,codes,result_table):
    mylogger.logger.debug("zy_independent_check init...")
    global zy_independent_result
    zy_independent_result.drop(zy_independent_result.index,inplace=False)
    zy_independent_result = result_table
    zy = zy.drop(0)
    # zhuzhai = zhuzhai.drop(0)
    zhuhu = zhuhu.drop(0)
    zy = zy.sort_values(by='SID')
    zy = add_column(zy,codes)
    zy_families = spliteFamily(zy)
    for zy_family in zy_families:
        family_sid = zy_family['SID'].values[0]
        A = tableA[tableA['SID'] == family_sid]
        A = A.drop_duplicates()
        # print(A)
        B = tableB[tableB['SID'] == family_sid]
        B = B.drop_duplicates()
        # print(B)
        one_zhuhu = zhuhu[zhuhu['HHID'] == family_sid]
        qu_vid = family_sid[0:15]
        qu = xiaoqu[xiaoqu['vID'] == qu_vid]
        townname = qu['townName'].values[0]
        vname = qu['vName'].values[0]
        coun = str(qu['coun'].values[0])
        task = str(B['TASK'].values[0])
        scode = zy_family['SCODE'].values[0]
        year = str(zy_family['YEAR'].values[0])
        month = str(zy_family['MONTH'].values[0])
        dict = {'year':year, 'task':task, 'month': month, 'coun':coun,'scode':scode, 'sid':family_sid,'person':str(99), 'townname':townname, 'vname':vname}

        if Table(one_zhuhu,'M211') != 1:
            money = moneySum(zy_family,"12")
            if money > 0:
                dict['code'] = "M211={},'12'={}".format(Table(one_zhuhu,"M211"),money)
                dict['核实内容'] = "此户M211不是农业经营户，却出现出售农产品及提供服务编码（12打头），请核实！"
                insert_to_pd(dict)

        if Table(one_zhuhu, "M216") == 2:
            renkou = sum_people(A)
            money = moneySum(zy_family, "3")
            if renkou > 0:
                if money / renkou < 300:
                    dict['code'] = "M216={},'3'={},'人数'={}".format(Table(one_zhuhu, "M211"), money, renkou)
                    dict['核实内容'] = "此户不是低保户，但月均消费支出不满300元？请核实！"
                    insert_to_pd(dict)

        if code_match(zy_family, "333307") == 1:
            dict['code'] = "code=333307"
            dict['核实内容'] = "使用管道液化石油气？请核实！"
            insert_to_pd(dict)

        if len(zy_family.index) < 30:
            dict['核实内容'] = "记账笔数少于30笔，请核实并写明原因！"
            insert_to_pd(dict)

        money = moneySum(zy_family, "240211")
        if money != 0 and Table(one_zhuhu, 'M216') == 2:
            dict['code'] = "'240211'={},M216={}".format(money,Table(one_zhuhu,'M216'))
            dict['核实内容'] = "本月发生低保收入，为何该户不是低保户（M216）？，请核实！"
            insert_to_pd(dict)

        if Table(one_zhuhu, "M216") == 1:
            if money == 0:
                dict['code'] = "'240211'={},M216={}".format(money, Table(one_zhuhu, 'M216'))
                dict['核实内容'] = "该户为低保户（M216），为何没有低保收入（2402111）？请核实并注明原因！"
                insert_to_pd(dict)

        #zycheck about tableA and zy
        # if Table(one_zhuhu,'M217') == 1:
        for rowA in A.iterrows():
            A_member = rowA[1]
            person = A_member['A100']
            person_zy = zy_family[zy_family['PERSON'] == str(person)]
            # print(person_zy)
            dict['person'] = str(person)
            dict['name'] = A_member['A101']

            A204 = A_member['A204']
            A205 = A_member['A205']
            A208 = A_member['A208']
            m1 = moneySum(person_zy, "12")
            m2 = moneySum(person_zy, "2101")
            m3 = moneySum(person_zy, "22")
            if A205 == 1 and A204 == 1 and A208 != 0:
                if m1 + m2 + m3 == 0:
                    dict['code'] = "A205={},A204={},A208={},'12'={},'2101'={},'22'={}".format(A205,A204,A208,m1,m2,m3)
                    dict['核实内容'] = "雇主漏填收入，请核实！"
                    insert_to_pd(dict)

            if 2 <= A205 <= 5 and A208 > 0:
                m4 = moneySum(person_zy, "21221")
                if m1 + m3 + m4 == 0:
                    dict['code'] = "A205={},A208={},'12'={},'21221'={},'22'={}".format(A205, A208, m1,m4,m3)
                    dict['核实内容'] = "此人漏填工资性收入，请核实！"
                    insert_to_pd(dict)

            if A204 != 1 or (A205 < 2 or A205 > 5) or A208 == 0:
                if m2 != 0:
                    dict['code'] = "A204={},A205={},A208={},'2101'={}".format(A204,A205,A208,m2)
                    dict['核实内容'] = "多填工资性收入，请核实！"
                    insert_to_pd(dict)

            if A_member['A204'] == 1 and A_member['A205'] == 7 and A_member['A208'] != 0:
                if m3 == 0:
                    dict['code'] = "A204={},A205={},A208={},'22'={}".format(A204, A205, A208, m3)
                    dict['核实内容'] = "漏填非农自营收入，请核实！"
                    insert_to_pd(dict)

            if A_member['A204'] != 1 or A_member['A205'] != 7 or A_member['A208'] == 0:
                if m3 != 0:
                    dict['code'] = "A204={},A205={},A208={},'2101'={}".format(A204, A205, A208, m3)
                    dict['核实内容'] = "多填非农自营收入，请核实！"
                    insert_to_pd(dict)

            if A_member['A206'] != 12:
                if code_match(person_zy, "220911") == 1:
                    dict['code'] = "A206={},'220911'={}".format(A_member['A206'],moneySum(person_zy,'220911'))
                    dict['核实内容'] = "确有租赁和商务服务收入？请核实并注明具体收入内容！"
                    insert_to_pd(dict)

            A201 = A_member['A201']
            A202 = A_member['A202']
            m1 = moneySum(person_zy,"2401")
            m11 = moneySum(person_zy,"240111")
            m21 = moneySum(person_zy,"240121")
            m91 = moneySum(person_zy, "240191")
            if A201 == 1 or A201 == 2:
                if A202 == 2 and code_match(person_zy, "2401") == 1 and code_match(person_zy,"240111") != 1:
                    dict['code'] = "A201={},A202={},'2401'={},'240111'={}".format(A201,A202,m1,m11)
                    dict['核实内容'] = "参加城镇职工养老保险，记账代码应填240111，请核实A202或编码是否正确。"
                    insert_to_pd(dict)

                if A202 == 3 and code_match(person_zy, "2401") == 1 and code_match(person_zy,"240121") != 1:
                    dict['code'] = "A201={},A202={},'2401'={},'240121'={}".format(A201,A202,m1,m21)
                    dict['核实内容'] = "参加城镇居民养老保险，记账代码应填240121，请核实A202或编码是否正确。"
                    insert_to_pd(dict)

                if A202 == 4 or A202 == 5 and code_match(person_zy, "2401") == 1 and code_match(person_zy, "240191") != 1:
                    dict['code'] = "A201={},A202={},'2401'={},'240191'={}".format(A201, A202, m1,m91)
                    dict['核实内容'] = "参加其他养老保险，记账代码应填240191，请核实A202或编码是否正确。"
                    insert_to_pd(dict)

            if code_match(person_zy, "240111") == 1:
                if A201 == 3 and A202 != 3 and A202 != 4 and A202 != 5:
                    dict['code'] = "A201={},A202={},'240111'={}".format(A201, A202, m11,)
                    dict['核实内容'] = "A201=3，为何有A202（4、5）之外的养老金收入？请核实!"
                    insert_to_pd(dict)

            if A_member['A106'] >= 60 and A202 != 6 and A202 != 0 and A204 == 2:
                if moneySum(person_zy, "2401") == 0:
                    dict['code'] = "A106={},A202={},A204={},'2401'={}".format(A_member['A106'], A202,A204, m1)
                    dict['核实内容'] = "60岁以上为工作参保人员，没有任何养老金收入？请核实！"
                    insert_to_pd(dict)

            if (A201 == 1 or A201 == 2) and A202 != 4 and A202 != 5:
                if code_match(person_zy,"240191") == 1:
                    dict['code'] = "A201={},A202={},'240191'={}".format(A201, A202, m91)
                    dict['核实内容'] = "A202≠4,5，为何有其他养老保险收入，请核实！"
                    insert_to_pd(dict)
                    # dict['核实内容'] =("此人为退休者、A202里面没有4或5，为何有其他养老保险收入，请核实！")

            if A204 != 2 and code_match(person_zy, "240811") == 1:
                dict['code'] = "A204={},'240811'={}".format(A204,moneySum(person_zy,"240811"))
                dict['核实内容'] = "非失业人员，有失业保险金？请核实！"
                insert_to_pd(dict)

            if A201 == 3 and A204 == 1 and A202 == 2:
                if moneySum(person_zy, "532111") == 0:
                    dict['code'] = "A201={},A202={},'532111'={}".format(A201, A202, moneySum(person_zy,"532111"))
                    dict['核实内容'] = "漏填个人缴纳的养老保险金，请核实！"
                    insert_to_pd(dict)

            if A202 != 1 and A202 != 5:
                if code_match(person_zy, "532911") == 1:
                    dict['code'] = "A202={},'532911'={}".format( A202,moneySum(person_zy,"532911"))
                    dict['核实内容'] = "非农保镇保人员，为何有其他社保支出？请注明具体支出内容！"
                    insert_to_pd(dict)

            if A205 != 7:
                if code_match(person_zy, "5513") == 1 or code_match(person_zy, "5514") == 1:
                    dict['code'] = "A205={},'5513'={},'5514'={}".format(A205,moneySum(person_zy,"5513"),moneySum(person_zy,'5514'))
                    dict['核实内容'] = "不是非农自营对象，为何有生产性固定资产支出？请核实并注明具体情况！"
                    insert_to_pd(dict)

            # 多填农业自营收入（12 - --15）

            if A202 == 4 or A202 == 6:
                if code_match(person_zy, "532111") == 1:
                    dict['code'] = "A202={},'532111'={}".format(A202,moneySum(person_zy,"532111"))
                    dict['核实内容'] = "A202=4、6，为何有个人缴纳的养老保险支出，请查改！"
                    insert_to_pd(dict)

            A111 = A_member['A111']
            if A111 == 4 or A111 == 5 or A111 == 7:
                if code_match(person_zy,"532211") == 1:
                    dict['code'] = "A111={},'532211'={}".format(A111,moneySum(person_zy,"532211"))
                    dict['核实内容'] = "A111=4、5、7，为何有个人缴纳的医疗保险支出，请查改"
                    insert_to_pd(dict)

            if A111 == 7 and code_match(person_zy,"240511") == 1:
                dict['code'] = "A111={},'240511'={}".format(A111,moneySum(person_zy,"240511"))
                dict['核实内容'] = "此人A111=7,为何有报销医疗费用收入,请查改！"
                insert_to_pd(dict)

            if A205 == 2 or A205 == 3 or A205 == 4:
                if code_match(person_zy, "210111") == 1 and moneySum(person_zy, "210111") < 2300:
                    dict['code'] = "A205={},'210111'={}".format(A205,moneySum(person_zy,"210111"))
                    dict['核实内容'] = "A205为公职、事业、国企员工，按月发放的工资低于2300元，请核实！"
                    insert_to_pd(dict)

            if 1 <= A_member['A108'] <= 7 or A_member['A109'] != 1:
                if code_match(person_zy, "533111") == 1:
                    dict['code'] = "A108={},A109={},'533111'={}".format(A_member['A108'],A_member['A109'],moneySum(person_zy,"533111"))
                    dict['核实内容'] = "A卷该人身份（a108、a109）与记账代码533111不符，请核实！"
                    insert_to_pd(dict)

            if (1 <= A_member['A108'] <= 7 or A_member['A109'] != '2') and code_match(person_zy, "533211") == 1:
                dict['code'] = "A108={},A109={},'12'={}".format(A_member['A108'],A_member['A109'],moneySum(person_zy,"533211"))
                dict['核实内容'] = "A卷该人身份（a108、a109）与记账代码533211不符。请核实！"
                insert_to_pd(dict)

            if A205 != 1 and A_member['A100'] == "77":
                dict['code'] = "A205={},A100={},".format(A205,A_member['A100'])
                dict['核实内容'] = "月度记账人代码77，发生非农经营收入的人应为雇主（a205=1）"
                insert_to_pd(dict)

            if A204 == 2 or pd.isnull(A_member['A204']) == False:
                if code_match(person_zy, "531111") == 1 or code_match(person_zy, "532311") == 1 or code_match(\
                        person_zy, "532411") == 1 or code_match(person_zy, "532911") == 1:
                    dict['code'] = "A204={},'12'={}".format(A204,moneySum(person_zy,"531111"),moneySum(person_zy,'532311'),moneySum(person_zy,'532411'),moneySum(person_zy,'532911'))
                    dict['核实内容'] = "本季度未从业过（A204），为何发生个税和社会保障支出？请核实并注明原因"
                    insert_to_pd(dict)

            if A202 != 3 and code_match(person_zy, "240121") == 1:
                dict['code'] = "A202={},'240121'={}".format(A202,moneySum(person_zy,'240121'))
                dict['核实内容'] = "该人为城乡居保收入（240121），为何A202不等于3？请核实并注明原因！"
                insert_to_pd(dict)

            if code_match(person_zy, "210291") == 1:
                dict['code'] = "'210291'={}".format(moneySum(person_zy,'210291'))
                dict['核实内容'] = "确有其他劳动所得？请核实并注明具体情况"
                insert_to_pd(dict)

            if code_match(person_zy, "230911") == 1:
                dict['code'] = "'230911'={}".format(moneySum(person_zy, '230911'))
                dict['核实内容'] = "确有其他财产性收入？请注明具体收入内容"
                insert_to_pd(dict)

            if code_match(person_zy, "240891") == 1:
                dict['code'] = "'240891'={}".format(moneySum(person_zy, '240891'))
                dict['核实内容'] = "确有其他转移性收入？请注明具体收入内容"
                insert_to_pd(dict)

            m1 = moneySum(person_zy, "539111")
            m2 = moneySum(person_zy, "539211")
            m3 = moneySum(person_zy,"539911")
            if m1 > 500 or m2 > 500 or m3 > 500:
                dict['code'] = "'539111'={},'539211'={},'539911'={}".format(m1,m2,m3)
                dict['核实内容'] = "确有较大金额的其他经常转移支出？(539***)请核实并注明具体支出内容"
                insert_to_pd(dict)

            if code_match(person_zy, "522111") == 1:
                dict['code'] = "'522111'={}".format(moneySum(person_zy, '522111'))
                dict['核实内容'] = "确有其他财产性支出？请注明具体支出内容"
                insert_to_pd(dict)

            for row in person_zy.iterrows():
                person_row = row[1]
                c = int(person_row['CODE'])
                money = float(person_row['MONEY'])
                if 561011 >= c >= 111011 and c != 260111 and c != 560111:
                    if c > 399999 or c < 300000:
                        if money > 50000:
                            dict['code'] = "code={}".format(c)
                            dict['核实内容'] = "单笔5万元以上的大额数据，请核实并注明情况！"
                        else:
                            if money > 20000:
                                dict['code'] = "code={}".format(c)
                                dict['核实内容'] = "消费单笔2万元以上的大额数据，请核实并注明情况！"
                                insert_to_pd(dict)

                if person_row['note4'] == 0 and (pd.isnull(person_row['CODE']) == True or c == 0):
                    dict['code'] = "code={},note4={}".format(c,person_row['note4'])
                    dict['核实内容'] = "此条账页的编码（code）,不在标准编码库中，漏填？编码错？导入导出错？请核实！"
                    insert_to_pd(dict)

                if person_row['markyc'] == 2:
                    dict['code'] = "code={},markyc={}".format(c,person_row['markyc'])
                    dict['核实内容'] = "此条账页的编码（code）为异常编码（这些编码上海应不存在），确有？编码错？导入导出错？请核实！"
                    insert_to_pd(dict)

                if c != 641111 and c != 651111:
                    if person_row['note11'] == 1 and person_row['AMOUNT'] == 0:
                        dict['code'] = "code={},note11={},amount={}".format(c,person_row['note11'],person_row['AMOUNT'])
                        dict['核实内容'] = "此条账页应有数据，却漏填数据。请核实！"
                        insert_to_pd(dict)
                    if person_row['note22'] == 1 and person_row['MONEY'] == 0:
                        dict['code'] = "code={},note22={},money={}".format(c, person_row['note22'],person_row['MONEY'])
                        dict['核实内容'] = "此条账页应填金额，却漏填金额。请核实！"
                        insert_to_pd(dict)

                if person_row['note11'] == 0 and person_row['AMOUNT'] != 0:
                    dict['code'] = "code={},note11={},amount={}".format(c, person_row['note11'], person_row['AMOUNT'])
                    dict['核实内容'] = "此条账页不应填数据，却填了数据。请核实！"
                    insert_to_pd(dict)

                if person_row['note22'] == 0 and person_row['MONEY'] != 0:
                    dict['code'] = "code={},note22={},money={}".format(c, person_row['note22'], person_row['MONEY'])
                    dict['核实内容'] = "此条账页不应填金额，却填了金额。请核实！"
                    insert_to_pd(dict)

                if person_row['note33'] == 1 and person_row['note4'] == 1:
                    dict['code'] = "code={},note33={},note4={}".format(c, person_row['note33'], person_row['note4'])
                    dict['核实内容'] = "此条账页应填note4，但是漏填note4内容。请核实！"
                    insert_to_pd(dict)

                if person_row['note33'] == 0 and person_row['note4'] != 1:
                    dict['code'] = "code={},note33={},note4={}".format(c, person_row['note33'], person_row['note4'])
                    dict['核实内容'] = "此条账页不应填note4，却填了note4内容。请核实！"
                    insert_to_pd(dict)

                p = int(person_row['PERSON'])
                if p < 1 or p > 20 and person_row['note44'] == 1:
                    dict['code'] = "code={},person={},note44={}".format(c, p,person_row['note44'])
                    dict['核实内容'] = "此条账页应填人代码却漏填或填错。请核实！"
                    insert_to_pd(dict)

                # if c != 0 and person_row['note44'] == 0 and p != 99:
                #     t = code_match(person_row, "3") + code_match(person_row, "52") + code_match(person_row, "54") + code_match(person_row,"55") + \
                #         code_match(person_row, "56") + code_match(person_row, "534111") + code_match(person_row, "539") + code_match(person_row, "23") \
                #         + code_match(person_row, "2402") + code_match(person_row, "2403") + code_match(person_row,"2404") + code_match(person_row,"240711") + \
                #         code_match(person_row, "25") + code_match(person_row, "26") + code_match(person_row, "240821") + code_match(person_row, "240831") + \
                #         code_match(person_row, "240841") + code_match(person_row, "240851") + code_match(person_row,"240861") + code_match(index, "240891")
                #     if t > 0:
                #         print("此条账页人代码应为99，却填为其他值。请核实！")

            m1 = moneySum(person_zy, "240611")
            m2 = moneySum(person_zy, "21")
            if m1 > 0 and m2 > 0:
                dict['code'] = "'240611'={},'21'={}".format(m1,m2)
                dict['核实内容'] = "此人既有工资性收入又有寄带回收入。请核实！"
                insert_to_pd(dict)

            m1 = moneySum(person_zy, "260111")
            m2 = moneySum(person_zy, "230111")
            if m1 >= 10000 and m2 == 0:
                dict['code'] = "'260111'={},'230111'={}".format(m1, m2)
                dict['核实内容'] = "提取储蓄款万元以上，应有利息收入。请核实！"
                insert_to_pd(dict)

            if code_match(person_zy, "240131") == 1:
                dict['code'] = "'240131'={}".format(moneySum(person_zy,"240131"))
                dict['核实内容'] = "城乡养老保险已经合并成城乡居保，为何发生新型农村社会养老保险收入（240131）请核实！"
                insert_to_pd(dict)

            if num_same_zy(person_zy, "532111") > 1:
                dict['核实内容'] = "同一人单月个人缴纳的社会保险支出（532111)出现多笔相同金额账页数据"
                insert_to_pd(dict)

            if num_same_zy(person_zy, "532211") > 1:
                dict['核实内容'] = "同一人单月个人缴纳的社会保险支出（532211)出现多笔相同金额账页数据"
                insert_to_pd(dict)

            if num_same_zy(person_zy, "532311") > 1:
                # print("同一个人单月缴纳的社会保障支出出现多笔账页数据？请核实并注明原因")
                dict['核实内容'] = "同一人单月个人缴纳的社会保险支出（532311)出现多笔相同金额账页数据"
                insert_to_pd(dict)

            if num_same_zy(person_zy, "532411") > 1:
                # print("同一个人单月缴纳的社会保障支出出现多笔账页数据？请核实并注明原因")
                dict['核实内容'] = "同一人单月个人缴纳的社会保险支出（532411)出现多笔相同金额账页数据"
                insert_to_pd(dict)

            #qd 月度数据
            # if Table(one_zhuhu,"M217") == 1:
            #     print("该户账页数据没有录入。")


            # A问卷
            if Table(one_zhuhu,"M217") == 1 and A201 != 3 and A202 == 6:
                dict['code'] = "M217={},A201={},A202={}".format(Table(one_zhuhu,"m217"),A201,A202)
                dict['核实内容'] = "单位离退休人员，为何没有参加任何养老保险A202=6，请核实并注明！"
                insert_to_pd(dict)

            if A_member['A108'] == 6:
                dict['code'] = "A108={}".format(A_member['A108'])
                dict['核实内容'] = "A108=6,户口登记地在省外，应直接填写省代码！"
                insert_to_pd(dict)

            if A_member['A108'] == 7:
                dict['code'] = "A108={}".format(A_member['A108'])
                dict['核实内容'] = "A108=7,户口登记地为其他？请核实！"
                insert_to_pd(dict)

            a1 = A_member['A111']
            a2 = A_member['A202']
            pk1 = (a1 == 1) and (a2 != 1)
            pk2 = (a1 == 2) and (a2 != 2)
            pk3 = (a1 == 3) and (a2 != 3)
            pk4 = (a1 != 1) and (a2 == 1)
            pk5 = (a1 != 2) and (a2 == 2)
            pk6 = (a1 != 3) and (a2 == 3)
            if pk1 or pk2 or pk3 or pk4 or pk5 or pk6:
                dict['code'] = "A111={},A202={}".format(A111,A202)
                dict['核实内容'] = "A111医疗保险种类与A202养老保险不一致，请核实！"
                insert_to_pd(dict)

            if A_member['A106'] >= 16 and A_member['A112'] == 3 and A_member['A203'] == 2 and A111 == 4:
                dict['code'] = "A106={},A112={},A203={},A111={}".format(A_member['A106'],A_member['A112'],A_member['A203'],A111)
                dict['核实内容'] = "A111确实是公费医疗？请核实并注明具体情况!"
                insert_to_pd(dict)

            if len(str(A_member['A108'])) > 1 and A_member['A204'] == 1:
                if A_member['A111'] == 7:
                    dict['code'] = "A108={},A204={},A111={}".format(A_member['A108'],A204,A111)
                    dict['核实内容'] = "外来务工人员，未参加任何医疗保险A111=7，请核实并注明具体情况!"
                    insert_to_pd(dict)

            if A202 == 6:
                dict['code'] = "A202={}".format(A202)
                dict['核实内容'] = "外来务工人员，未参加任何养老保险A202=6，请核实并注明具体情况！"
                insert_to_pd(dict)

            if A204 == 1 and A205 == 6 and A208 > 0:
                m = moneySum(person_zy, "12")
                if m == 0:
                    dict['code'] = "A204={},A205={},A208={},'12'={}".format(A204,A205,A208,m)
                    dict['核实内容'] = "此人漏填农业自营收入（编码12打头）。请核实！"
                    insert_to_pd(dict)

        #zycheck about tableB and zy
        for rowB in B.iterrows():
            B_family = rowB[1]
            # family_SID = B_family['SID']
            # family_zy = zy_family[zy_family['SID'] == family_SID]
            # print(person_SID,person)
            if B_family['B130'] == 0 and B_family['B133'] == 0 and code_match(zy_family,"2305") == 1:
                dict['code'] = "B130={},B133={},'2305'={}".format(B_family['B130'],B_family['B133'],moneySum(zy_family,"2305"))
                dict['核实内容'] = "多填出租房屋收入。请核实！"
                insert_to_pd(dict)

            if B_family['B201'] == 0 and B_family['B202'] == 0 and B_family['B203'] == 0:
                # if per_row['CODE'] == "351311" or per_row['CODE'] == "541111":
                m1 = moneySum(zy_family,"351311")
                m2 = moneySum(zy_family,"541111")
                if m1 + m2 > 0:
                    dict['code'] = "B201={},B202={},B203={},'351311'={},'541111'={}".format(B_family['B201'], B_family['B202'],B_family['B203'],m1,m2)
                    dict['核实内容'] = "B卷中没有家用汽车、摩托车、燃油助力车，为何发生燃料或机动车保险费？请核实！"
                    insert_to_pd(dict)

            if B_family['B104'] != 2:
                # if per_row['CODE'] == "331211" and per_row['MONEY'] > '0':
                m = moneySum(zy_family,"331211")
                if m > 0:
                    dict['code'] = "B104={},'331211'={}".format(B_family['B104'],m)
                    dict['核实内容'] = "B卷中房屋来源不是租赁私房，为何发生租赁私房房租费用？请核实并注明原因！"
                    insert_to_pd(dict)

            if B_family['B104'] != 1:
                # if per_row['CODE'] == "331111" and per_row['MONEY'] > '0':
                m = moneySum(zy_family,"331111")
                if m > 0:
                    dict['code'] = "B104={},'331111'={}".format(B_family['B104'],m)
                    dict['核实内容'] = "B卷中房屋来源不是租赁公房，为何发生租赁公房房租费用？请核实并注明原因！"
                    insert_to_pd(dict)

            if B_family['B208'] == 0 and code_match(zy_family,"362351") == 1:
                m = moneySum(zy_family,"362351")
                dict['code'] = "B208={},'362351'={}".format(B_family['B208'],m)
                dict['核实内容'] = "Ｂ卷中没有接入有线电视网，为何发生有线电视费用？请核实!"
                insert_to_pd(dict)

            m1 = moneySum(zy_family, "521111")
            m2 = moneySum(zy_family, "560611")
            if B_family['B126'] == 2:
                if m1 > 0:
                    dict['code'] = "B126={},'521111'={}".format(B_family['B126'], m1)
                    dict['核实内容'] = "B卷B126未在还款，为何发生住房贷款利息支出？请核实并注明原因！"
                    insert_to_pd(dict)
                if m2 > 0:
                    dict['code'] = "B126={},'560611'={}".format(B_family['B126'], m2)
                    dict['核实内容'] = "B卷中B126未在还款，为何发生归还住房贷款支出？请核实并注明原因！"
                    insert_to_pd(dict)

            if B_family['B126'] == 1:
                if m1 == 0:
                    dict['code'] = "B126={},'521111'={}".format(B_family['B126'], m1)
                    dict['核实内容'] = "Ｂ卷中B126在还款，为何未发生住房贷款利息支出？漏记或人码有误或B126有误？请核实并注明原因"
                    insert_to_pd(dict)
                if m2 == 0:
                    dict['code'] = "B126={},'560611'={}".format(B_family['B126'], m2)
                    dict['核实内容'] = "Ｂ卷中B126在还款，为何未发生归还住房贷款支出？漏记或人码有误或B126有误？请核实并注明原因！"
                    insert_to_pd(dict)

            month = Table(zy_family,"MONTH")
            if B_family['B116'] == 5:
                m = moneySum(zy_family,"333306")
                if m == 0 and month == 2 or month == 5 or month == 8 or month == 11:
                    dict['code'] = "B116={},month={},'333306'={}".format(B_family['B116'],month, m)
                    dict['核实内容'] = "B卷中B116=5，本月无管道煤气费用支出。请核实！"
                    insert_to_pd(dict)

            if B_family['B116'] == 6:
                m = moneySum(zy_family,"333305")
                if m == 0 and month == 2 or month == 5 or month == 8 or month == 11:
                    dict['code'] = "B116={},month={},'333305'={}".format(B_family['B116'], month, m)
                    dict['核实内容'] = "B卷中B116=6，本月无管道天然气费用支出。请核实！"
                    insert_to_pd(dict)

            if B_family['B116'] == 3:
                m = moneySum(zy_family,"333308")
                if m == 0 and month == 2 or month == 5 or month == 8 or month == 11:
                    dict['code'] = "B116={},month={},'333305'={}".format(B_family['B116'], month, m)
                    dict['核实内容'] = "B卷中B116=3，本月无罐装液化石油气费用支出。请核实！"
                    insert_to_pd(dict)

            if B_family['B201'] != 0 or B_family['B202'] != 0 or B_family['B203'] != 0:
                if code_match(zy_family,"251311") == 1 or code_match(zy_family,"541111") == 1:
                    dict['code'] = "B201={},202={},B203={},'251311'={},'541111'={}".format(B_family['B201'],B_family['B202'],B_family['B203'],moneySum(zy_family,"251311"),moneySum(zy_family,"541111"))
                    dict['核实内容'] = "有汽车或摩托车，无燃料及维修费用支出。请核实！"
                    insert_to_pd(dict)

            # if B_family['B201'] == 0 and B_family['B202'] == 0 and B_family['B203'] == 0:
            #     if per_row['CODE'] == "351311" or per_row['CODE'] == "541111":
            #         print("B卷中没有家用汽车、摩托车、燃油助力车，为何发生燃料或机动车保险费？请核实！")

            if B_family['B104'] != 2 and moneySum(zy_family, "333211") == 0:
                dict['code'] = "B104={},'333211'={}".format(B_family['B104'],moneySum(zy_family,'333211'))
                dict['核实内容'] = "本月无电费支出。请核实！"
                insert_to_pd(dict)

            if B_family['B217'] == 0 and B_family['B219'] == 0 and moneySum(zy_family,"352231") != 0:
                dict['code'] = "B127={},B129={},'352231'={}".format(B_family['B217'],B_family['B219'], moneySum(zy_family, '352231'))
                dict['核实内容'] = "B卷中手机与电脑均无接入互联网，为何发生上网费用？"
                insert_to_pd(dict)

        # zyselfcheck
        if 310101 <= int(Table(zy_family,"COUN")) <= 310110:
            if code_match(zy_family,"1") == 1:
                dict['核实内容'] = "此户为市中心户，却有1打头的农业账页编码，请核实！"
                insert_to_pd(dict)

        if code_match(zy_family,"333307") == 1:
            dict['code'] = "code='333307'"
            dict['核实内容'] = "此户本月使用过管道液化石油气？请核实！"
            insert_to_pd(dict)

    return zy_independent_result

# 打开csv文件 返回DataFrame对象
def read_csv(path):
    with open(path, 'r') as f:
        file = pd.read_csv(f, header=0)
    return file

if __name__ == '__main__':
    A_path = u"D:/研一/审核程序/src/输入文件夹/A310151.18.csv"
    B_path = u"D:/研一/审核程序/src/输入文件夹/B310151.18.csv"
    zy_path = u"D:/研一/项目/Auditing/输入文件夹/06账页310151.1806.csv"
    zhuhu_path = u"D:/研一/审核程序/src/输入文件夹/住户样本310151.18.csv"
    xiaoqu_path = u"D:/研一/审核程序/src/输入文件夹/小区名录310151.18.csv"
    codes_path = "D:\研一\项目\CheckProgram\Auditing\输入文件夹\编码手册.csv"
    # fp2 = open(codes_path)
    codes = read_csv(codes_path)

    TableA = read_csv(A_path)
    TableB = read_csv(B_path)
    zy = read_csv(zy_path)
    xiaoqu = read_csv(xiaoqu_path)
    zhuhu = read_csv(zhuhu_path)

    head = {'year': [], 'task': [], 'month': [], 'coun':[],'scode': [], 'sid': [], 'person': [], 'name': [], 'code': [],
            '核实内容': [], 'townname': [], 'vname': []}
    result = pd.DataFrame(head)
    result = result[['year', 'month', 'task','coun', 'scode', 'sid', 'person', 'name', 'code', '核实内容', 'townname', 'vname']]  # , 'haddr']]
    IndependentCheck(TableA,TableB,zy,zhuhu,xiaoqu,codes,result)
    zy_independent_result.to_excel('./independent_result.xlsx',encoding="utf-8",index=False,sheet_name='Sheet')
