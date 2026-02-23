import os
import tushare as ts
import pandas as pd
from dotenv import load_dotenv
import schedule
import time
os.makedirs('股票历史行情日线数据')
load_dotenv()
token = os.getenv("Tushare_token")
pro = ts.pro_api(token=token)
df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
df.to_csv("股票列表.csv")
stock_list = df['ts_code']
print(stock_list)
for stocks in stock_list:
    stock_price = pro.stock_basic(**{
    "ts_code": "{stocks}",
    "name": "",
    "exchange": "",
    "market": "",
    "is_hs": "",
    "list_status": "",
    "limit": "",
    "offset": ""
}, fields=[
    "ts_code",
    "symbol",
    "name",
    "area",
    "industry",
    "cnspell",
    "market",
    "list_date",
    "act_name",
    "act_ent_type"
])
    stock_price.to_csv(f"股票历史行情日线数据/{stocks}.csv", index=False, encoding='utf-8-sig')
    print(f"已获取股票{stocks}的历史行情数据")
    time.sleep(3)
