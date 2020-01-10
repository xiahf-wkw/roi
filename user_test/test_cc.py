import datetime

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
            mysql_util = MysqlUtil('ach_envconfig',envopt, "userlevel_achv_xq")
        except Exception as e:
            mysql_util=None
        return {"env":  get_envconfig()['ach_envconfig'][envopt], "mysql_util": mysql_util, "db_check": db_check}

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

    def test_submit_achievement(self, init_data):
        '''正常情况'''
        passId =create_random_id()
        global passId_global
        passId_global=passId  #给到全局passid
        url = "http://%s/service/report" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "type": "achv",
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":100,"taskId":"12","tradingTime":"%s",''' %
                               (create_random_id(), passId, create_long_time()) +
                               '''"desc":"1111","code":"sign_in"}]'''}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info(str(passId) +","+str(Des.get_passid_distribution(passId)))
        logger_print(data, r.json())
        assert r.json()['code'] == 200
        if init_data['db_check']:
            sql = "select * from user_achv_%s where pass_id='%s'" % (Des.get_passid_distribution(passId), passId)
            print(sql)
            result1 = init_data['mysql_util'].query_in_time(sql, 15)
            # sql = "select * from userinfo_%s where pass_id='%s'" % (Des.get_passid_distribution(passId), passId)
            # result2 = init_data['mysql_util'].query_in_time(sql, 1)
            date1 = str(datetime.datetime.today())[0:10].replace("-", "")[2:]
            sql = "select * from achv_detail_%s_%s where pass_id='%s'" % (
            date1, Des.get_passid_distribution(passId), passId)
            result3 = init_data['mysql_util'].query_in_time(sql, 1)
            assert result1 != None
            assert result3 != None
            #assert result2 != None

    def test_submit_achievement_mul(self, init_data):
        '''正常情况,多个一起上报'''
        passId =create_random_id()
        url = "http://%s/service/report" % init_data['env']
        list1 = []
        list_code = ["sign_in", "install", "gain_gold"]
        for i in range(3):
            list1.append({"projectSN": "%s" % create_random_id(), "passId": "%s" % passId, "taskId": "12",
                          "tradingTime": "%s" % create_long_time(), "desc": "1111", "code": "%s" % list_code[i],
                          "tradingValue": 313})
        # a=[{"projectSN":"%s"%create_random_id(),"passId":"%s"%passId ,"taskId":"12","tradingTime":"%s" %create_long_time(),"desc":"1111","code":"sign_in"}]
        processlist = json.dumps(list1)
        processlist = (processlist.replace(' ', ''))
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "type": "achv",
                "processList": processlist}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info("passid_:"+str(str(passId) + "," + str(Des.get_passid_distribution(passId))))
        logger_print(data, r.json())
        assert r.json()['code'] == 200
        return passId

    def test_submit_achievement_mul_same_liushui(self, init_data):
        '''异常情况,多个一起上报，2个流水号一样'''
        passId = create_random_id()
        url = "http://%s/service/report" % init_data['env']
        list1 = []
        list_code = ["sign_in", "install", "gain_gold"]
        projectSN=create_random_id()
        for i in range(3):
            list1.append({"projectSN": "%s" % projectSN, "passId": "%s" % passId, "taskId": "12",
                          "tradingTime": "%s" % create_long_time(), "desc": "1111", "code": "%s" % list_code[i],
                          "tradingValue": 313})
        # a=[{"projectSN":"%s"%create_random_id(),"passId":"%s"%passId ,"taskId":"12","tradingTime":"%s" %create_long_time(),"desc":"1111","code":"sign_in"}]
        processlist = json.dumps(list1)
        processlist = (processlist.replace(' ', ''))
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "type": "achv",
                "processList": processlist}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info(str(passId+","+str(Des.get_passid_distribution(passId))))
        logger_print(data, r.json())
        assert r.json()['code'] == 200


    def test_submit_achievement_sign_error(self, init_data):
        '''sign错误情况'''
        passId = 34
        url = "http://%s/service/report" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "type": "achv",
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":313,"taskId":"12","tradingTime":"%s",''' %
                               (create_random_id(), passId, create_long_time()) +
                               '''"desc":"1111","code":"sign_in"}]'''}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = 'sign'
        r = requests.post(url, data=data)

        logger.info(Des.get_passid_distribution(passId))
        logger_print(data, r.json())
        assert r.json()['code'] == 4002

    def test_submit_achievement_time_error(self, init_data):
        '''request错误情况'''
        passId = 34
        url = "http://%s/service/report" % init_data['env']
        data = {"project": "xq",
                "requestTime": "1570518465",
                "type": "achv",
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":313,"taskId":"12","tradingTime":"%s",''' %
                               (create_random_id(), passId, create_long_time()) +
                               '''"desc":"1111","code":"sign_in"}]'''}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info(Des.get_passid_distribution(passId))
        logger_print(data, r.json())
        assert r.json()['code'] == 4005

    def test_submit_achievement_ache_error(self, init_data):
        '''成就值负数情况'''
        passId = create_random_id()
        url = "http://%s/service/report" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "type": "achv",
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":-5,"taskId":"12","tradingTime":"%s",''' %
                               (create_random_id(), passId, create_long_time()) +
                               '''"desc":"1111","code":"sign_in"}]'''}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info(Des.get_passid_distribution(passId))
        logger_print(data, r.json())
        assert r.json()['code'] == 200
        if init_data['db_check']:
            sql = "select * from user_achv_%s where pass_id='%s'" % (Des.get_passid_distribution(passId), passId)
            result1 = init_data['mysql_util'].query_in_time(sql, 10)
            assert result1 == None

    def test_submit_achievement_ache_error_2(self, init_data):
        """成就值字符串情况"""
        passId = create_random_id()
        url = "http://%s/service/report" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "type": "achv",
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":"55","taskId":"12","tradingTime":"%s",''' %
                               (create_random_id(), passId, create_long_time()) +
                               '''"desc":"1111","code":"sign_in"}]'''}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info(Des.get_passid_distribution(passId))
        logger_print(data, r.json())
        assert r.json()['code'] == 200
        if init_data['db_check']:
            sql = "select * from user_achv_%s where pass_id='%s'" % (Des.get_passid_distribution(passId), passId)
            result1 = init_data['mysql_util'].query_in_time(sql, 10)
            assert result1 == None

    def test_submit_achievement_ache_error_3(self, init_data):
        '''成就值0情况'''
        passId = create_random_id()
        url = "http://%s/service/report" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "type": "achv",
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":0,"taskId":"12","tradingTime":"%s",''' %
                               (create_random_id(), passId, create_long_time()) +
                               '''"desc":"1111","code":"sign_in"}]'''}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info(Des.get_passid_distribution(passId))
        logger_print(data, r.json())
        assert r.json()['code'] == 200
        if init_data['db_check']:
            sql = "select * from user_achv_%s where pass_id='%s'" % (Des.get_passid_distribution(passId), passId)
            result1 = init_data['mysql_util'].query_in_time(sql, 10)
            assert result1 == None

    def test_submit_achievement_ache_error_4(self, init_data):
        '''成就值非正整数情况'''
        passId = create_random_id()
        url = "http://%s/service/report" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "type": "achv",
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":4.6,"taskId":"12","tradingTime":"%s",''' %
                               (create_random_id(), passId, create_long_time()) +
                               '''"desc":"1111","code":"sign_in"}]'''}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info(Des.get_passid_distribution(passId))
        logger_print(data, r.json())
        assert r.json()['code'] == 200
        if init_data['db_check']:
            sql = "select * from user_achv_%s where pass_id='%s'" % (Des.get_passid_distribution(passId), passId)
            result1 = init_data['mysql_util'].query_in_time(sql, 10)
            assert result1 == None

    # def test_submit_achievement_ache_error_4(self, init_data):
    #     '''成就值非正整数情况'''
    #     passId=35
    #     url = "http://%s/service/report" % init_data['env']
    #     data = {"project": "xq",
    #             "requestTime": "%s" % create_long_time(),
    #             "type": "achv",
    #             "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":4.6,"taskId":"12","tradingTime":"%s",'''%
    #                            (create_random_id(),passId, create_long_time())+
    #             '''"desc":"1111","code":"sign_in"}]'''  }
    #     sign = Des.get_sign(data, self.salt)
    #     data['sign'] = sign
    #     r = requests.post(url, data=data)
    #     print(url)
    #     logger.info(Des.get_passid_distribution(passId))
    #     logger_print(data, r.json())
    #     assert r.json()['code']==200

    def test_submit_achievement_no_must_pra(self, init_data):
        '''成就值缺少必填参数'''
        passId = 35
        url = "http://%s/service/report" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "processList": '''[{"projectSN":"%s","passId":"%s","taskId":"12","tradingTime":"%s",''' %
                               (create_random_id(), passId, create_long_time()) +
                               '''"desc":"1111","code":"sign_in"}]'''}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info(Des.get_passid_distribution(passId))
        logger_print(data, r.json())
        assert r.json()['code'] == 4003

    def test_submit_processlist_50(self, init_data):
        '''processlist50个'''
        passId = 35
        url = "http://%s/service/report" % init_data['env']
        list1 = []
        for i in range(55):
            list1.append({"projectSN": "%s" % create_random_id(), "passId": "%s" % passId, "taskId": "12",
                          "tradingTime": "%s" % create_long_time(), "desc": "1111", "code": "sign_in"})
        # a=[{"projectSN":"%s"%create_random_id(),"passId":"%s"%passId ,"taskId":"12","tradingTime":"%s" %create_long_time(),"desc":"1111","code":"sign_in"}]
        processlist = json.dumps(list1)
        processlist = (processlist.replace(' ', ''))
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "type": "achv",
                "processList": processlist}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info(Des.get_passid_distribution(passId))
        logger_print(data, r.json())
        assert r.json()['code'] == 4013

    def test_submit_diff_projectSN(self, init_data):
        '''成就值缺少必填参数'''
        passId = 35
        url = "http://%s/service/report" % init_data['env']
        for i in range(2):
            data = {"project": "xq",
                    "requestTime": "%s" % create_long_time(),
                    "type": "achv",
                    "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":13,"taskId":"12","tradingTime":"%s",''' %
                                   (create_random_id(), passId, create_long_time()) +
                                   '''"desc":"1111","code":"sign_in"}]'''}
            sign = Des.get_sign(data, self.salt)
            data['sign'] = sign
            r = requests.post(url, data=data)
            print(url)
            logger.info(Des.get_passid_distribution(passId))
            logger_print(data, r.json())
        # assert r.json()['code'] == 4013

    def test_select_achievement(self, init_data):
        '''查询成就'''
        passId = self.test_submit_achievement_mul(init_data)
        url = "http://%s/service/User/Achievement" % init_data['env']
        time.sleep(3)
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "passId": str(passId)}
        print("sss:" + str(data))
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.get(url, params=data)
        print(url)
        logger.info(Des.get_passid_distribution(passId))
        logger_print(data, r.json())
        assert r.json()['data']['passId']==str(passId)

    def test_init(self, init_data):
        '''初始化'''
        passId1 = create_random_id()
        global passId_global
        passId_global=passId1
        passId2 = create_random_id()
        url = "http://%s/service/InitAchv" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                #"type": "achv",
                "processList": f'''[{{"passId":"{passId1}","tradingTime":"{create_long_time()}","achv":[{{"code":"gain_gold","tradingValue":10,"projectSN":"{create_random_id()}"}},{{"code":"sign_in","tradingValue":10,"projectSN":"{create_random_id()}"}}]}},{{"passId":"{passId2}","tradingTime":"{create_long_time()}","achv":[{{"code":"sign_in","tradingValue":10,"projectSN":"{create_random_id()}"}},{{"code":"install","tradingValue":10,"projectSN":{create_random_id()}}}]}}]'''
                }
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info("passid_:"+str(passId1)+","+str(Des.get_passid_distribution(passId1)))
        logger.info("passid_:"+str(passId2)+","+str(Des.get_passid_distribution(passId2)))
        logger_print(data, r.json())
        assert r.json()['code'] == 200

    def test_init_0(self, init_data):
        '''初始化,上传trading为0的'''
        passId1 = create_random_id()
        global passId_global
        passId_global = passId1
        passId2 = create_random_id()
        url = "http://%s/service/InitAchv" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                # "type": "achv",
                "processList": f'''[{{"passId":"{passId1}","tradingTime":"{create_long_time()}","achv":[{{"code":"gain_gold","tradingValue":0,"projectSN":"{create_random_id()}"}},{{"code":"sign_in","tradingValue":10,"projectSN":"{create_random_id()}"}}]}},{{"passId":"{passId2}","tradingTime":"{create_long_time()}","achv":[{{"code":"sign_in","tradingValue":10,"projectSN":"{create_random_id()}"}},{{"code":"install","tradingValue":10,"projectSN":{create_random_id()}}}]}}]'''
                }
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info("passid:" + str(passId1) + "," + str(Des.get_passid_distribution(passId1)))
        logger.info("passid:" + str(passId2) + "," + str(Des.get_passid_distribution(passId2)))
        logger_print(data, r.json())
        assert r.json()['code'] == 200


    def test_init_same_project_sn(self, init_data):
        '''相同流水号'''
        passId1 = create_random_id()
        passId2 = create_random_id()
        url = "http://%s/service/InitAchv" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                #"type": "achv",
                "processList": f'''[{{"passId":"{passId1}","tradingTime":"{create_long_time()}","achv":[{{"code":"gain_gold","tradingValue":10,"projectSN":"{passId1}"}},{{"code":"install","tradingValue":10,"projectSN":"{passId1}"}}]}},{{"passId":"{passId2}","tradingTime":"{create_long_time()}","achv":[{{"code":"sign_in","tradingValue":10,"projectSN":"{create_random_id()}"}},{{"code":"install","tradingValue":10,"projectSN":"{create_random_id()}"}}]}}]'''
                }
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info("passid:"+str(passId1)+","+str(Des.get_passid_distribution(passId1)))
        logger.info("passid:"+str(passId2)+","+str(Des.get_passid_distribution(passId2)))
        logger_print(data, r.json())
        assert r.json()['code'] == 200


    def test_init_project_submit_init(self, init_data):
        '''先上报成就，后初始化'''
        self.test_submit_achievement(init_data) #chengjiu
        passId1 = passId_global
        passId2 = create_random_id()
        url = "http://%s/service/InitAchv" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                #"type": "achv",
                "processList": f'''[{{"passId":"{passId1}","tradingTime":"{create_long_time()}","achv":[{{"code":"gain_gold","tradingValue":10,"projectSN":"{create_random_id()}"}},{{"code":"sign_in","tradingValue":10,"projectSN":{create_random_id()}}}]}},{{"passId":"{passId2}","tradingTime":"{create_long_time()}","achv":[{{"code":"sign_in","tradingValue":10,"projectSN":"{create_random_id()}"}},{{"code":"install","tradingValue":10,"projectSN":{create_random_id()}}}]}}]'''
                }
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info("passid:"+str(passId1)+","+str(Des.get_passid_distribution(passId1)))
        logger.info("passid:"+str(passId2)+","+str(Des.get_passid_distribution(passId2)))
        logger_print(data, r.json())
        assert r.json()['code'] == 200


    def test_init_same_project_init_submit(self, init_data):
        '''先初始化，后上报'''
        self.test_init(init_data)
        passId = passId_global
        url = "http://%s/service/report" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "type": "achv",
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":10,"taskId":"12","tradingTime":"%s",''' %
                               (create_random_id(), passId, create_long_time()) +
                               '''"desc":"1111","code":"sign_in"}]'''}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info(str(passId) + "," + str(Des.get_passid_distribution(passId)))
        logger_print(data, r.json())
        assert r.json()['code'] == 200
        if init_data['db_check']:
            sql = "select * from user_achv_%s where pass_id='%s'" % (Des.get_passid_distribution(passId), passId)
            print(sql)
            result1 = init_data['mysql_util'].query_in_time(sql, 15)
            # sql = "select * from userinfo_%s where pass_id='%s'" % (Des.get_passid_distribution(passId), passId)
            # result2 = init_data['mysql_util'].query_in_time(sql, 1)
            date1 = str(datetime.datetime.today())[0:10].replace("-", "")[2:]
            sql = "select * from achv_detail_%s_%s where pass_id='%s'" % (
                date1, Des.get_passid_distribution(passId), passId)
            result3 = init_data['mysql_util'].query_in_time(sql, 1)
            assert result1 != None
            assert result3 != None


    def test_exp_submit(self,init_data):

        passId=create_random_id()
        global exp_passid_global
        exp_passid_global=passId
        url = "http://%s/service/Exp" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":10,"taskId":"12","tradingTime":"%s",''' %
                               (create_random_id(), passId, create_long_time()) +
                               '''"desc":"1111"}]'''}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        logger.info("passid:" + str(passId) + "," + str(Des.get_passid_distribution(passId)))
        r = requests.post(url, data=data)
        logger_print(data, r.json())
        assert r.json()['code']==200

    # def test_exp_select(self, init_data):
    #     '''用户查询'''
    #
    #     url = "http://%s/service/User" % init_data['env']
    #     data = {"project": "xq",
    #             "requestTime": "%s" % create_long_time(),
    #             "passId":"%s" %passId}
    #     sign = Des.get_sign(data, self.salt)
    #     data['sign'] = sign
    #     logger.info("passid:" + str(passId) + "," + str(Des.get_passid_distribution(passId)))
    #     r = requests.get(url, params=data)
    #     logger_print(data, r.json())
    #     assert r.json()['data']['passId']==(passId)



    # def test_roll(self,init_data):
    #     for i in range(10):
    #         self.test_init(init_data)
    #     self.test_submit_achievement_mul(init_data)
    #test_submit_achievement_mul
    # def test_answer(self, init_data):
    #     url = "http://%s/api/achievement" % init_data['env']
    #     data = {"project": "xq",
    #             "requestTime": "%s" % create_long_time()
    #             }
    #     sign = Des.get_sign(data, self.salt)
    #     data['sign'] = sign
    #     print(url)
    #     r = requests.get(url, params=data)
    #     logger_print(data, r.json())
    #     assert 0
