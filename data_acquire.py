import os
import tushare as ts
import pandas as pd
from dotenv import load_dotenv
import schedule
import time as time_module  
from tqdm import tqdm

class StockDownloader:
    def __init__(self, output_dir='股票历史行情日线数据'):
        load_dotenv()
        self.token = os.getenv("Tushare_token")
        self.output_dir = output_dir
        self.pro = self._auth()
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f'目录 {self.output_dir} 创建成功')
    """下载股票列表"""        
    def download_stock_list(self):
        df = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        df.to_csv("股票列表.csv", index=False, encoding='utf-8-sig')

    def _auth(self):
        try:
            return ts.pro_api(token=self.token)
        except Exception as e:
            print(f"Tushare 认证失败: {e}")
            return None
    """下载x日到当前的历史行情数据"""    
    def download_all_history(self, sleep_time=0.5, start_date='', end_date=''):
        """执行下载"""
        df = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        df.to_csv("股票列表.csv", index=False, encoding='utf-8-sig')
        stock_list = df['ts_code']
        
        print(f"开始下载，共计 {len(stock_list)} 只股票...")

        for stock in tqdm(stock_list,desc="同步行情", unit="stock"):
            try:
                stock_price = self.pro.daily(
                    ts_code=stock,
                    start_date=start_date,
                    end_date=end_date,
                    fields="ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount"
                )
                
                file_path = os.path.join(self.output_dir, f"{stock}.csv")
                stock_price.to_csv(file_path, index=False, encoding='utf-8-sig')
                tqdm.write(f"股票{stock}数据已获取")
                time_module.sleep(sleep_time)
            except Exception as e:
                print(f"股票 {stock} 下载出错: {e}")
                continue

    def download_all_daily(self,sleep_time=0.5,start_date = '',end_date=''):
        df = pd.read_csv('股票列表.csv')
        stock_list = df['ts_code']
        for stock in tqdm(stock_list,desc="同步行情", unit="stock"):
            try:
                stock_price = self.pro.daily(
                    ts_code=stock,
                    start_date=start_date,
                    end_date=end_date,
                    fields="ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount"
                )
                
            except Exception as e:



        print("所有数据下载任务完成。")

if __name__ == "__main__":
    downloader = StockDownloader()
    downloader.download_all_history (sleep_time=0.3,start_date ='20210302',end_date = '20260302')
