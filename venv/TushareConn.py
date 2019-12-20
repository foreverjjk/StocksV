# coding=utf-8
"""
定义tushare类，用于从tushare获取股票数据
"""
import tushare as ts
import pandas as pd

# 生成常用指数索引
index = {'上证综指': '000001.SH',
         '深证成指': '399001.SZ',
         '沪深300': '000300.SH',
         '创业板指': '399006.SZ',
         '上证50': '000016.SH',
         '中证500': '000905.SH',
         '中小板指': '399005.SZ',
         '上证180': '000010.SH'}
# 获取当前交易的股票代码和名称
# 添加参数，可以获取50，180，300，500
def get_code(pro,INDEX = 'all'):
    # 获取全部上市股票
    if INDEX  == 'all':
        df = pro.stock_basic(exchange='', list_status='L')
        codes = df.ts_code.values
    # 获取上证50
    elif INDEX == '50':
        df = ts.get_sz50s()
        codes = df.code.values
    # 获取沪深300
    elif INDEX == '300':
        df = ts.get_hs300s()
        codes = df.code.values
    # 获取中证500
    elif INDEX == '500':
        df = ts.get_zz500s()
        codes = df.code.values
    # 获取代码和股票名称
    names = df.name.values
    stock = dict(zip(names, codes))
     # 合并指数和个股成一个字典
    stocks = dict(stock, **index)
    return stocks

# 获取全部股票名称
def get_names(pro):
    df = pro.stock_basic(exchange='', list_status='L')
    names = df.name.values
    return names
# 获取每日交易数据
def get_daily_data(stock, start, end, pro):
    # 如果代码在字典index里，则取的是指数数据
    code = get_code(pro,'all')[stock]
    if code in index.values():
        df = pro.index_daily(ts_code=code, start_date=start, end_date=end)
    # 否则取的是个股数据
    else:
        df = pro.daily(ts_code=code, adj='qfq', start_date=start, end_date=end)
    # 将交易日期设置为索引值
    df.index = pd.to_datetime(df.trade_date)
    df = df.sort_index()
    return df

def main():
    token = '3ec0ae8a7b5471f8991b1c97fe07ba5cc4a33ea19a6674a46d6e45b4'
    pro = ts.pro_api(token)
    st = get_code('all')
    for i in st:
        print(i)

if __name__ == '__main__':
    main()