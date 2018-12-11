# ********************************
# *   全国住户生活状况调查季报   *
# *    问卷B审核公式（必要性）   *
# *        2015年08月26日        *
# ********************************
import pandas as pd
import datetime
import myLogging as mylogger
from typing import Any

# Year = datetime.datetime.now().year
# Month = datetime.datetime.now().month
B_necessity_result = pd.DataFrame()

def insert_to_pd(data):
    global B_necessity_result
    B_necessity_result = B_necessity_result.append(data, ignore_index=True)


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
            return int(t.values[0])
        return t.values[0]
    else:
        return 0


def B_necessity_check(tableB,zhuhu,zhuzhai,xiaoqu,result_table):
    mylogger.logger.debug("B_necessity_check init..")
    B,M = 92,993
    E = 95
    global B_necessity_result
    B_necessity_result.drop( B_necessity_result.index, inplace=True)
    B_necessity_result = result_table
    # B1部分    住房基本情况
    #B1.1    期末现住房基本情况
    #超界错误。b101 - b116重写，0825lw
    #B101 ?: "B101填报错误"
    #if tableB['B101']:
    # result = open(r'D:\研一\审核程序\src\审核结果输出\B_necessity_CheckResult.txt', 'w')
    for row in tableB.iterrows():
        single_row = row[1]
        #zhuzhai对应M1，zhuhu对应M2
        family_sid = single_row['SID']
        one_zhuhu = zhuhu[zhuhu['HHID'] == family_sid]
        one_zhuzhai = zhuzhai[zhuzhai['HID'] == family_sid[:-2]]
        # Year = Table(single_row, "YEAR")
        Year = int(float(single_row['YEAR']))

        # print(Year,single_row['YEAR'])
        scode = single_row['SCODE']
        qu_vid = family_sid[0:15]
        # qu = xiaoqu[xiaoqu['VID'] == qu_vid]
        # townname = qu['TOWNNAME'].values[0]
        # vname = qu['VNAME'].values[0]
        qu = xiaoqu[xiaoqu['vID'] == qu_vid]
        townname = qu['townName'].values[0]
        vname = qu['vName'].values[0]
        dict = {'year':str(single_row['YEAR']),'sid':family_sid,'scode':scode,'townname':townname,'vname':vname}

        # result.write(single_row['SID']+":")
        # if pd.isnull(single_row['B101']) == False:
        if Table(one_zhuhu,'HHSTATUS') == 2:
            continue

        B101 = single_row['B101']
        if B101 != 0:
            # print('aaaa')
            if B101 < 1 or B101 > 4:
                dict['code'] = "B101={}".format(B101)
                dict['提示内容'] = "住宅类型越界，请填写（1-4）"
                insert_to_pd(dict)

            if single_row['B102'] < 1 or single_row['B102'] > 8:
                dict['code'] = "B101={},B102={}".format(B101,single_row['B102'])
                dict['提示内容'] = "本住宅的建筑样式越界，请填写（1-8）"
                insert_to_pd(dict)

            if single_row['B103'] < 1 or single_row['B103'] > 5:
                dict['code'] = "B101={},B103={}".format(B101,single_row['B103'])
                dict['提示内容'] = "主要建筑材料越界，请填写（1-5）"
                insert_to_pd(dict)

            if single_row['B104'] < 1 or single_row['B104'] > 11:
                dict['code'] = "B101={},B104={}".format(B101, single_row['B104'])
                dict['提示内容'] = "房屋来源越界，请填写（1-11）"
                insert_to_pd(dict)

            if single_row['B105'] <= 0 or single_row['B105'] > 999:
                dict['code'] = "B101={},B105={}".format(B101, single_row['B105'])
                dict['提示内容'] = "建筑面积填报越界，请核实"
                insert_to_pd(dict)

            if single_row['B106'] <1 or single_row['B106'] > 3:
                dict['code'] = "B101={},B106={}".format(B101, single_row['B106'])
                dict['提示内容'] = "住宅外道路路面情况越界，请填写（1-3）"
                insert_to_pd(dict)

            if single_row['B107'] < 1 or single_row['B107'] > 3:
                dict['code'] = "B101={},B107={}".format(B101, single_row['B107'])
                dict['提示内容'] = "住宅内是否有管道自来水越界，请填写（1-3）"
                insert_to_pd(dict)

            if single_row['B108'] < 1 or single_row['B108'] > 7:
                dict['code'] = "B101={},B108={}".format(B101, single_row['B108'])
                dict['提示内容'] = "主要饮用水来源越界，请填写（1-7）"
                insert_to_pd(dict)

            if single_row['B109'] < 1 or single_row['B109'] > 4:
                dict['code'] = "B101={},B109={}".format(B101, single_row['B109'])
                dict['提示内容'] = "获取饮用水存在的困难越界，请填写（1-4）"
                insert_to_pd(dict)

            if single_row['B110'] < 1 or single_row['B110'] > 5:
                dict['code'] = "B101={},B110={}".format(B101, single_row['B110'])
                dict['提示内容'] = "饮用水处理措施越界，请填写（1-5）"
                insert_to_pd(dict)

            if single_row['B111'] < 1 or single_row['B111'] > 5:
                dict['code'] = "B101={},B111={}".format(B101, single_row['B111'])
                dict['提示内容'] = "厕所类型越界，请填写（1-5）"
                insert_to_pd(dict)

            if single_row['B112'] < 1 or single_row['B112'] > 3:
                dict['code'] = "B101={},B112={}".format(B101, single_row['B112'])
                dict['提示内容'] = "厕所使用情况越界，请填写（1-3）"
                insert_to_pd(dict)

            if single_row['B113'] < 1 or single_row['B113'] > 4:
                dict['code'] = "B101={},B113={}".format(B101, single_row['B113'])
                dict['提示内容'] = "洗澡设施越界，请填写（1-4）"
                insert_to_pd(dict)

            if single_row['B114'] < 1 or single_row['B114'] > 3:
                dict['code'] = "B101={},B114={}".format(B101, single_row['B114'])
                dict['提示内容'] = "主要取暖设备状况越界，请填写（1-3）"
                insert_to_pd(dict)

            if single_row['B115'] < 1 or single_row['B115'] > 11:
                dict['code'] = "B101={},B115={}".format(B101, single_row['B115'])
                dict['提示内容'] = "主要取暖能源状况越界，请填写（1-11）"
                insert_to_pd(dict)

            if single_row['B116'] < 1 or single_row['B116'] > 11:
                dict['code'] = "B101={},B116={}".format(B101, single_row['B116'])
                dict['提示内容'] = "主要灶用能源状况越界，请填写（1-11）"
                insert_to_pd(dict)

            #逻辑审核
            if single_row['B102'] == 8:
                if single_row['B103'] == 1 or single_row['B103'] == 2:
                    dict['code'] = "B101={},B102={},B03={}".format(B101, single_row['B102'],single_row['B103'])
                    dict['提示内容'] = "居住空间样式为其他，建筑材料不应为钢混或砖混结构"
                    insert_to_pd(dict)

            if single_row['B107'] == 1 and single_row['B109'] == 1:
                dict['code'] = "B101={},B107={},B109={}".format(B101, single_row['B107'],single_row['B109'])
                dict['提示内容'] = "有自来水，单次取水时间却超过半小时？"
                insert_to_pd(dict)

            #跳转审核
            if 8 >= single_row['B104'] >= 3:
                sum = single_row['B117']+single_row['B118']+single_row['B119']+single_row['B120']+single_row['B121']+single_row['B122']+single_row['B123']+single_row['B124']+single_row['B125']+single_row['B126']
                if sum <= 0:
                    dict['code'] = "sum（B117-B126）={}".format(sum)
                    dict['提示内容'] = "现住房为自有房者应填写B117-B126"
                    insert_to_pd(dict)
            # if single_row['B104'] == 1 or single_row['B104'] == 2:
            #     if tableM['M101'] <= 1 and tableM['M205'] == 4:
            #         if single_row['B127'] <= 0:
            #             result.write('现住房为租赁房者应填写B127')
            if single_row['B104'] == 1 or single_row['B104'] == 2:
                if Table(one_zhuzhai, 'M101') <= 1 and Table(one_zhuhu,'M205') == 4:
                    if tableB['B127'] <= 0:
                        dict['code'] = "B104={},M101={},M205={},B127={}".format(single_row['B104'], Table(one_zhuzhai, 'M101'), Table(one_zhuhu,'M205'),single_row['B127'])
                        dict['提示内容'] = "现住房为租赁房者应填写B127"
                        insert_to_pd(dict)
        # print('ok')
        # df = tableM[single_row['SID'][:-2] == tableM['SID']]
        # for index, Modi in df.iterrows():
            # if single_row['SID'][:-2] == Modi['SID']:
        # if pd.isnull(single_row['B101']) == False:
            # 住家保姆、帮工或者集体居住户审核
        if B101 != 0:
            if Table(one_zhuhu,'M205') == 4:
                # value = single_row.apply(lambda : x['B117']+x['B118'], axis=1)
                # sum = 0
                # for i in range(117, 151):
                #     s = "%s%s" % ('B', str(i))
                #     sum += single_row[s]
                #     print(sum)

                if single_row['B117'] + single_row['B118'] + single_row['B119'] + single_row['B120'] + single_row['B121'] + single_row['B122'] \
                        + single_row['B123'] + single_row['B124'] + single_row['B125'] + single_row['B126'] + single_row['B127'] + single_row[
                    'B128'] \
                        + single_row['B129'] + single_row['B130'] + single_row['B131'] + single_row['B132'] + single_row['B133'] + single_row[
                    'B134'] \
                        + single_row['B135'] + single_row['B136'] + single_row['B137'] + single_row['B138'] + single_row['B139'] + single_row[
                    'B140'] \
                        + single_row['B141'] + single_row['B142'] + single_row['B143'] + single_row['B144'] + single_row['B145'] + single_row[
                    'B146'] \
                        + single_row['B147'] + single_row['B148'] + single_row['B149'] + single_row['B150'] > 0:
                    dict['提示内容'] = '住家保姆、帮工,不用填B117-B150'
                    insert_to_pd(dict)

                if B101 != 4:
                    dict['code'] = "B101={}".format(B101)
                    dict['提示内容'] = '住家保姆、帮工,B101要填4'
                    insert_to_pd(dict)
                if single_row['B104'] != 10:
                    dict['code'] = "B101={}".format(B101)
                    dict['提示内容'] = '住家保姆、帮工,B101要填10'
                    insert_to_pd(dict)
                if single_row['B112'] != 2:
                    dict['code'] = "B112={}".format(single_row['B112'])
                    dict['提示内容'] = '住家保姆、帮工,B112要填2'
                    insert_to_pd(dict)

        # print(single_row['SID'], " ", Table(one_zhuzhai, 'M101'))
        if Table(one_zhuzhai,'M101') == 1 and B101 != 0:
            # B1.2 自有现住房情况

            if 8 >= single_row['B104'] >= 3:
                if single_row['B118'] < 0.5 or single_row['B118'] >= 999:
                    dict['code'] = "B118={}".format(single_row['B118'])
                    dict['提示内容'] = 'B118自有现住房市场价'
                    insert_to_pd(dict)

                if single_row['B119'] < 100 or single_row['B119'] >= 9999:
                    dict['code'] = "B119={}".format(single_row['B119'])
                    dict['提示内容'] = 'B119同类住房的市场价月租金越界'
                    insert_to_pd(dict)

                if single_row['B120'] < 1949 or single_row['B120'] > Year:
                    dict['code'] = "B120={}".format(single_row['B120'])
                    dict['提示内容'] = 'B120现住房购(建)房时间越界'
                    insert_to_pd(dict)

                if single_row['B121'] < 0.5 or single_row['B121'] >= 999:
                    dict['code'] = "B121={}".format(single_row['B118'])
                    dict['提示内容'] = 'B121购(建)房总金额越界'
                    insert_to_pd(dict)

                if single_row['B122'] != 0:
                    if single_row['B122'] < 0.1 or single_row['B122'] >= 999:
                        dict['code'] = "B122={}".format(single_row['B122'])
                        dict['提示内容'] = 'B122购(建)房时借贷总额(不含利息)越界'
                        insert_to_pd(dict)

                    if single_row['B125'] < 1 or single_row['B125'] > 30:
                        dict['code'] = "B125={}".format(single_row['B125'])
                        dict['提示内容'] = 'B125借贷款还款总年限越界'
                        insert_to_pd(dict)

                if pd.isnull(single_row['B123']) == False:
                    if single_row['B123'] < 1 or single_row['B123'] >= 999:
                        dict['code'] = "B123={}".format(single_row['B123'])
                        dict['提示内容'] = 'B123购(建)房按揭贷款越界'
                        insert_to_pd(dict)

                if pd.isnull(single_row['B124']) == False:
                    if single_row['B124'] < 0.01 or single_row['B124'] >= 99:
                        dict['code'] = "B124={}".format(single_row['B124'])
                        dict['提示内容'] = 'B124购(建)房时借贷款总利息越界'
                        insert_to_pd(dict)

                if pd.isnull(single_row['B125']) == False:
                    if single_row['B126'] != 1 and single_row['B126'] != 2:
                        dict['code'] = "B126={}".format(single_row['B126'])
                        dict['提示内容'] = 'B126现在是否还在还款越界'
                        insert_to_pd(dict)

                if single_row['B121'] < single_row['B122']:
                    dict['code'] = "B121={},B122={}".format(single_row['B121'],single_row['B122'])
                    dict['提示内容'] = '借贷款总额不应大于购(建)房总金额'
                    insert_to_pd(dict)

                if single_row['B122'] < single_row['B123']:
                    dict['code'] = "B122={},B123={}".format(single_row['B122'], single_row['B123'])
                    dict['提示内容'] = '按揭贷款不应大于借贷款总额'
                    insert_to_pd(dict)

                if single_row['B122'] == 0:
                    if pd.isnull(single_row['B124']) == False:
                        dict['code'] = "B122={},B124={}".format(single_row['B122'], single_row['B124'])
                        dict['提示内容'] = '没借贷款不应有利息'
                        insert_to_pd(dict)

                    if pd.isnull(single_row['B125']) == False:
                        dict['code'] = "B122={},B125={}".format(single_row['B122'], single_row['B125'])
                        dict['提示内容'] = '没借贷款不应填还款总年限'
                        insert_to_pd(dict)

                    if pd.isnull(single_row['B126']) == False:
                        dict['code'] = "B122={},B126={}".format(single_row['B122'], single_row['B126'])
                        dict['提示内容'] = '没借贷款不应填写B126'
                        insert_to_pd(dict)

            # B1.3 期内拥有其它房屋情况
            data = single_row['B128']
            if data > 0:
                if data < 5 or data > 999:
                    dict['code'] = "B128={}".format(data)
                    dict['提示内容'] = 'B128出租住房建筑面积填报越界'
                    insert_to_pd(dict)

                if single_row['B129'] < 0.3 or single_row['B129'] >= 999:
                    dict['code'] = "B128={},B129={}".format(data,single_row['B129'])
                    dict['提示内容'] = 'B129出租住房市场价越界'
                    insert_to_pd(dict)

                if single_row['B130'] < 100 or single_row['B130'] >= 9999:
                    dict['code'] = "B128={},B130={}".format(data,single_row['B130'])
                    dict['提示内容'] = 'B130出租住房月租金越界'
                    insert_to_pd(dict)

            data = single_row['B131']
            if data > 0:
                if data < 1 or data > 999:
                    dict['code'] = "B131={}".format(single_row['B131'])
                    dict['提示内容'] = 'B131出租商用建筑物建筑面积填报越界'
                    insert_to_pd(dict)

                if single_row['B132'] < 0.3 or single_row['B132'] >= 999:
                    dict['code'] = "B131={},B132={}".format(single_row['B131'], single_row['B132'])
                    dict['提示内容'] = 'B132出租商用建筑物市场价越界'
                    insert_to_pd(dict)

            data = single_row['B134']
            if data > 0:
                if data < 1 or data > 999:
                    dict['code'] = "B134={}".format(single_row['B134'])
                    dict['提示内容'] = 'B134偶尔居住房建筑面积填报越界'
                    insert_to_pd(dict)

                if single_row['B135'] < 0.3 or single_row['B135'] >= 999:
                    dict['code'] = "B134={},B135={}".format(single_row['B134'], single_row['B135'])
                    dict['提示内容'] = 'B135偶尔居住房市场价越界'
                    insert_to_pd(dict)

            if single_row["B136"] > 0:
                if single_row['B136'] < 1 or single_row['B136'] > 999:
                    dict['code'] = "B136={}".format(single_row['B136'])
                    dict['提示内容'] = 'B136空宅或其他用途住房建筑面积填报越界'
                    insert_to_pd(dict)

                if single_row['B137'] < 0.3 or single_row['B137'] >= 999:
                    dict['code'] = "B136={},B137={}".format(single_row['B136'], single_row['B137'])
                    dict['提示内容'] = 'B137空宅或其他用途住房市场价越界'
                    insert_to_pd(dict)

            # B1.4新购住房情况审核
            if 7 >= single_row['B104'] >= 4 and single_row['B120'] == Year:
                if single_row['B138'] < 5 or single_row['B138'] >= 999:
                    dict['code'] = "B138={}".format(single_row['B138'])
                    dict['提示内容'] = '新购住房建筑面积越界'
                    insert_to_pd(dict)

                data = single_row['B140']
                if data != 0:
                    if data < 1 or data >= 999:
                        dict['code'] = "B140={}".format(single_row['B140'])
                        dict['提示内容'] = '新购住房借贷款总额(不含利息)越界'
                        insert_to_pd(dict)

                    if single_row['B141'] < 1 or single_row['B141'] >= 999:
                        dict['code'] = "B140={},B141={}".format(data,single_row['B141'])
                        dict['提示内容'] = '新购住房按界揭贷款越'
                        insert_to_pd(dict)

                    if single_row['B142'] < 1 or single_row['B142'] >= 99:
                        dict['code'] = "B140={},B142={}".format(data,single_row['B142'])
                        dict['提示内容'] = '新购住房借贷款总利息越界'
                        insert_to_pd(dict)

                    if single_row['B143'] < 1 or single_row['B143'] > 30:
                        dict['code'] = "B140={},B143={}".format(data,single_row['B143'])
                        dict['提示内容'] = '新购住房借贷款还款总年限越界'
                        insert_to_pd(dict)

                    if single_row['B142'] / data < 0 or single_row['B142'] / data >= 0.15:
                        dict['code'] = "B140={},B142={}".format(data,single_row['B142'])
                        dict['提示内容'] = '贷款利率越界'
                        insert_to_pd(dict)

                    if single_row['B143'] < 3 or single_row['B143'] > 30:
                        dict['code'] = "B140={},B143={}".format(data, single_row['B143'])
                        dict['提示内容'] = '还款年限越界'
                        insert_to_pd(dict)

                if single_row['B139'] <= data:
                    dict['code'] = "B140={},B139={}".format(data, single_row['B139'])
                    dict['提示内容'] = '借贷款总额不应大于购(建)房总金额'
                    insert_to_pd(dict)

                if data < single_row['B141']:
                    dict['code'] = "B140={},B141={}".format(data, single_row['B141'])
                    dict['提示内容'] = '按揭贷款不应大于借贷款总额'
                    insert_to_pd(dict)

                if data == 0:
                    if single_row['B142'] != 0:
                        dict['code'] = "B140={},B142={}".format(data, single_row['B142'])
                        dict['提示内容'] = '没借贷款不应有利息'
                        insert_to_pd(dict)

                    if single_row['B143'] != 0:
                        dict['code'] = "B140={},B143={}".format(data, single_row['B143'])
                        dict['提示内容'] = '没借贷款不应填还款总年限'
                        insert_to_pd(dict)


            # B1.5 新住房情况审核
            if single_row['B104'] == 3 and single_row['B120'] == Year:
                if single_row['B144'] != 0:
                    if single_row['B144'] < 5 or single_row['B144'] >= 999:
                        dict['code'] = "B144={}".format(single_row['B144'])
                        dict['提示内容'] = '新住房建筑面积越界'
                        insert_to_pd(dict)
                sum = single_row['B146'] + single_row['B147'] + single_row['B148'] + single_row['B149']
                if single_row['B145'] != sum :
                    dict['code'] = "B145={},B146{}+B147{}+B148{}+B149{}={}".format(single_row['B145'], single_row['B146'],single_row['B147'],single_row['B148'],single_row['B149'],sum)
                    dict['提示内容'] = '建房资金来源不平'
                    insert_to_pd(dict)

            # B1.6 期内住房大修或装修费用
            if single_row['B150'] > 99:
                dict['code'] = "B150={}".format(single_row['B150'])
                dict['提示内容'] = '住房大修或装修费用越界'
                insert_to_pd(dict)

            # break
        #B2部分 耐用消费品情况
        # if single_row['B101']:
        if pd.isnull(B101) == False:
            # print('ccc')
            if single_row['B201'] < 0 or single_row['B201'] > 3:
                dict['code'] = "B201={}".format(single_row['B201'])
                dict['提示内容'] = 'B201耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B202'] < 0 or single_row['B202'] > 3:
                dict['code'] = "B202={}".format(single_row['B202'])
                dict['提示内容'] = 'B202耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B203'] < 0 or single_row['B203'] > 5:
                dict['code'] = "B203={}".format(single_row['B203'])
                dict['提示内容'] = 'B203耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B204'] < 0 or single_row['B204'] > 5:
                dict['code'] = "B204={}".format(single_row['B204'])
                dict['提示内容'] = 'B204耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B205'] < 0 or single_row['B205'] > 5:
                dict['code'] = "B205={}".format(single_row['B205'])
                dict['提示内容'] = 'B205耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B206'] < 0 or single_row['B206'] > 5:
                dict['code'] = "B206={}".format(single_row['B206'])
                dict['提示内容'] = 'B206耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B207'] < 0 or single_row['B207'] > 5:
                dict['code'] = "B207={}".format(single_row['B207'])
                dict['提示内容'] = 'B207耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B208'] < 0 or single_row['B208'] > 10:
                dict['code'] = "B208={}".format(single_row['B208'])
                dict['提示内容'] = 'B208耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B209'] < 0 or single_row['B209'] > 7:
                dict['code'] = "B209={}".format(single_row['B209'])
                dict['提示内容'] = 'B209耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B210'] < 0 or single_row['B210'] > 3:
                dict['code'] = "B210={}".format(single_row['B210'])
                dict['提示内容'] = 'B210耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B211'] < 0 or single_row['B211'] > 5:
                dict['code'] = "B211={}".format(single_row['B211'])
                dict['提示内容'] = 'B211耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            #if single_row['B212'] < 0 or single_row['B212'] > 5:
             #   result.write('B212耐用消费品拥有量超界，请核实')
            if single_row['B213'] < 0 or single_row['B213'] > 2:
                dict['code'] = "B213={}".format(single_row['B213'])
                dict['提示内容'] = 'B213耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B214'] < 0 or single_row['B214'] > 2:
                dict['code'] = "B214={}".format(single_row['B214'])
                dict['提示内容'] = 'B214耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B215'] < 0 or single_row['B215'] > 3:
                dict['code'] = "B215={}".format(single_row['B215'])
                dict['提示内容'] = 'B215耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B216'] < 0 or single_row['B216'] > 10:
                dict['code'] = "B216={}".format(single_row['B216'])
                dict['提示内容'] = 'B216耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B217'] < 0 or single_row['B217'] > 10:
                dict['code'] = "B217={}".format(single_row['B217'])
                dict['提示内容'] = 'B217耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B218'] < 0 or single_row['B218'] > 10:
                dict['code'] = "B218={}".format(single_row['B218'])
                dict['提示内容'] = 'B218耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B219'] < 0 or single_row['B219'] > 10:
                dict['code'] = "B219={}".format(single_row['B219'])
                dict['提示内容'] = 'B219耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            #if single_row['B220'] < 0 or single_row['B220'] > 5:
             #   result.write('B220耐用消费品拥有量超界，请核实')
            if single_row['B221'] < 0 or single_row['B221'] > 5:
                dict['code'] = "B221={}".format(single_row['B221'])
                dict['提示内容'] = 'B221耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B222'] < 0 or single_row['B222'] > 5:
                dict['code'] = "B222={}".format(single_row['B222'])
                dict['提示内容'] = 'B222耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B223'] < 0 or single_row['B223'] > 5:
                dict['code'] = "B223={}".format(single_row['B223'])
                dict['提示内容'] = 'B223耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            #if single_row['B224'] < 0 or single_row['B224'] > 5:
             #   result.write('B224耐用消费品拥有量超界，请核实')
            if single_row['B225'] < 0 or single_row['B225'] > 5:
                dict['code'] = "B225={}".format(single_row['B225'])
                dict['提示内容'] = 'B225耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B226'] < 0 or single_row['B226'] > 5:
                dict['code'] = "B226={}".format(single_row['B226'])
                dict['提示内容'] = 'B226耐用消费品拥有量超界，请核实'
                insert_to_pd(dict)

            if single_row['B208'] > single_row['B207']:
                dict['code'] = "B207={},B208={}".format(single_row['B207'],single_row['B208'])
                dict['提示内容'] = 'B208拥有量不应超过B207，请核实'
                insert_to_pd(dict)

            if single_row['B211'] > single_row['B210']:
                dict['code'] = "B210={},B211={}".format(single_row['B210'], single_row['B211'])
                dict['提示内容'] = 'B211拥有量不应超过B210，请核实'
                insert_to_pd(dict)

            if single_row['B217'] > single_row['B216']:
                dict['code'] = "B216={},B217={}".format(single_row['B216'], single_row['B217'])
                dict['提示内容'] = 'B217拥有量不应超过B216，请核实'
                insert_to_pd(dict)

            if single_row['B219'] > single_row['B218']:
                dict['code'] = "B218={},B219={}".format(single_row['B218'], single_row['B219'])
                dict['提示内容'] = 'B219拥有量不应超过B218，请核实'
                insert_to_pd(dict)

        #B3部分 补充资料2：现住房房屋状况
        # if single_row['B101']:
            if single_row['B238'] < 1 or single_row['B238'] > 4:
                dict['code'] = "B238={}".format(single_row['B238'])
                dict['提示内容'] = '住户现住房所处场地状况越界，请填写(1-4)'
                insert_to_pd(dict)

            if single_row['B239'] < 1 or single_row['B239'] > 4:
                dict['code'] = "B239={}".format(single_row['B239'])
                dict['提示内容'] = '住户现住房屋安全状况越界，请填写(1-4)'
                insert_to_pd(dict)

            if single_row['B240'] != 1 and single_row['B240'] != 2:
                dict['code'] = "B240={}".format(single_row['B240'])
                dict['提示内容'] = '住宅地面是否经常有泥土、沙土、畜禽粪便等脏东西越界，请填写(1-2)'
                insert_to_pd(dict)

        #B3部分 补充资料3：家庭或家庭成员合伙、参股或独立控股公司（企业）的经营情况 *     lw 0905
        # if single_row['B101']:
            if single_row['B241'] != 1 and single_row['B241'] != 2:
                dict['code'] = "B241={}".format(single_row['B241'])
                dict['提示内容'] = '是否拥有独立控股的公司（企业）越界，请填写(1-2)'
                insert_to_pd(dict)

            if single_row['B243'] != 1 and single_row['B243'] != 2:
                dict['code'] = "B243={}".format(single_row['B243'])
                dict['提示内容'] = '是否拥有合伙或参股的公司（企业）越界，请填写(1-2)'
                insert_to_pd(dict)

            if single_row['B242'] > 0:
                if single_row['B241'] != 1:
                    dict['code'] = "B241={},B242={}".format(single_row['B241'],single_row['B242'])
                    dict['提示内容'] = '有公司（企业）税后净利润，应有公司'
                    insert_to_pd(dict)

            if single_row['B244'] > 0:
                if single_row['B243'] != 1:
                    dict['code'] = "B243={},B244={}".format(single_row['B243'], single_row['B242'])
                    dict['提示内容'] = '有公司（企业）税后净利润，应有公司'
                    insert_to_pd(dict)

        # print('done!')

    return B_necessity_result




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

    B_necessity_data = {'year': [], 'sid': [], 'scode': [], 'code': [], '提示内容': [], 'townname': [], 'vname': []}
    B_necessity_result = pd.DataFrame(B_necessity_data)
    B_necessity_result = B_necessity_result[['year', 'sid', 'scode', 'code', '提示内容', 'townname', 'vname']]

    B_necessity_check(tableB,zhuhu,zhuzhai,xiaoqu,B_necessity_result)
    B_necessity_result.to_csv('B_necessity_result.csv',encoding='utf_8_sig')
