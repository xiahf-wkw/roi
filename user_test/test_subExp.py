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
    port = ""
    salt = "118test" #118
    salt = "xq_userlevel"  # 226

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



    def test_submit_exp(self, init_data):
        '''正常情况,上报exp'''
        passId=create_random_id()
        url = "http://%s/service/Exp" % init_data['env']
        data = {"project": "ydlm",
                "requestTime": "%s" % create_long_time(),
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":100,"taskId":"12","tradingTime":"%s","desc":"1111"}]'''%
                (create_random_id(),passId, create_long_time())
                }
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger.info(str(passId)+","+str(Des.get_passid_distribution(passId)))
        logger_print(data, r.json())
        assert r.json()['code']==200

    def test_submit_exp_two(self, init_data):
        '''重复上报exp'''
        passId = create_random_id()
        url = "http://%s/service/Exp" % init_data['env']
        data = {"project": "ydlm",
                "requestTime": "%s" % create_long_time(),
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":28,"taskId":"12","tradingTime":"%s","desc":"1111"}]''' %
                               (create_random_id(), passId, create_long_time())
                }
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        print(url)
        logger_print(data, r.json())
        #第二次上报
        data = {"project": "ydlm",
                "requestTime": "%s" % create_long_time(),
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":27,"taskId":"12","tradingTime":"%s","desc":"1111"}]''' %
                               (create_random_id(), passId, create_long_time())
                }
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        logger.info(str(passId) + "," + str(Des.get_passid_distribution(passId)))
        logger_print(data, r.json())
        assert r.json()['code'] == 200

    def test_select_userinfo(self, init_data):
        '''查询用户信息'''
        passId = create_random_id()
        url = "http://%s/service/Exp" % init_data['env']
        data = {"project": "ydlm",
                "requestTime": "%s" % create_long_time(),
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":28,"taskId":"12","tradingTime":"%s","desc":"1111"}]''' %
                               (create_random_id(), passId, create_long_time())
                }
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        #开始查询
        time.sleep(3)
        url = "http://%s/service/User" % init_data['env']
        data = {"project": "ydlm",
                "requestTime": "%s" % create_long_time(),
                "passId": str(passId)}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.get(url, params=data)
        print(url)
        logger.info(Des.get_passid_distribution(passId))
        logger_print(data, r.json())
        assert r.json()['data']['passId'] == int(passId)

    def test_select_userinfo_no_achieve(self, init_data):
        '''查询用户信息,无成就'''
        passId = create_random_id()
        url = "http://%s/service/Exp" % init_data['env']
        data = {"project": "ydlm",
                "requestTime": "%s" % create_long_time(),
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":28,"taskId":"12","tradingTime":"%s","desc":"1111"}]''' %
                               (create_random_id(), passId, create_long_time())
                }
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        #用户成就

        '''上报成就'''
        url = "http://%s/service/report" % init_data['env']
        data = {"project": "ydlm",
                "requestTime": "%s" % create_long_time(),
                "type": "achv",
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":100,"taskId":"12","tradingTime":"%s",''' %
                               (create_random_id(), passId, create_long_time()) +
                               '''"desc":"1111","code":"install"}]'''}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        print(data)
        r = requests.post(url, data=data)
        print(url)
        logger.info(str(passId) + "," + str(Des.get_passid_distribution(passId)))
        logger_print(data, r.json())
        assert r.json()['code'] == 200
        # 开始查询
        time.sleep(3)
        url = "http://%s/service/User" % init_data['env']
        data = {"project": "ydlm",
                "requestTime": "%s" % create_long_time(),
                "passId": str(passId),
                "ignoreAchv":"ignore"
                }

        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.get(url, params=data)
        logger.info("查询")
        logger_print(data, r.json())
        assert r.json()['data']['achievementCount']==0



    def test_select_userinfo_exist_achieve(self,init_data):
        '''查询用户信息,无成就'''
        passId = create_random_id()
        url = "http://%s/service/Exp" % init_data['env']
        data = {"project": "ydlm",
                "requestTime": "%s" % create_long_time(),
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":28,"taskId":"12","tradingTime":"%s","desc":"1111"}]''' %
                               (create_random_id(), passId, create_long_time())
                }
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.post(url, data=data)
        # 用户成就

        '''上报成就'''
        url = "http://%s/service/report" % init_data['env']
        data = {"project": "ydlm",
                "requestTime": "%s" % create_long_time(),
                "type": "achv",
                "processList": '''[{"projectSN":"%s","passId":"%s","tradingValue":100,"taskId":"12","tradingTime":"%s",''' %
                               (create_random_id(), passId, create_long_time()) +
                               '''"desc":"1111","code":"install"}]'''}
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        print(data)
        r = requests.post(url, data=data)
        print(url)
        logger.info(str(passId) + "," + str(Des.get_passid_distribution(passId)))
        logger_print(data, r.json())
        assert r.json()['code'] == 200
        # 开始查询
        time.sleep(3)
        url = "http://%s/service/User" % init_data['env']
        data = {"project": "ydlm",
                "requestTime": "%s" % create_long_time(),
                "passId": str(passId),
                #"ignoreAchv": "ignore"
                }

        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.get(url, params=data)
        logger.info("查询")
        logger_print(data, r.json())
        assert r.json()['data']['achievementCount'] == 1

    def test_config(self,init_data):
        '''查询成就配置'''
        url = "http://%s/api/achievement" % init_data['env']
        data = {"project": "xq",
                "requestTime": "%s" % create_long_time(),

                }
        sign = Des.get_sign(data, self.salt)
        data['sign'] = sign
        r = requests.get(url, params=data)
        logger.info("url:"+url)
        logger_print(data, r.json())
        print (r.json()['data']['achievement'][0])