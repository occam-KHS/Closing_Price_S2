import FinanceDataReader as fdr
import pandas as pd
import numpy as np
import datetime

def select_stocks(today_dt):
    
    today = datetime.datetime.strptime(today_dt, '%Y-%m-%d')
    start_dt = today - datetime.timedelta(days=365) # 100 일전 데이터 부터 시작 - 피쳐 엔지니어링은 최소 60 개의 일봉이 필요함
    start_dt = start_dt.strftime('%Y-%m-%d')
    print(start_dt, today_dt)

    kosdaq_list = pd.read_pickle('kosdaq_list.pkl')

    code_list = []

    for code, name in zip(kosdaq_list['code'], kosdaq_list['name']):  # 코스닥 모든 종목에서 대하여 반복
        daily_price = fdr.DataReader(code, start=start_dt, end=today_dt)  # 종목, 일봉, 데이터 갯수
        highest = daily_price['High'].quantile(0.95)
        today_close = daily_price['Close'][-1]
        today_open = daily_price['Open'][-1]
        today_high = daily_price['High'][-1]
        today_vol = daily_price['Volume'][-1]
        prev_vol = daily_price['Volume'][-2]

        if daily_price.index[-1].strftime('%Y-%m-%d') != today_dt:
            continue

        c1 = (prev_vol>0)*(today_vol > 0).astype('int')
        c2 = (today_close > highest).astype('int')
        c3 = (today_vol > prev_vol * 3.5).astype('int')
        c4 = (today_open < today_close).astype('int')
        c5 = ((today_high / today_close) < 1.01).astype('int')

        if c1 & c2 & c3 & c4 & c5:
            print(code)
            code_list.append(code)

    return code_list