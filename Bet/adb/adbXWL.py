import os
import time
import random
import datetime
import requests
import math
import random
import re
from lxml import etree
import multiprocessing
import threading
from decorate import wheWrong


from logfile import logger

inputTapCMD = "adb shell input tap 410 1600"


confirmCMD = "adb shell input tap 800 675"
# 微信端

# confirmCMD = "adb shell input tap 800 590"
# APP端

# 10s封单,50s下注
reflashCMD = "adb shell input tap 300 1825"

class ADB(object):
    """docstring for ADB"""



    def __init__(self, ):
        super(ADB, self).__init__()
        pass

    def getResult(self):
        '''
        判断是否出奖了,获得特码的值
        :return:
        '''
        html = requests.post("http://xwl.na81p.cn/txwldd88x85lin/getOpeninfo?random={}".format(random.random()),headers=headers)
        # 单次结果
        html.encoding = 'utf-8'
        if html.status_code == 200:
            returnData = html.json()
            result =  returnData.get("info6")
            return result

    def buyList(self):
        '''
        个人的购买清单,判断是否购买成功
        :return: 期数和余额
        '''
        html = requests.post("http://xwl.na81p.cn/txwldd88x85lin/getZxinfo?random={}".format(random.random()),headers=headers,cookies=self._cookie)
        # 个人信息
        if html.status_code == 200:
            returnData = html.json()

            newest = returnData.get('buylist')[0]
            period = newest.get("issue")
            status = newest.get("pstatus")
            # 下注成功 ==> 撤销

            # last = returnData.get('buylist')[1]
            # period = last.get("issue")
            # status = last.get("pstatus")
            # 中奖或者未中奖

            return period,returnData.get('umoney')
            # 所剩余额

    def getPeriod(self):
        '''
        获得当前出奖的期数
        :return:
        '''
        url = 'http://xwl.si53w.cn/txwldd88x85lin/indexdd88fom?randoms=0.4249590995851321&choosemode=tema'
        html =requests.get(url=url,headers=headers,cookies=self._cookie)
        content = html.text
        tree = etree.HTML(content)
        period = tree.xpath('//*[@id="issue1info"]/text()')[0]
        return int(period)


    def choose(self):
        '''
        用ADB模拟点击选的码
        :return:
        '''
        choiceStategy = random.sample(choice.keys(),9)
        logger.info(choiceStategy)
        # 随机生成的策略
        for i in choiceStategy:
            XY = choice.get(i)
            x,y = XY
            os.popen("adb shell input tap {} {}".format(x,y))
            time.sleep(0.25)
        # 8--2s


    def ADBstart(self):
        '''
        ADB模拟操作,选码,押注,确认
        :return:
        '''
        global nowPeriod



        while True:
            # 等出奖结果出来再操作
            s = getResult()
            if s:
                result = re.findall('特(\d+)',s)
                if result:
                    break
            else:
                time.sleep(1.5)

        t = random.randint(1,5)
        time.sleep(t)
        # 比较简陋的做法
        # time.sleep(10)
        # t = random.randint(0,3)
        # time.sleep(t)
        # os.popen(reflashCMD)
        # time.sleep(2)
        # 在38s左右时,开奖结果知晓


        period , leftValue =  self.buyList()
        leftValue= float(leftValue) 
        if leftValue >= 2000:
            submit_info(KEY,'余额超过2000,请提早体现!~')
            time.sleep(10)
            exit(0)

        self.value = math.floor(leftValue/ 2 / 9)
        if self.value < 1 and self.value > 0:
            self.value = 1
        elif self.value <= 0:
            submit_info(KEY,'''余额不足,请充值!~\r\n
            目前金额**{}**'''.format(leftValue))

        if period == nowPeriod:
            # 两次失败,就关闭
            self.cnt += 1
            if self.cnt == 3:
                submit_info(KEY,'''程序出错!!\r\n
            目前金额**{}**'''.format(leftValue))
                time.sleep(5)
                exit(0)

        inputValueCMD = "adb shell input text {}".format(self.value)
        choose()
        os.popen(inputTapCMD)
        time.sleep(1)
        os.popen(inputValueCMD)
        time.sleep(1.5)
        os.popen(confirmCMD)
        time.sleep(1.5)


        os.popen("adb shell input swipe 550 555 550 1650 300")
        # 拖动置顶 , 方便下次操作
        time.sleep(42-t)
        # 一轮结束
        logger.info("{},第{}期,一轮结束".format(str(datetime.datetime.now() )[:-7] , period))

        nowPeriod = period

