import pandas as pd
import os
import numpy as np
import datetime
import mpl_finance
import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image
from pandas_datareader import data
from pandas_datareader import data as pdr # pip install pandas-datareader
import yfinance as yf # pip install yfinance

# 일봉차트 만들기

class met1_step3_cls():
    def exe_step3(self,name):
        ## 추출 시작일, 종료일 설정
        st_year = '2015'
        st_month = '01'
        st_day = '02'
        en_year = '2021'
        en_month = '11'
        en_day = '02'
        
        ## 야후 API로 데이터 가져오기
        yf.pdr_override()
        
        #start=st_year + '-' + st_month + '-' + st_day, end=en_year + '-' + en_month + '-' + en_day
        #data1 = pdr.get_data_yahoo("028300.KQ", start="2015-01-01", end="2020-01-01")
        data1 = data.DataReader('028300.KQ','yahoo','2016-07-04','2020-01-01')
        data1['일자'] = data1.index
        print(data1)
        
        ## data3 = 수급데이터 ##
        path3 = "F:/JusikData/oneday_csv/onedaydata_supply/"+name+'.csv'
        data3 = pd.read_csv(path3, encoding='cp949')
        
        # 수급데이터 정제
        data3 = data3.fillna(0) # nan 값을 0으로 바꾸기
        data3['기관'] = data3['금융투자'] + data3['보험'] + data3['투신'] + data3['사모'] + data3['은행'] + data3['기타금융'] + data3['연기금 등']
        print(data3.columns)
        
        # 일정기간만 추출
        st_idx = data3[data3['일자'] == st_year + '/' + st_month + '/' + st_day].index[0]
        en_idx = data3[data3['일자'] == en_year + '/' + en_month + '/' + en_day].index[0]
        data3 = data3[st_idx:en_idx]
        
        
        
        ##------------------------------------------------------------------##
        ## 그래프 그리기
        # 캔버스 설정(크기, 배경 설정 등)
        fig = plt.figure(figsize=(40,25)) ## 캔버스 생성
        fig.set_facecolor('white') ## 캔버스 색상 설정
        
        # 그림 뼈대(프레임) 생성 
        #차트 : 월봉차트
        ax = fig.add_subplot(421)
        mpl_finance.candlestick2_ohlc(ax, data1['Open'], data1['High'], data1['Low'], data1['Close'], width=0.5, colorup='r', colordown='b')
        plt.xticks(visible=False) # 축값없애기
        plt.grid(True, axis='y') # 그리드(격자)
        
        # 차트 : 거래량차트
        # 1. 거래량 바 차트
        ax2 = fig.add_subplot(425)
        plt.bar(range(len(data1)), data1['Volume'])
        
        # 2. 수급 거래량 차트(개인)
        ax3 = fig.add_subplot(422)
        plt.bar(range(len(data3)), data3['개인'])
        
        # 3. 수급 거래량 차트(외국인)
        ax4 = fig.add_subplot(424)
        plt.bar(range(len(data3)), data3['외국인'])
        
        # 4. 수급 거래량 차트(기관)
        ax5 = fig.add_subplot(426)
        plt.bar(range(len(data3)), data3['기관'])
        
        # 5. 수급 거래량 차트(기타법인)
        ax6 = fig.add_subplot(428)
        plt.bar(range(len(data3)), data3['기타법인'])
        
        # 그림보기
        plt.show()
        
        # 메모리제거
        plt.close()
        
conn = met1_step3_cls()
conn.exe_step3('에이치엘비')
