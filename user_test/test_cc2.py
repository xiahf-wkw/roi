import pytest
from user_test.util.Des import *
import logging

import requests
import logconfig

from commonutils.logutil import *
from commonutils.data_gen import *
from commonutils.mysql_utils import *
import json
from commonutils.yaml_utils import *
logger = logging.getLogger(__file__)  # 生成logger实例


class Test(object):
    '''test1122'''
    port = ""
    salt = "118test"
    salt = "b66faf5855eefc11c2961d402bb140be" # 线上


    @classmethod
    def setup_class(cls):
        pass

    def teardown_method(self, method):
        print('\n测试用例执行完毕')

    @pytest.fixture(scope="module", autouse=True)
    def init_data(self, request):
        envopt = request.config.getoption("--envopt")
        print("env:" + envopt)
        return {"env": get_envconfig()['ach_envconfig'][envopt]}

    # def test_submit_activity(self, init_data):
    #     url = "http://%s/service/Exp" % init_data['env']
    #     data = {"project": "xq",
    #             "requestTime": "%s" % create_long_time(),
    #             "processList": '''[{"projectSN":"%s","passId":"34",''' % create_random_id() +
    #                            '''"tradingValue":313,"taskId":"12","tradingTime":"%s","desc":"1111"}]''' % (
    #                                create_long_time())}
    #     sign = Des.get_sign(data, self.salt)
    #     data['sign'] = sign
    #     print(data)
    #     print(url)
    #     r = requests.post(url, data=data)
    #     logger_print(data, r.json())
    #     assert r.json().get('code') == 201
    #
    # test_data=["sign_in",
    #             "install",
    #             "gain_gold",
    #             "read",
    #             "questionnaire",
    #             "orchard",
    #             "turntable",
    #             "invite",
    #             "qdtest",]
    # @pytest.mark.parametrize("data", test_data)
    # def test_submit_achievement(self, init_data,data):
    #     '''正常情况'''
    #     passId=1989
    #     url = "http://%s/service/report" % init_data['env']
    #     data = {"project": "xq",
    #             "requestTime": "%s" % create_long_time(),
    #             "type": "achv",
    #             "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":413,"taskId":"12","tradingTime":"%s",'''%
    #                            (create_random_id(),passId, create_long_time())+
    #             '''"desc":"1111","code":"%s"}]'''% data  }
    #     sign = Des.get_sign(data, self.salt)
    #     data['sign'] = sign
    #     r = requests.post(url, data=data)
    #     print(url)
    #     logger.info(Des.get_passid_distribution(passId))
    #     logger_print(data, r.json())
    #     assert r.json()['code']==200
    #
    #
    # # def test_33(self,init_data):
    # #     data = {"project": "xq",
    # #             "requestTime": "1573524875",
    # #             "type": "achv",
    # #             "processList": '''[{"projectSN":"271542999","passId":"60000","tradingValue":13,"taskId":"12","tradingTime":"1573524875","desc":"1111","code":"sign_in"}]'''}
    # #     sign = Des.get_sign(data, self.salt)
    # #     print (sign)
    # #     mysql1=MysqlUtil("T1","userlevel_xq")
    # #     result=mysql1.query_all("select * from userinfo_1")
    # #     print (result)
    # #     del mysql1
    # test_data2=[
    #     5330069824,
    #     2574950463,
    #     6780094194,
    #     7185319985,
    #     1717750743,
    #     8026917198,
    #     6816260735,
    #     9826668328,
    #     4084211834,
    #     1689524145,
    #     6066389160,
    #     7935875703,
    #     7154222893,
    #     1587635302,
    #     7343609290,
    #     5731081460,
    #     7107313375,
    #     3454447079,
    #     7909232933,
    #     2594864839,
    #     2687836423,
    # ]
    #
    # @pytest.mark.parametrize("data", test_data2)
    # def test_select_achievement(self, init_data,data):
    #     '''查询成就'''
    #     passId = data
    #     url = "http://%s/service/User/Achievement" % init_data['env']
    #
    #     data = {"project": "xq",
    #             "requestTime": "%s" % create_long_time(),
    #             "passId": str(passId)}
    #     print("sss:" + str(data))
    #     sign = Des.get_sign(data, self.salt)
    #     data['sign'] = sign
    #     r = requests.get(url, params=data)
    #     print(url)
    #     logger.info(Des.get_passid_distribution(passId))
    #     logger_print(data, r.json())
    #
    #
    # def test_submit_user_exp_and_ach(self,init_data):
    #     '''上报成就'''
    #     passId = create_random_id()
    #     global passId_global
    #     passId_global = passId  # 给到全局passid
    #     url = "http://%s/service/report" % init_data['env']
    #     data = {"project": "ydlm",
    #             "requestTime": "%s" % create_long_time(),
    #             "type": "achv",
    #             "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":100,"taskId":"12","tradingTime":"%s",''' %
    #                            (create_random_id(), passId, create_long_time()) +
    #                            '''"desc":"1111","code":"install"}]'''}
    #     sign = Des.get_sign(data, self.salt)
    #     data['sign'] = sign
    #     print(data)
    #     r = requests.post(url, data=data)
    #     print(url)
    #     logger.info(str(passId) + "," + str(Des.get_passid_distribution(passId)))
    #     logger_print(data, r.json())
    #     assert r.json()['code'] == 200
    #     #上报活跃值
    #     url = "http://%s/service/Exp" % init_data['env']
    #     data = {"project": "ydlm",
    #             "requestTime": "%s" % create_long_time(),
    #             "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":28,"taskId":"12","tradingTime":"%s","desc":"1111"}]''' %
    #                            (create_random_id(), passId, create_long_time())
    #             }
    #     sign = Des.get_sign(data, self.salt)
    #     data['sign'] = sign
    #     r = requests.post(url, data=data)
    #     logger.info(str(passId) + "," + str(Des.get_passid_distribution(passId)))
    #     logger_print(data, r.json())
    #
    #
    #
    # def test_select_achievement(self, init_data):
    #     '''查询成就'''
    #     passId =5907494605
    #     url = "http://%s/service/User/Achievement" % init_data['env']
    #
    #     data = {"project": "ydlm",
    #             "requestTime": "%s" % create_long_time(),
    #             "passId": str(passId)}
    #     print("sss:" + str(data))
    #     sign = Des.get_sign(data, self.salt)
    #     data['sign'] = sign
    #     r = requests.get(url, params=data)
    #     print(url)
    #     logger.info(Des.get_passid_distribution(passId))
    #     logger_print(data, r.json())

    def test_select_userinfo(self, init_data):
        '''查询用户信息'''
        passId = 125820878
        url = "http://%s/service/User" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "passId": str(passId),
                "ignoreAchv": "ignore"
                }

        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.get(url, params=data)
        logger.info("查询")
        logger_print(data, r.json())
        #time.sleep(4)


    def test_select_3_day_detail(self, init_data):
        '''3天明细'''
        passId = 125820878
        url = "http://%s/service/Exp/expDetail" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "passId": str(passId),
                "tradingDate": "2020-01-07,2020-01-08,2020-01-09"
                }

        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.get(url, params=data)
        logger.info("查询明细")
        logger_print(data, r.json())
        #time.sleep(4)
