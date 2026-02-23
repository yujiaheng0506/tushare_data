import os
import tushare as ts
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("Tushare_token")
print(token)
pro = ts.pro_api(token=token)
print("Tushare接口初始化成功")
df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
df.to_csv("股票列表.csv")