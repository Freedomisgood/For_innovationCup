# encoding: utf-8

from logfile import logger

"""
避免requests请求失败
"""


def wheWrong(func):
    def wrapper(self,*args, **kwargs):
        try:
            return func(self,*args, **kwargs)
        except Exception as e:
        	logger.debug(e)
            # submit_info(KEY,'程序出错:{} \n目前金额 **{}**'.format(e,leftValue))
        else:
            pass
    return wrapper
