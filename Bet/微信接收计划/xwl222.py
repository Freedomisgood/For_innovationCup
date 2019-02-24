import os
import time
import random
import datetime
import requests
import math
import random
import re
from lxml import etree
import threading
import itchat
import multiprocessing
from requests.exceptions import ConnectTimeout
from decorate import wheWrong

from logfile import logger

# import sys
# path = os.path.abspath(__file__) #获取当前文件的绝对路径
# envPath = os.path.dirname(path)
# sys.path.append(envPath)
# logger.info(os.environ)

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; MI 6 Build/OPR1.170623.027; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0',
    # 'Connection': 'keep-alive',
}


DOMAIN = 'xgeba'
# 大号

cookieList = [
    # dqf二级
    {
        'uid': 'd71bab2309a9f9c611a6ce761ff74d6b',
        'nickname': '5b+D6Iul5piT5Ya3'
    },

    # 三级 , 带头像的果粒橙
    {
        'uid': '800927a30d6f90917584d103ba7909bc',
        'nickname': '5p6c57KS5qmZ'
    },
    #  二级mrli
    {
        'uid': '54bdd5b6b3462281bb376fd62dfb1d91',
        'nickname': '"TXJsaQ=="'
    },
    # 一级
    {
        'uid': '05511d07e17b8bf765a9f09523286402',
        'nickname': '"5p6c57KS5qmZeno="'
    }
]
# cookies = cookieList[0]

KEY = 'SCU35113Te369cebc21f6e483c03fffc400c4c5c05bdad63995c32'

nowPeriod = 0


def submit_info(secret_key, content):
    '''
    用ServerChan发送消息
    :param secret_key: 秘钥
    :param content: 发送的内容
    :return: None
    '''
    data_info = {
        'text': '新未来',
        'desp': content
    }
    requests.post(url='https://sc.ftqq.com/{}.send'.format(secret_key), data=data_info)


choice = {
    # 左右选项间隔为185
    '0': [165, 1200],
    '1': [350, 1200],
    '2': [535, 1200],
    '3': [720, 1200],
    '4': [905, 1200],
    # 左右选项间隔为185
    '5': [165, 1355],
    '6': [350, 1355],
    '7': [535, 1355],
    '8': [720, 1355],
    '9': [905, 1355],
}

choiceStategy = ['1', '2', '3', '4', '5', '6', '7', '8', '9']  # 8注不亏



def getPeriod():
    '''
    获得当前出奖的期数
    :return:
    '''
    while True:
        url = 'http://xwl.{}.cn/txwldd88x85lin/indexdd88fom?randoms=0.3861611309781524'\
            .format(DOMAIN,random.random())
        # url = 'http://xwl.xgeba.cn/txwldd88x85lin/indexdd88fom?randoms=0.{}&choosemode=tema'
        html = requests.get(url=url, headers=headers, timeout = 6,cookies= {
            'uid': '800927a30d6f90917584d103ba7909bc',
            'nickname': '5p6c57KS5qmZ'
        }
    )
        content = html.text
        tree = etree.HTML(content)
        period = tree.xpath('//*[@id="issue1info"]/text()')
        if period:
            return int(period[0])


def getNums(strData):
    '''
    从字符串中获得要下注的码子
    :param strData:
    :return: list-nums
    '''
    a = strData.split('\n')
    for x in a:
        result = re.findall('(\d+)-\d+ +定个位【(.*?)】 +第(\d+)期', x)
        if result:
            s = str(nowPeriod)[-len(result[0][0]):]
            if result[0][2] == '2' or result[0][2] == '3' or result[0][0] == s:
                return result[0][1] + ','


class CRequest(object):

    def __init__(self, cookie):
        super(CRequest, self).__init__()
        self._cookie = cookie
        # print(self._cookie)
        self._nickname = self._cookie.get("nickname")
        self.judgeaccount()

        self.No0times = 0
        # 0未出现的次数
        self.Nomoney = 0
        # 没钱提醒次数, 为了防止低于9时,不能连续下注

        self.cnt = 0
        self.value = 1  # 每注押注金额

    def judgeaccount(self):
        if self._nickname == '5p6c57KS5qmZ':
            self._account = '3rd:18005187969'
        elif self._nickname == '"TXJsaQ=="':
            self._account = '2nd:15061873738'
        elif self._nickname == '"5p6c57KS5qmZeno="':
            self._account = '1st:18115124951'
        elif self._nickname == '5b+D6Iul5piT5Ya3':
            self._account = '4st:杜琪峰小号'



    @property
    def cookie(self):
        return self._cookie

    @property
    def account(self):
        return self._account

    def getValue(self):
        period, leftValue = self.buyList()
        leftValue = float(leftValue)
        if leftValue >= 300:
            submit_info(KEY, '余额超过300,请提早体现!~')
            time.sleep(10)
            exit(0)

        self.value = math.floor(leftValue / 2 / 9)

        if self.value <= 1:
            self.value = 1
        elif self.value > 3:
            self.value = 3

    @wheWrong
    def getResult(self):
        '''
        判断是否出奖了,获得特码的值
        :return:
        '''
        html = requests.post("http://xwl.{}.cn/txwldd88x85lin/getOpeninfo?random={}".format(DOMAIN,random.random()),
                             headers=headers,timeout = 6)
        # 单次结果
        html.encoding = 'utf-8'
        if html.status_code == 200:
            returnData = html.json()
            result = returnData.get("info6")
            return result

    @wheWrong
    def buyList(self):
        '''
        个人的购买清单,判断是否购买成功
        :return: 期数和余额
        '''
        html = requests.post("http://xwl.{}.cn/txwldd88x85lin/getZxinfo?random={}".format(DOMAIN,random.random()),
                             headers=headers,timeout = 6,cookies=self._cookie)
        # 个人信息
        if html.status_code == 200:
            returnData = html.json()

            newest = returnData.get('buylist')[0]
            period = newest.get("issue")
            status = newest.get("pstatus")
            # 下注成功 ==> 撤销

            return period, returnData.get('umoney')
            # 所剩余额



    def getchoice(self):
        if self.No0times > 5:
            randomChioce = random.sample(choice.keys(), 9)
            randomChioce = sorted(randomChioce)
        else:
            randomChioce = choiceStategy
        Fchoice = ','.join(randomChioce) + ','
        return Fchoice

    @wheWrong
    def completepost(self):
        '''
        完成post的请求,买单
        :param self.value: 注数
        :return: NULL
        '''
        # global choice
        randomChioce = self.getchoice()
        # print(randomChioce)
        logger.info("下注{}".format(randomChioce))
        global  nowPeriod
        postdata = {
            'issue2': nowPeriod,
            'chooseinfo': randomChioce,
            'choosenums': int(len(randomChioce) / 2),  # 除去逗号
            'mons': self.value,
            'mode': 15,
            'buytype': 1,
            'random': random.random()
        }

        html = requests.post('http://xwl.{}.cn/txwldd88x85lin/savesinfo'.format(DOMAIN),
                             headers=headers,timeout = 6,cookies=self._cookie, data=postdata)
        data = html.json()
        msg = data.get('rtmsg')
        umoney = data.get('umoney')
        logger.info("账号{} , 第{}期{}目前余额为 **{}**\n".
                    format(self._account, nowPeriod, msg, umoney))
        if msg == '本期已封单！':
            time.sleep(10)
        elif msg == '购买成功！':
            time.sleep(40 + random.randint(0, 5))
        elif msg == '余额不足！':
            self.Nomoney += 1
            # print(self.Nomoney)
            if self.Nomoney == 2:
                # print('no')
                submit_info(KEY, '## 账号{}\r\n####余额不足,请充值!~\r\n目前金额 **{}**'.format(self._account, umoney))

            while True:
                period, leftValue = self.buyList()
                # print(leftValue)
                if math.floor(float(leftValue)) > 8:
                    break
                else:
                    time.sleep(120)
            # 如果金额不足,则一直卡死
        elif msg == '购买失败,本期号码不能全买！':
            logger.debug(msg)
            time.sleep(35)
        else:
            print(postdata)
            time.sleep(20)

    def postway(self):
        '''
        使用POST请求完成下注
        :return:
        '''

        while True:
            # 等出奖结果出来再操作
            s = self.getResult()
            if s:
                result = re.findall('特(\d+)', s)
                # print(result)
                if result:
                    if result[0] == '0':
                        self.No0times = 0
                    else:
                        self.No0times += 1
                    break
            else:
                time.sleep(1.5)

        t = random.randint(1, 5)
        time.sleep(t)

        self.getValue()

        self.completepost()
        # time.sleep(40-t)

    def run(self):
        for x in range(30):
            for y in range(25):
                logger.info("第{}轮:".format(y + 1))
                self.postway()
            logger.info("-" * 20)

            period, leftValue = self.buyList()
            submit_info(KEY, '#### {}一周期结束!休息{}s~\r\n目前金额 **{}**'.format(self._nickname, restTime, leftValue))
            restTime = random.randint(300, 1000)
            time.sleep(restTime)

        period, leftValue = self.buyList()
        submit_info(KEY, '#### 计划完成!~\r\n目前金额 **{}**'.format(leftValue))


# nomoney = False
class CCaim(CRequest):
    """docstring for ClassName"""

    def __init__(self, cookie,valuethod):
        super(CCaim, self).__init__(cookie)
        self.Nums = '1,2,3,4,5,6,7,8,9,'
        self.valuethod = valuethod

    @property
    def cookie(self):
        return self._cookie

    def getValue(self):
        period, leftValue = self.buyList()
        leftValue = float(leftValue)
        if leftValue >= 300:
            submit_info(KEY, '余额超过300,请提早体现!~')
            time.sleep(10)
            exit(0)
        self.value = math.floor(leftValue / 2 / 9)
        if self.value <= 1:
            self.value = 1
        if self.value > self.valuethod:
            self.value = self.valuethod




    @wheWrong
    def completepost(self):
        '''
        完成post的请求,买单
        :param self.value: 注数
        :return: NULL
        '''
        # global choice
        randomChioce = self.getchoice()
        # print(randomChioce)
        logger.info("下注{}".format(randomChioce))

        global  nowPeriod
        postdata = {
            'issue2': nowPeriod,
            'chooseinfo': randomChioce,
            'choosenums': int(len(randomChioce) / 2),  # 除去逗号
            'mons': self.value,
            'mode': 15,
            'buytype': 1,
            'random': random.random()
        }
        html = requests.post('http://xwl.{}.cn/txwldd88x85lin/savesinfo'.format(DOMAIN),
                             headers=headers,timeout = 6,cookies=self._cookie, data=postdata)
        data = html.json()
        msg = data.get('rtmsg')
        umoney = data.get('umoney')
        logger.info("账号{} , 第{}期{}目前余额为 **{}**\n".format(self._account, nowPeriod, msg, umoney))
        if msg == '余额不足！':
            submit_info(KEY, '## 账号{}\r\n####余额不足,请充值!~\r\n目前金额 **{}**'.format(self._account, umoney))

    def getchoice(self):
        return self.Nums

    def run(self):
        self.postway()


if __name__ == '__main__':
    times = 0
    thold = 5

    itchat.auto_login()
    # itchat.auto_login(enableCmdQR=2)


    @itchat.msg_register(itchat.content.TEXT)
    def msg_reply(msg):
        print('*' * 10 + '收到信息' + '*'*10)
        # 三个账号
        # time.sleep(5)
        global nowPeriod
        nowPeriod = getPeriod() + 1
        # print(nowPeriod)

        fenfencai = getNums(msg['Text'])
        print(fenfencai)
        if fenfencai:
            for i in range(1, 4):
                global times
                caimin = CCaim(cookieList[i],valuethod=5)
                caimin.Nums = fenfencai
                if caimin.Nums:
                    print("分分彩", caimin.Nums)
                    # 如果不符合该项目的信息,不会启动
                    times += 1
                    _, leftmoney = caimin.buyList()
                    if float(leftmoney) < thold:
                        print('{} : nomoney'.format(caimin._account))
                        # submit_info(KEY, '## 账号{}\r\n####余额不足,请充值!~\r\n目前金额 **{}**'.format(caimin._account,leftmoney))
                        continue

                    if times % 20 == 0:
                        continue
                    t = threading.Thread(target=caimin.run(), args=())
                    t.start()


    itchat.run()
