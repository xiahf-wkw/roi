from decimal import Decimal


def get_zhushou_danjia(mysqlutil,dic_price):
    print(dic_price['124035'] * 3)  # 单价列表
    sql = "select sum(count) sum_c ,channel,soft_id from origin_from_sjzs_dist_soft  where `date`>='2019-12-31' and `date` <='2020-01-07'   GROUP BY channel,soft_id"
    channel_list = mysqlutil.query_all(sql)
    dic_cal = {}
    for i in channel_list:
        if i['channel'] not in dic_cal:
            soft_id_key = str(i['soft_id'])
            if soft_id_key in dic_price:
                dic_cal[i['channel']] = dic_price[soft_id_key] * int(i['sum_c'])
            else:
                dic_cal[i['channel']] = 0
        else:
            soft_id_key = str(i['soft_id'])
            if soft_id_key in dic_price:
                dic_cal[i['channel']] = dic_cal[i['channel']] + dic_price[soft_id_key] * int(i['sum_c'])
        # try:
        #     # print (dic_cal['sc-xuanyuanjrtt1_cpc_wch'])
        # except:
        #     pass


    sql = '''select channel, sum(count) sum1 from origin_from_sjzs_dist_channel   where `date`>='2019-12-31' and `date` <='2020-01-07' GROUP BY channel'''
    chinnel_send_list = mysqlutil.query_all(sql)

    chinnel_send_dic = {}
    for i in chinnel_send_list:
        chinnel_send_dic[i['channel']] = i['sum1']

    return dic_cal,chinnel_send_dic





def get_shouzhu_dingxiang(mysqlutil,dic_price,channel,dx_dic):
    sql = "select sum(count) sum_c ,channel,soft_id from origin_from_sjzs_dist_soft  where `date`>='2019-12-31' and `date`" \
          " <='2020-01-07' and register_date=date and  channel='%s' and soft_id='%s'  GROUP BY channel,soft_id" %(channel,dx_dic['soft_id'])

    channel_list = mysqlutil.query_all(sql)
    dic_cal = {}
    for i in channel_list:
        if i['channel'] not in dic_cal:
            soft_id_key = str(i['soft_id'])
            if soft_id_key in dic_price:
                dic_cal[i['channel']] = dic_price[soft_id_key] * int(i['sum_c'])
            else:
                dic_cal[i['channel']] = 0
        else:
            soft_id_key = str(i['soft_id'])
            if soft_id_key in dic_price:
                dic_cal[i['channel']] = dic_cal[i['channel']] + dic_price[soft_id_key] * int(i['sum_c'])

    sql = '''select channel, sum(count) sum1 from origin_from_sjzs_dist_soft   where `date`>='2019-12-31' and `date` <='2020-01-07' and 
    register_date=date  and channel='%s' and soft_id='%s'  GROUP BY channel''' %(channel,dx_dic['soft_id'])
    print (sql)
    chinnel_send_list = mysqlutil.query_all(sql)

    chinnel_send_dic = {}
    for i in chinnel_send_list:
        chinnel_send_dic[i['channel']] = i['sum1']

    return dic_cal, chinnel_send_dic

def get_dx_income(mysqlutil,dx_price,channel,dx_dic,date1):

    if dx_dic["passageway"] == "zs":
        table = "origin_from_sjzs_dist_soft"
    elif dx_dic["passageway"] == "yyb":
        table = "origin_from_sjzs_dist_yyb"

    sql = '''select channel, sum(count) sum1 from %s   where `date`='%s'  and 
       register_date=date  and channel='%s' and soft_id='%s'  GROUP BY channel''' % (table, date1,channel, dx_dic['soft_id'])

    chinnel_send_list = mysqlutil.query_all(sql)
    chinnel_send_dic = {}
    for i in chinnel_send_list:
        chinnel_send_dic[i['channel']] = i['sum1']
    print (Decimal(dx_price), chinnel_send_dic[channel])
    return Decimal(dx_price)*chinnel_send_dic[channel]


def check_zhushou_unit_price_with_db(mysqlutil,dic,date):
    sql = "SELECT * FROM original_from_sjzs_cal_price WHERE date='%s'"%date
    price_with_db = mysqlutil.query_all(sql)
    dic_db = {}
    for record in price_with_db:
        dic_db[record["channel"]] = record["price_7"]
    for i in dic.keys():
        result_contrast = []
        # print(i)
        try:
            if float(str(dic[i])[0:6]) == float(str(dic_db[i])[0:6]):
                c = i+"比对成功"
                result_contrast.append(c)
            else:
                d = i+"比对失败"
                print(i+":::"+"test_price:"+ str(dic[i]),"dev_price:"+str(dic_db[i]))
                result_contrast.append(d)
        except:
            print(i + ":::" + "test_price:" + str(dic[i]))
            print(i+"在库中不存在")



def check_dxb_income(mysqlutil,dic,date):
    sql = "SELECT * FROM original_from_sjzs_direct_price WHERE date='%s'"%date
    dxb_income_db = mysqlutil.query_all(sql)
    dic_db = {}
    for dxb_record in dxb_income_db:
        dic_db[dxb_record['channel']] = dxb_record['income']
        pass
    for i in dic.keys():
        dxb_result_constrast = []
        try:
            if round(float(str(dic[i])[0:6]),1) == round(float(str(dic_db[i])[0:6]),1):
                c = i +"比对成功"
                dxb_result_constrast.append(c)
                print(c + "dev_income:"+str(dic_db[i]) + "test_income"+ str(dic[i]))
            else:
                d = i +"比对失败"
                dxb_result_constrast.append(d)
                print(d + "dev_price:" + str(dic_db[i])+"test_income:" + str(dic[i]))
        except:
            print("库中不存在")



















