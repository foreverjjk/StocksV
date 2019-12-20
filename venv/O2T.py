# coding=utf-8
"""
一阳穿三线（多线程）选股策略
"""
import tushare as ts
import numpy as np
import talib as ta
import pandas as pd
from threading import Thread,Lock
import yagmail
import TushareConn as tc
from time import time, sleep
# 正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

class Compare(object):

    def __init__(self):
        self._win = False

    # 比较是否出现一阳线穿13、34、55日均线，同时比较一阳穿三线后成交量是否放大
    def comp_o2t(self,df):
        win = False
        # 取比较数值
        open_price = df.open.values.round(2).tolist()
        close_price = df.close.values.round(2).tolist()
        amount = df.amount.values.tolist()
        df["MA13"] = ta.MA(df.close, timeperiod=13).shift(1)
        df["MA34"] = ta.MA(df.close, timeperiod=34).shift(1)
        df["MA55"] = ta.MA(df.close, timeperiod=55).shift(1)
        ap13 = df.MA13.values.round(2).tolist()
        ap34 = df.MA34.values.round(2).tolist()
        ap55 = df.MA55.values.round(2).tolist()
        # 找出当日最高价穿过当日13、34、55日均线的
        if open_price[-1] < ap13[-1] and open_price[-1] < ap34[-1] and open_price[-1] < ap55[-1]:
             # 找出收盘价格大于13、34、55日均线的
            if close_price[-1] > ap13[-1] and close_price[-1] > ap34[-1] and close_price[-1] > ap55[-1]:
                # 找出成交量大于前一日的1.2倍
                if amount[-1] > amount[- 2] * 1.3:
                    #满足条件，则出现一阳穿三线
                    win = True
        self._win = win

    # 返回信号值
    def get_Win(self):
        return self._win

# 定义线程版本的比较函数
class Check(object):
    # 设定锁，控制全局变量被进程调用
    def __init__(self):
        self._lock = Lock()

    # 将结果写入全局变量，并加锁控制
    def add_signal(self,name):
        self._lock.acquire()
        try:
            stock_1to3.append(name)
        finally:
            self._lock.release()

    # 遍历传入的所有股票
    def check(self,stocks,pro,comp):
        win = False
        for name in stocks:
            try:
                hs = tc.get_daily_data(name, "20190601", "20191210", pro)
                if len(hs) > 55:
                    comp.comp_o2t(hs)
                    win = comp.get_Win()
                    # 将突破股票写入全局函数
                    if win:
                        print(name)
                        print(win)
                        self.add_signal(name)
            except:
                continue

class checkThread(Thread):
    def __init__(self,check,stocks,pro,comp):
        super().__init__()
        self._check = check
        self._stocks = stocks
        self._pro = pro
        self._comp = comp

    # 重写run函数
    def run(self):
        print('run')
        self._check.check(self._stocks,self._pro,self._comp)

def main():
    start = time()
    # 设置tushare的登陆token
    token = '3ec0ae8a7b5471f8991b1c97fe07ba5cc4a33ea19a6674a46d6e45b4'
    pro = ts.pro_api(token)
    # 遍历所有正常交易的股票，选择最近交易日出现一阳穿三线的股票
    stocks = tc.get_names(pro)
    # 定义出现信号的股票列表全局变量
    global stock_1to3
    stock_1to3 = []
    ck = Check()
    comp = Compare()
    thread = []
    i = 0
    print(len(stocks))
    while i < len(stocks):
        # 按100一组，分线程遍历股票
        if i < 3700:
            st = stocks[i:i+200]
            t = checkThread(ck,st,pro,comp)
            t.start()
            #将所有线程加入线程组
            thread.append(t)
            i = i + 200
        # 如果最后一组大于股票数量，则按照股票数量分组
        else :
            st = stocks[3700:]
            t = checkThread(ck,st,pro,comp)
            thread.append(t)
            t.start()
            i = len(stocks)+1
    print(len(thread))
    # 结束所有线程
    for t in thread:
        t.join()
    # 计算运算时间
    end = time()
    print('总共耗费了%.2f秒.' % (end - start))
    print(stock_1to3)

    #设置发件箱
    yag=yagmail.SMTP(user="18538921226@163.com",password="fjjk120826",host="smtp.163.com")
    #设置发送邮件列表
    addresses=["18538921226@163.com","236207045@qq.com","1107241620@qq.com",
           "17757701@qq.com","303896139@qq.com","14618870@qq.com"]
    #发送邮件
    yag.send(addresses,"一阳穿三线",stock_1to3)


if __name__ == '__main__':
    main()











