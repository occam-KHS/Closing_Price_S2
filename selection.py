import FinanceDataReader as fdr
import pandas as pd
import numpy as np
import datetime

kosdaq_list = pd.read_pickle('kosdaq_list.pkl')

def select_stocks(today_dt):
    
    today = datetime.datetime.strptime(today_dt, '%Y-%m-%d')
    start_dt = today - datetime.timedelta(days=120)
    start_dt = start_dt.strftime('%Y-%m-%d')
    print(start_dt, today_dt)

    code_list = []

    for code, name in zip(kosdaq_list['code'], kosdaq_list['name']):  # 코스닥 모든 종목에서 대하여 반복

        df = fdr.DataReader(code, start = today_dt, end = today_dt)
        if (len(df) == 0) or (df['Open'][-1] == 0) or ((df['Close'][-1]/df['Open'][-1]) < 1.05) or (df.index[-1].strftime('%Y-%m-%d') != today_dt) or ('스팩' in name):
            continue

        daily_price = fdr.DataReader(code, start=start_dt, end=today_dt)  # 종목, 일봉, 데이터 갯수

        highest = daily_price['High'].quantile(0.95)
        today_close = daily_price['Close'][-1]
        today_high = daily_price['High'][-1]
        today_vol = daily_price['Volume'][-1]
        prev_vol = daily_price['Volume'][-2]

        c1 = (prev_vol>0)*(today_vol > 0).astype('int')
        c2 = (today_close > highest).astype('int')
        c3 = (today_vol > prev_vol * 2.5).astype('int')
        c4 = ((today_high / today_close) < 1.005).astype('int')

        print(code, c1, c2, c3, c4)
        if c1 & c2 & c3 & c4:
            code_list.append(code)

    return code_list