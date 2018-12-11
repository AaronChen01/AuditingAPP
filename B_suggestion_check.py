# ********************************
# *   全国住户生活状况调查季报   *
# *    问卷B审核公式（必要性）   *
# *        2015年08月26日        *
# ********************************
from decimal import Decimal

import pandas as pd
import myLogging as mylogger
import datetime

# Year = datetime.datetime.now().year
# Month = datetime.datetime.now().month
B_suggestion_result = pd.DataFrame()

def insert_to_pd(data):
    global B_suggestion_result
    B_suggestion_result = B_suggestion_result.append(data, ignore_index=True)


def read_csv(path):
    with open(path, 'r') as f:
        file = pd.read_csv(f, header=0)
    return file


def Table(table, code):
    t = table[code]
    # print("tabledata:",t)
    if t.empty == False:
        if pd.isnull(t.values[0]) == True:
            return 0
        if type(t.values[0]) == type("str"):
            # print("字符串类型：",type(t.values[0]))
            return int(t.values[ 0])
        return t.values[0]
    else:
        return 0


def B_suggestion_check(tableB, zhuhu, zhuzhai,xiaoqu,result_table):
    mylogger.logger.debug("B_necessity_check init..")
    global B_suggestion_result
    B_suggestion_result.drop(B_suggestion_result.index, inplace=True)
    B_suggestion_result = result_table

    B, M = 92, 993
    E = 95
    # if M_91 == M_94:  #//开户拒访：开户时间和拒访时间相同
    # if table['M91'] == table['M94']:
    # nextHousehold
    # result = open(r'D:\研一\审核程序\src\审核结果输出\B_suggestion_Check_result.txt', 'w')

    # B1部分    住房基本情况
    # B1.1    期末现住房基本情况
    # result.write(tableB['SID']+': ')
    for row in tableB.iterrows():
        single_row = row[1]
        # zhuzhai对应M1,zhuhu对应M2
        family_sid = single_row['SID']
        one_zhuhu = zhuhu[zhuhu['HHID'] == family_sid]
        one_zhuzhai = zhuzhai[zhuzhai['HID'] == family_sid[:-2]]
        # Year = Table(single_row, "YEAR")
        Year = int(float(single_row['YEAR']))
        print(Year)
        scode = single_row['SCODE']
        qu_vid = family_sid[0:15]
        qu = xiaoqu[xiaoqu['VID'] == qu_vid]
        townname = qu['TOWNNAME'].values[0]
        vname = qu['VNAME'].values[0]
        dict = {'year': str(single_row['YEAR']), 'sid': family_sid, 'scode': scode, 'townname': townname, 'vname': vname}

        if single_row['B101'] == 1:
            # 逻辑审核
            if single_row['B103'] == 4 and single_row['B102'] != 2 and single_row['B102'] != 7 and single_row['B102'] != 8:
                dict['code'] = "B101={},B102={},B103={}".format(single_row['B101'], single_row['B102'],single_row['B103'])
                dict['提示内容'] = "竹草土坯结构的房屋是楼房或单元房吗？请核实"
                insert_to_pd(dict)

            # B3部分 补充资料3：家庭或家庭成员合伙、参股或独立控股公司（企业）
            # if (single_row['B101'])
            if single_row['B242'] < 0 or single_row['B242'] > 5000:
                dict['code'] = "B101={},B242={}".format(single_row['B101'], single_row['B242'])
                dict['提示内容'] = "公司（企业）税后净利润可能偏高，请核实"
                insert_to_pd(dict)

            if single_row['B244'] < 0 or single_row['B244'] > 500:
                dict['code'] = "B101={},B244={}".format(single_row['B101'],single_row['B244'])
                dict['提示内容'] = "属于本住户或住户成员名下股份的公司（企业）税后净利润可能偏高，请核实"
                insert_to_pd(dict)

        # df = tableM[single_row['SID'][:-2] == tableM['SID']]
        # for index, Modi in df.iterrows():
            # if single_row['SID'][:-2] == Modi['SID']:
        if Table(one_zhuzhai, "M101") == 1 and single_row['B101'] == 1:
            # B1.2自有现住房情况
            # print(single_row['SID'],one_zhuzhai["M101"])
            if single_row['B104'] >= 3 and single_row['B104'] <= 8:
                # if single_row['B117'] < 1949 or single_row['B117'] > Year * 100 + Month:
                if single_row['B117'] < 1949 or single_row['B117'] > Year:
                    dict['code'] = "B104={},B117={}".format(single_row['B104'], single_row['B117'])
                    dict['提示内容'] = "B117自有现住房建筑年份越界"
                    insert_to_pd(dict)

                if single_row['B118'] / 100 > single_row['B121']:
                    dict['code'] = "B104={},B118={},B121={}".format(single_row['B104'], single_row['B118'],single_row['B121'])
                    dict['提示内容'] = "自有现住房现市场价是原购建价的100倍以上，请核实"
                    insert_to_pd(dict)

                if single_row['B103'] == 4:
                    if single_row['B117'] < 1970:
                        dict['code'] = "B104={},B103={},B117={}".format(single_row['B104'], single_row['B103'],single_row['B117'])
                        dict['提示内容'] = "请核实竹草土坯结构房屋的建筑年份"
                        insert_to_pd(dict)

                    if single_row['B118'] > 10:
                        dict['code'] = "B104={},B103={},B118={}".format(single_row['B104'], single_row['B103'],single_row['B118'])
                        dict['提示内容'] = "请核实竹草土坯结构房屋的市场价值"
                        insert_to_pd(dict)

                if single_row['B105'] != 0:
                    if single_row['B118'] / single_row['B105'] <= 0.01 or single_row['B118'] / single_row['B105'] >= 8:
                        dict['code'] = "B104={},B118={},B105={},B118/B105={}".format(single_row['B104'], single_row['B118'],single_row['B105'],single_row['B118']/single_row['B105'])
                        dict['提示内容'] = "B118自有现住房单价越界,请核实"
                        insert_to_pd(dict)

            # B1.3租赁房实际月租金
            data = single_row['B127']
            dict['code'] = "B104={},M101={},M205={},B127={}".format(single_row['B104'], Table(one_zhuzhai, "M101"),Table(one_zhuhu, "M205"), single_row['B127'])
            if single_row['B104'] == 1 or single_row['B104'] == 2:
                if Table(one_zhuzhai, "M101") < 2 and Table(one_zhuhu, "M205") != 4:
                    if 10 > data > 0 or data >= 999:
                        dict['提示内容'] = "B127租赁公房实际月租金越界"
                        insert_to_pd(dict)

                    if 100 > data > 0 or data >= 9999:
                        dict['提示内容'] = "B127租赁公房实际月租金越界"
                        insert_to_pd(dict)

            # B1.4期内拥有其他房屋情况
            if single_row['B131'] > 0 and single_row['B133'] < 10 or single_row['B133'] >= 9999:
                dict['code'] = "B131={},B133={}".format(single_row['B131'],single_row['B133'])
                dict['提示内容'] = "B133出租商用建筑物月租金越界"
                insert_to_pd(dict)
            # 出租屋单间越界
            # print(single_row['SID'],single_row["B128"],single_row['B129'])
            if pd.isnull(single_row['B128']) == False and single_row['B128'] > 0:
                if single_row['B129'] / single_row['B128'] <= 0.1 or single_row['B129'] / single_row['B128'] >= 8:
                    dict['code'] = "B129={},B128={},B129/B128={}".format(single_row['B129'], single_row['B128'],single_row['B129']/single_row['B128'])
                    dict['提示内容'] = "出租住房单价越界,请核实"
                    insert_to_pd(dict)

            if single_row['B131'] > 0:
                if single_row['B132'] / single_row['B131'] <= 0.1 or single_row['B132'] / single_row['B131'] >= 8:
                    dict['code'] = "B132={},B131={},B132/B131={}".format(single_row['B132'], single_row['B131'],single_row['B132']/single_row['B131'])
                    dict['提示内容'] = "出租商用建筑物单价越界，请核实"
                    insert_to_pd(dict)

            if single_row['B134'] > 0:
                if single_row['B135'] / single_row['B134'] <= 0.1 or single_row['B135'] / single_row['B134'] >= 8:
                    dict['code'] = "B135={},B134={},B135/B134={}".format(single_row['B135'], single_row['B134'],single_row['B135']/single_row['B134'])
                    dict['提示内容'] = "偶尔居住房单价越界，请核实"
                    insert_to_pd(dict)

            if single_row['B136'] > 0:
                if single_row['B137'] / single_row['B136'] <= 0.1 or single_row['B137'] / single_row['B136'] >= 8:
                    dict['code'] = "B137={},B136={},B137/B136={}".format(single_row['B137'], single_row['B136'],single_row['B137'] / single_row['B136'])
                    dict['提示内容'] = "空宅或其他用途住房单价越界,请核实"
                    insert_to_pd(dict)

            # B1.5新购住房情况审核
            if 4 <= single_row['B104'] <= 7 and single_row['B120'] <= 2019:
                if single_row['B139'] < 0 or single_row['B139'] >= 999:
                    dict['code'] = "B104={},B120={},B139={}".format(single_row['B104'], single_row['B120'],single_row['B139'])
                    dict['提示内容'] = "新购住房总金额越界"
                    insert_to_pd(dict)

                if single_row['B138'] != 0:
                    if single_row['B139'] / single_row['B138'] <= 0.1 or single_row['B138'] / single_row['B137'] >= 8:
                        dict['code'] = "B137={},B138={},B139={},B139/B138={},B138/B137={}".format(single_row['B137'], single_row['B138'],single_row['B139'],single_row['B139'] / single_row['B138'],single_row['B137'],single_row['B138']/single_row['B137'])
                        dict['提示内容'] = "新购住房单价越界,请核实"
                        insert_to_pd(dict)

            # B1.6新建住房情况审核
            if single_row['B104'] == 3 and single_row['B120'] == Year:
                if single_row['B144'] != 0:
                    if single_row['B145'] < 0.1 or single_row['B145'] >= 999:
                        dict['code'] = "B104={},B120={},B144={},B145={}".format(single_row['B104'], single_row['B120'],single_row['B144'],single_row['B145'])
                        dict['提示内容'] = "新建住房总费用越界"
                        insert_to_pd(dict)

                    if single_row['B145'] / single_row['B144'] <= 0.01 or single_row['B145'] / single_row['B144'] >= 3:
                        dict['code'] = "B104={},B120={},B144={},B145={},B144/B145={}".format(single_row['B104'], single_row['B120'],single_row['B144'], single_row['B145'],single_row['B144']/single_row['B145'])
                        dict['提示内容'] = "新建住房单价越界，请核实"
                        insert_to_pd(dict)

                if single_row['B145'] < 0.5 or single_row['B145'] >= 999:
                    dict['code'] = "B104={},B120={},B145={}".format(single_row['B104'], single_row['B120'],single_row['B145'])
                    dict['提示内容'] = "B145购（建）房总金额越界"
                    insert_to_pd(dict)

            # B1.7期内住房大修或装修费用
            if single_row['B150'] > 99:
                dict['code'] = "B150={}".format(single_row['B150'])
                dict['提示内容'] = "住房大修或专修费用越界"
                # break

        # B3部分 年末粮食结存
        if single_row['TASK'] == 7 and single_row['B101'] == 1:
            if single_row['B230'] + single_row['B231'] + single_row['B232'] + single_row['B233'] + single_row['B234'] + \
                    single_row['B235'] + single_row['B236'] + single_row['B237'] < 0:
                dict['提示内容'] = "没有粮食结存，请核实"


            # df2 = tableE[single_row['SID'] == tableE['SID']]
            # for index2, kaihu in df2.iterrows():
            #     # if kaihu['SID'] == single_row['SID']:
            #     if kaihu['E113'] > 0:
            #         if single_row['B230'] + single_row['B231'] <= 0:
            #             result.write('有种植小麦，但无小麦或面粉结存，请核实')
            #     if kaihu['E114'] > 0:
            #         if single_row['B232'] + single_row['B233'] <= 0:
            #             result.write('有种植水稻，但无稻谷或大米结存，请核实')
            #     if kaihu['E115'] > 0:
            #         if single_row['B234'] + single_row['B235'] <= 0:
            #             result.write('有种植玉米。但无玉米或玉米面结存，请审核')
            #     if kaihu['E116'] + kaihu['E117'] > 0:
            #         if single_row['B236'] + single_row['B237'] <= 0:
            #             result.write('有种植大豆或薯类，但无其他原粮或加工粮结存，请审核')

    return B_suggestion_result


if __name__ == "__main__":
    B_path = "D:\研一\审核程序\src\输入文件夹\B310151.18.csv"
    tableB = read_csv(B_path)
    zhuhu_path = u"\研一\审核程序\src\输入文件夹\住户样本310151.18.csv"
    zhuzhai_path = u"\研一\审核程序\src\输入文件夹\住宅名录310151.18.csv"
    xiaoqu_path = u"D:\研一\项目\CheckProgram\Auditing\输入文件夹\小区名录310151.18.csv"
    zhuzhai = read_csv(zhuzhai_path)
    zhuhu = read_csv(zhuhu_path)
    zhuzhai = read_csv(zhuzhai_path)
    zhuhu = read_csv(zhuhu_path)
    xiaoqu = read_csv(xiaoqu_path)
    B_suggestion_data = {'year': [], 'sid': [], 'scode': [], 'code': [], '提示内容': [], 'townname': [], 'vname': []}
    B_suggestion_result = pd.DataFrame(B_suggestion_data)
    B_suggestion_result = B_suggestion_result[['year', 'sid', 'scode', 'code', '提示内容', 'townname', 'vname']]
    B_suggestion_check(tableB,zhuhu,zhuzhai,xiaoqu,B_suggestion_result)
    B_suggestion_result.to_csv('B_suggestion_result.csv',encoding='utf_8_sig')

