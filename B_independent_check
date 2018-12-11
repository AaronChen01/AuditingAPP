# ***
# ***qbjcheck.prg
# **B卷check

# from decimal import Decimal
import pandas as pd
import myLogging as mylogger
import datetime

B_independent_result = pd.DataFrame()


def insert_to_pd(data):
    global B_independent_result
    B_independent_result = B_independent_result.append(data,ignore_index=True)


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


def B_independent_check(tableB,xiaoqu,result):
    mylogger.logger.debug("B_independent_check init...")
    Year = datetime.datetime.now().year
    global B_independent_result
    B_independent_result.drop(B_independent_result.index,inplace = True)
    B_independent_result = result

    for row in tableB.iterrows():
        B = row[1]
        year = str(B['YEAR'])
        family_sid = B['SID']
        scode = B['SCODE']
        qu_vid = family_sid[0:15]
        qu = xiaoqu[xiaoqu['vID'] == qu_vid]
        townname = qu['townName'].values[0]
        vname = qu['vName'].values[0]

        dict = {'year': year, 'sid': family_sid, 'scode': scode, 'townname': townname,'vname': vname}

        if B['B102'] == 8:
            dict['code'] = "B102=8"
            dict['提示内容'] = "本户居住空间样式为其他？请核实！"
            insert_to_pd(dict)

        if B['B103'] == 4 or B['B103'] == 5:
            dict['code'] = "B103={}".format(B['B103'])
            dict['提示内容'] = "本户房屋主要建筑材料为竹草或其他？请核实！"
            insert_to_pd(dict)

        b104 = B['B104']
        # print(type(b104))
        if b104 == 11:
            dict['code'] = "B104=11"
            dict['提示内容'] = "本户房屋来源为其他？请核实！"
            insert_to_pd(dict)

        if B['B106'] == 3:
            dict['code'] = "B106=3"
            dict['提示内容'] = "本户住宅外道路路面情况为其他？请核实！"
            insert_to_pd(dict)

        if B['B107'] == 2 or B['B107'] == 3:
            dict['code'] = "B107={}".format(B['B107'])
            dict['提示内容'] = "本户供水为管道供水至公共取水点或没有管道设施？请核实！"
            insert_to_pd(dict)

        if B['B108'] == 4 or B['B108'] == 5 or B['B108'] == 7:
            dict['code'] = "B108={}".format(B['B108'])
            dict['提示内容'] = "本户主要饮用水来源为江河湖泊水或收集雨水或其他水源？请核实！"
            insert_to_pd(dict)

        if B['B109'] == 1 or B['B109'] == 2 or B['B109'] == 3:
            dict['code'] = "B108={}".format(B['B108'])
            dict['提示内容'] = "本户获取饮用水存在主要困难1or2or3？请核实！"
            insert_to_pd(dict)

        if B['B110'] == 4 or B['B110'] == 5:
            dict['code'] = "B110={}".format(B['B110'])
            dict['提示内容'] = "本户饮用水引用前在家里所采取的主要措施为4or5？请核实！"
            insert_to_pd(dict)

        if B['B111'] == 5 and B['B112'] == 1:
            dict['code'] = "B111={},B112={}".format(B['b111'],B['B112'])
            dict['提示内容'] = "本户b111无厕所，b112却等于1（本户独用）？请核实！"
            insert_to_pd(dict)

        if B['B113'] == 1:
            dict['code'] = "B113=1"
            dict['提示内容'] = "本户洗澡设施同意供热水（B113=1）？请核实！"
            insert_to_pd(dict)

        if B['B113'] == 3:
            dict['code'] = "B113=3"
            dict['提示内容'] = "本户洗澡设施为其他？请核实！"
            insert_to_pd(dict)

        if B['B114'] == 1:
            dict['code'] = "B114=1"
            dict['提示内容'] = "本户取暖设备由小区集中供暖？请核实！"
            insert_to_pd(dict)

        if B['B115'] == 1 or B['B115'] == 2 or B['B115'] == 8 or B['B115'] == 9 or B['B115'] == 10:
            dict['code'] = "B115={}".format(B['B115'])
            dict['提示内容'] = "本户取暖能源状况异常？B115为1或2或8或9或10，请核实！"
            insert_to_pd(dict)

        if B['B116'] == 2 or B['B116'] == 8 or B['B116'] == 9 or B['B116'] == 10:
            dict['code'] = "B116={}".format(B['B116'])
            dict['提示内容'] = "本户炊用能源状况异常？B116为2或8或9或10，请核实！"
            insert_to_pd(dict)

        if 3 < b104 < 8:
            if int(B['B117']) > Year:
                dict['code'] = "B104={].B117={}".format(b104,B['B117'])
                dict['提示内容'] = "本户自有现住房建筑年份大于系统现在时间？请核实！"
                insert_to_pd(dict)
            if B['B118'] == 0:
                dict['code'] = "B104={},B118={}".format(b104,B['B118'])
                dict['提示内容'] = "本户自有现住房市场价估计值为0，漏填？请核实！"
                insert_to_pd(dict)
            if B['B118'] > 1000:
                dict['code'] = "B104={},B118={}".format(b104, B['B118'])
                dict['提示内容'] = "本户自有现住房市场价估计值高于1000万？请核实！"
                insert_to_pd(dict)
            coun = int(family_sid[0:5])
            if (B['B119'] > 15000 or B['B119'] < 500) and 310101 < coun < 310110:
                dict['code'] = "B104={},B119={}".format(b104, B['B119'])
                dict['提示内容'] = "本市区户同类住房的市场价月租金低于500元或高于1.5万元？请核实！"
                insert_to_pd(dict)
            if (B['B119'] > 10000 or B['B119'] < 200) and 310112 < coun < 310230:
                dict['code'] = "B104={},B119={}".format(b104, B['B119'])
                dict['提示内容'] = "本郊区户同类住房的市场价月租金低于200元或高于1万元？请核实！"
                insert_to_pd(dict)
            if int(B['B120']) > Year:
                dict['code'] = "B104={},B120={}".format(b104, B['B120'])
                dict['提示内容'] = "本户自有现住房购（建）年份大于系统现在时间？请核实！"
                insert_to_pd(dict)
            if int(B['B120']) != 0 and B['B120'] < B['B117']:
                dict['code'] = "B104={},B117={},B120={}".format(b104,B['B117'], B['B120'])
                dict['提示内容'] = "本户自有现住房购（建）年份小于b117,小于建筑年份？买房时间早于建房时间，不可能。请核实！"
                insert_to_pd(dict)
            if b104 != 7 and B['B121'] == 0:
                dict['code'] = "B104={},B121={}".format(b104, B['B121'])
                dict['提示内容'] = "本户购（建）房总金额为0，漏记？请核实！"
                insert_to_pd(dict)
            if B['B121'] > 1000:
                dict['code'] = "B104={},B121={}".format(b104,B['B121'])
                dict['提示内容'] = "本户购（建）房总金额大于1000万元？请核实！"
                insert_to_pd(dict)
            if (B['B120'] > 2000 and b104 == 4) and B['B121']<5:
                dict['code'] = "B120={},B104={},B121={}".format(B['B120'],b104, B['B121'])
                dict['提示内容'] = "本户2000年后购（建）商品房（b104=4）总金额却低于5万元？请核实！"
                insert_to_pd(dict)
            if b104 != 3 and int(B['B118']) - int(B['B121']) < 0:
                dict['code'] = "B118={},B104={},B121={}".format(B['B118'], b104, B['B121'])
                dict['提示内容'] = "本户b118-b121<0，房屋价格下降了？请核实！"
                insert_to_pd(dict)
            if b104 == 3 and int(B['B118']) - int(B['B121']) < 0:
                if int(B['B118']) < 0.3* int(B['B121']) and int(B['B121']) > 100:
                    dict['code'] = "B118={},B104={},B121={}".format(B['B118'], b104, B['B121'])
                    dict['提示内容'] = "本户为自建住房，b118(现价)低于b121(购或建价)的30%?折旧也太厉害了。填错？漏填？请核实！"
                    insert_to_pd(dict)
            if B['B123'] > B['B122']:
                dict['code'] = "B123={},B104={},B122={}".format(B['B123'], b104, B['B122'])
                dict['提示内容'] = "本户按揭贷款高于借贷款总额？不可能。请核实！"
                insert_to_pd(dict)
            if B['B125'] > 30:
                dict['code'] = "B125={},B104={}".format(B['B125'], b104)
                dict['提示内容'] = "本户借贷款还款总年限高于30年?请核实！"
                insert_to_pd(dict)
        if b104 < 3 or b104 > 8:
            arr = ['B117','B118','B119','B120','B121','B122','B123','B124','B125','B126']
            for i in arr:
                if B[i] != 0 and pd.isnull(B[i])==False:
                    dict['code']="B104={},{}={}".format(b104,i,B[i])
                    dict['提示内容'] = "请查看B卷B117-B126的值,本户B104不为3-8，B117-B126却有值。填错？"
                    insert_to_pd(dict)

        if (b104 == 1 or b104 == 2) and B['B127'] == 0:
            dict['code'] = "B127={},B104={}".format(B['B127'], b104)
            dict['提示内容'] = "本户租赁房户，但却没有租赁月租金?请核实！"
            insert_to_pd(dict)
        if (b104 != 1 and b104 != 2) and B['B127'] != 0 and pd.isnull(B['B127'])==False:
            dict['code'] = "B127={},B104={}".format(B['B127'], b104)
            dict['提示内容'] = "本户租赁月租金B127有值，但却不是租赁房（B104不为1或2），填错?请核实！"
            insert_to_pd(dict)

        if 0 < B['B150'] < 0.5:
            dict['code'] = "B150={}".format(B['B150'])
            dict['提示内容'] = "本户期内住房大修或装修费用低于5000元或高于30万元？"
            insert_to_pd(dict)

        if B['B238'] == 0:
            dict['code'] = "B238={}".format(B['B238'])
            dict['提示内容'] = "本户现住房所处场地B238(X21)为空，漏填？"
            insert_to_pd(dict)
        else:
            if B['B238'] != 4:
                dict['code'] = "B238={}".format(B['B238'])
                dict['提示内容'] = "本户现住房所处场地B238(X21)有危险？请核实！"
                insert_to_pd(dict)

        if B['B239'] == 0:
            dict['code'] = "B239={}".format(B['B239'])
            dict['提示内容'] = "本户现住房安全状况B239(X22)为空，漏填？"
            insert_to_pd(dict)
        else:
            if B['B239'] != 1 and B['B239'] != 2:
                dict['code'] = "B239={}".format(B['B239'])
                dict['提示内容'] = "本户现住房安全状况B239(X22)有危险？请核实！"
                insert_to_pd(dict)

        if B['B240'] == 0:
            dict['code'] = "B240={}".format(B['B240'])
            dict['提示内容'] = "本户住宅地面经常有泥土、沙土、畜禽粪便等脏东西B240(X23)为空，漏填？请核实！"
            insert_to_pd(dict)
        else:
            if B['B240'] != 2:
                dict['code'] = "B240={}".format(B['B240'])
                dict['提示内容'] = "本户住宅地面经常有泥土、沙土、畜禽粪便等脏东西？B240(X23)请核实！"
                insert_to_pd(dict)

# ******下面是B卷超界的审核****************************************************
        for i in ['B101','B109','B113','B238','B239']:
            bi = B[i]
            # print(bi,type(bi))
            if bi != 1 and bi != 2 and bi != 3 and bi != 4:
                dict['code'] = "{}={}".format(i,bi)
                dict['提示内容'] = "本户{}所填内容超界或漏填。请核实！".format(bi)
                insert_to_pd(dict)

        for j in ['B106','B107','B112','B114']:
            bj = B[j]
            if bj != 1 and bj != 2 and bj != 3:
                dict['code'] = "{}={}".format(j,bj)
                dict['提示内容'] = "本户{}所填内容超界或漏填。请核实！".format(j)
                insert_to_pd(dict)

        for k in ['B240','B241','B243']:
            bk = B[k]
            if bk != 1 and bk != 2:
                dict['code'] = "{}={}".format(k,bk)
                dict['提示内容'] = "本户{}所填内容超界或漏填。请核实！".format(k)
                insert_to_pd(dict)

        for m in ['B102']:
            bm = B[m]
            if bm != 1 and bm != 2 and bm != 3 and bm!=4 and bm!=5 and bm!=6 and bm!=7 and bm!=8:
                dict['code'] = "{}={}".format(m,bm)
                dict['提示内容'] = "本户{}所填内容超界或漏填。请核实！".format(m)
                insert_to_pd(dict)

        for n in ['B103','B110','B111']:
            bn = B[n]
            if bn != 1 and bn != 2 and bn != 3 and bn!=5 :
                dict['code'] = "{}={}".format(n,bn)
                dict['提示内容'] = "本户{}所填内容超界或漏填。请核实！".format(n)
                insert_to_pd(dict)

        # b1 = B['B101']
        # if b1!=1 and b1!=2 and b1!=3 and b1!=4:
        #     dict['code'] = "B101={}".format(b1)
        #     dict['提示内容'] = "本户B101所填内容超界或漏填。请核实！"
        #     insert_to_pd(dict)
        # b2 = B['B102']
        # if b2!=1 and b2!=2 and b2!=3 and b2!=4 and b2!=5 and b2!=6 and b2!=7 and b2!=8:
        #     dict['code'] = "B102={}".format(b2)
        #     dict['提示内容'] = "本户B102所填内容超界或漏填。请核实！"
        #     insert_to_pd(dict)
        # b3 = B['B103']
        # if b3!=1 and b3!=2 and b3!=3 and b3!=4 and b3!=5:
        #     dict['code'] = "B103={}".format(b3)
        #     dict['提示内容'] = "本户B103所填内容超界或漏填。请核实！"
        #     insert_to_pd(dict)
        b4 = b104
        if b4!=1 and b4!=2 and b4!=3 and b4!=4 and b4!=5 and b4!=5 and b4!=6 and b4!=7 and b4!=8 and b4!=9 and b4!=10:
            dict['code'] = "B104={}".format(b4)
            dict['提示内容'] = "本户B104所填内容超界或漏填。请核实！"
            insert_to_pd(dict)
        # b6 = B['B106']
        # if b6!=1 and b6!=2 and b6!=3:
        #     dict['code'] = "B106={}".format(b6)
        #     dict['提示内容'] = "本户B106所填内容超界或漏填。请核实！"
        #     insert_to_pd(dict)
        # b7 = B['B107']
        # if b7 != 1 and b7 != 2 and b7 != 3:
        #     dict['code'] = "B107={}".format(b7)
        #     dict['提示内容'] = "本户B107所填内容超界或漏填。请核实！"
        #     insert_to_pd(dict)
        b8 = B['B108']
        if b8 != 1 and b8 != 2 and b8 != 3 and b8!=4 and b8!=5 and b8!=6 and b8!=7:
            dict['code'] = "B108={}".format(b8)
            dict['提示内容'] = "本户B108所填内容超界或漏填。请核实！"
            insert_to_pd(dict)
        b115=B['B115']
        if b115!=1 and b115!=2 and b115!=3 and b115!=4 and b115!=5 and b115!=5 and b115!=6 and b115!=7 and b4!=8 and b115!=9 and b115!=10 and b115!=11:
            dict['code'] = "B115={}".format(b115)
            dict['提示内容'] = "本户B115所填内容超界或漏填。请核实！"
            insert_to_pd(dict)

        b116 = B['B116']
        if b116 != 1 and b116 != 2 and b116 != 3 and b116 != 116 and b116 != 5 and b116 != 5 and b116 != 6 and b116 != 7 and b116 != 8 and b116 != 11:
            dict['code'] = "B116={}".format(b116)
            dict['提示内容'] = "本户B116所填内容超界或漏填。请核实！"
            insert_to_pd(dict)

        b126 = B['B126']
        if b126!= 1 and b126!=2 and b126!=0:
            dict['code'] = "B126={}".format(b126)
            dict['提示内容'] = "本户B126所填内容超界或漏填。请核实！"
            insert_to_pd(dict)

    return B_independent_result



if  __name__ == "__main__":
    B_path = "D:\研一\审核程序\src\输入文件夹\B310151.18.csv"
    xiaoqu_path = u"D:\研一\项目\CheckProgram\Auditing\输入文件夹\小区名录310151.18.csv"
    xiaoqu = read_csv(xiaoqu_path)
    tableB = read_csv(B_path)
    head = {'year': [], 'sid': [], 'scode': [], 'code': [], '提示内容': [], 'townname': [], 'vname': []}
    B_independent_result = pd.DataFrame(head)
    B_independent_result = B_independent_result[['year', 'sid', 'scode', 'code', '提示内容', 'townname', 'vname']]
    B_independent_check(tableB,xiaoqu,B_independent_result)
    B_independent_result.to_excel('./B_independent_result.xlsx',encoding="utf-8",index=False,sheet_name='Sheet')





























