import datetime
from shouzhu_roi_test.util.util import *
import pytest

from commonutils.mysql_utils import MysqlUtil
from user_test.util.Des import *
import logging

import requests
import logconfig

from commonutils.logutil import *
from commonutils.data_gen import *

import json

from commonutils.yaml_utils import *

logger = logging.getLogger(__file__)  # 生成logger实例

#global data
passId_global=1704805759

exp_passid_global=0


class Test(object):
    port = ""
    salt = "118test"
    db_check = True

    @classmethod
    def setup_class(cls):
        pass

    def teardown_method(self, method):
        print('\n测试用例执行完毕')

    @pytest.fixture(scope="module", autouse=True)
    def init_data(self, request):
        envopt = request.config.getoption("--envopt")
        db_check = request.config.getoption("--db_check")
        print("env:" + envopt)
        try:
            mysql_util = MysqlUtil('shouzhu_envconfig',envopt, "roi_test")
        except Exception as e:
            mysql_util=None
        return {"env":  get_envconfig()['ach_envconfig'][envopt], "mysql_util": mysql_util, "db_check": db_check}

    def test_1(self,init_data):
        ''''''
        #拿最新单价list
        mysqlutil=init_data["mysql_util"]
        sql='''select * from original_from_sjzs_price as t 
                where t.id in 
                (
                select SUBSTRING_INDEX(group_concat(id order by `date` desc),',',1) from original_from_sjzs_price 
                 group by soft_id
                ) 
                '''
        dic_price_list=mysqlutil.query_all(sql)
        dic_price={}
        dic_price_cpd={}
        for i in dic_price_list:
            if str(i['date'])=='2020-01-07' and i['type']=='CPD':
                dic_price_cpd[str(i['soft_id'])]=i['price']
            if str(i['date']) == '2020-01-07':
                dic_price[str(i['soft_id'])] = i['price']

        dic_cal, chinnel_send_dic=get_zhushou_danjia(mysqlutil,dic_price_cpd)
        print (dic_cal,chinnel_send_dic)


        #dingxiang
        dic_dx={"sc-xuanyuanjrtt1_cpc_wch":{"price":"xxx","soft_id":83520}}


        dic_test = {}
        for i in dic_cal.keys():
            if i not in dic_dx:
                try:
                    dic_test[i] = dic_cal[i] / chinnel_send_dic[i]
                except:
                    dic_test[i] = 0
            else:
                dic_cal_dx, chinnel_send_dic_dx=get_shouzhu_dingxiang(mysqlutil,dic_price,i,dic_dx[i])

                print (dic_cal_dx,chinnel_send_dic_dx)
                if (chinnel_send_dic[i] - chinnel_send_dic_dx[i]) == 0:
                    dic_test[i] = 0
                else:
                    dic_test[i] = (dic_cal[i] - dic_cal_dx[i]) / (chinnel_send_dic[i] - chinnel_send_dic_dx[i])


        channel_tmp='sc-xuanyuanjrtt1_cpc_wch'
        print(dic_cal[channel_tmp], chinnel_send_dic[channel_tmp])
        try:
            print(dic_cal_dx[channel_tmp], chinnel_send_dic_dx[channel_tmp])
        except:
            pass
        print(dic_test[channel_tmp])
        return dic_test

    def test_2(self, init_data):
        '''定向收入'''
        dic_dx = {"sc-xuanyuanjrtt1_cpc_wch": {"price": 6.2, "soft_id": 83520, "passageway": "zs"},
                  "sc-zyyxuanyuanjrtt01_cpc_wg": {"price": 0, "soft_id": 173675, "passageway": "yyb"},
                  "sc-zsyuntianjrtt06_cpc_zdf": {"price": 5.1, "soft_id": 173675, "passageway": "yyb"},
                  "sc-smsemydqq_cpc_ljj": {"price": 5.3, "soft_id": 147779, "passageway": "yyb"},
                  "sc-mingya_ins_ljj": {"price": 5.4, "soft_id": 102657, "passageway": "yyb"},
                  "sc-dptf5_ins_lhp": {"price": 0, "soft_id": 82518, "passageway": "zs"},
                  "sc-smsemyd015_cpc_ljj": {"price": 6.1, "soft_id": 86275, "passageway": "zs"},
                  "sc-smsemydsjtb_cpc_ljj": {"price": 5.2, "soft_id": 174029, "passageway": "yyb"},
                  }
        date1 = "2019-12-31"
        mysqlutil = init_data["mysql_util"]
        dic_dx_in = {}
        for key, value in dic_dx.items():
            # print(value)
            income = get_dx_income(mysqlutil, value["price"], key, value, date1)
            dic_dx_in[key] = income
        # print(dic_dx_in)
        return dic_dx_in

    def test_xxx(self,init_data):
        dic_test = self.test_1(init_data)
        mysqlutil=init_data["mysql_util"]
        check_zhushou_unit_price_with_db(mysqlutil,dic_test,'2019-12-31')


    def test_aaa(self,init_data):
        dic_dxb_test = self.test_2(init_data)
        mysqlutil = init_data["mysql_util"]
        check_dxb_income(mysqlutil,dic_dxb_test,'2019-12-31')







