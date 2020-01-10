import logging
import logconfig
logger = logging.getLogger(__file__)  # 生成logger实例
def logger_print(req,resp):
    logger.info("【请求报文】:"+str(req))
    logger.info("【响应报文】:"+str(resp))