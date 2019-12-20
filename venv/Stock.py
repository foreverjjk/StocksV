# coding=utf-8
"""
定义stock类,包括name,code
定义静态类函数fix，补全未输入的代码或者股票
"""
class Stock(object):

    def __init__(self,name,code):
        #获取股票名称,代码
        self._name = name
        self._code = code

    @classmethod
    #补全不完整的或者错误的代码和名称
    def fix(cls,name,code):
        #补全股票名称或代码
        if name == "":
            name = "中国平安"
            #cls._name = ts.getName(cls._code)，通过代码查找名称
        if code == "":
            code = "601318"
            # cls._code = ts.getCode(cls._name)，通过代码查找名称
        return cls(name,code)

    """定义数据更新函数,需要输入起始日期和终止日期，以及更新来源
    DB(database)和TS(tushare)
    """
    def update(self,startdate,enddate,method = "DB"):
        pass

    #定义获取name函数
    def getName(self):
        return self._name

    # 定义获取code函数
    def getCode(self):
        return self._code

    #定义获取价格的函数
    def getPrice(self):
        pass

    #定义获取真实波动值的函数，需要输入时间区间
    def getATR(self,period = 20):
        pass

    #定义获取均值的函数，需要输入时间区间
    def getMean(self,period = 5):
        pass

    #定义获取成交量的函数
    def getAmount(self):
        pass



