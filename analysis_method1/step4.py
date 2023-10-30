import pandas as pd
import os
import numpy as np
import datetime
import mpl_finance
import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image
from pandas_datareader import data as pdr # pip install pandas-datareader
import yfinance as yf # pip install yfinance

# 월봉차트 만들기

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
        
        data1 = pdr.get_data_yahoo("005930.KS", start=st_year + '-' + st_month + '-' + st_day, end=en_year + '-' + en_month + '-' + en_day)
        data1['일자'] = data1.index
        #print(data1)
        
        ## data3 = 수급데이터 ##
        path3 = "F:/JusikData/oneday_csv/onedaydata_supply/"+name+'.csv'
        data3 = pd.read_csv(path3, encoding='cp949')
        print(data3.columns)
        
        
        ##------------------------------------------------------------------##
        ## 그룹 만들기
        data1['그룹'] = data1['일자'].astype(str) # 일자를 문자열로 만들기
        #print(data1.iloc[0])
        
        data1['그룹'] = data1['그룹'].str[0:7] # 년/월로 그룹 만들기
        #print(data1.iloc[0])
        
        ## 그룹화하기
        data_group = data1.groupby(data1['그룹'])
        #print(data_group.size())
        
        ## 시고저종, 거래량 구하기
        data_trade = data_group[['Volume']].agg(['sum', 'max', 'min']) # 거래량, 합 / 최고 / 최저
        data_max = data_group[['High']].agg(['max'])
        data_min = data_group[['Low']].agg(['min']) # 저가, 최저가
        data_first = data1.drop_duplicates(['그룹'], keep="first")
        data_first = data_first[['Open','그룹']]
        data_last = data1.drop_duplicates(['그룹'], keep="last")
        data_last = data_last[['Close', '그룹']]
        
        ## 월봉 데이터프레임 만들기
        data_month = pd.merge(data_trade,data_max, how='outer', on=['그룹'])
        data_month = pd.merge(data_month,data_min, how='outer', on=['그룹'])
        data_month = pd.merge(data_month,data_first, how='outer', on=['그룹'])
        data_month = pd.merge(data_month,data_last, how='outer', on=['그룹'])
        data_month.columns = ['그룹', '거래량합', '거래량최대', '거래량최소', '고가', '저가', '시가', '종가']
        #print(len(data_month))
        #print(data_month['거래량합'])
        #print(data_month.columns)
        
        
        
        ##------------------------------------------------------------------##
        ## 수급 표현하기
        data3 = data3.fillna(0) # nan 값을 0으로 바꾸기
        data3['기관'] = data3['금융투자'] + data3['보험'] + data3['투신'] + data3['사모'] + data3['은행'] + data3['기타금융'] + data3['연기금 등']
        
        # 일정기간만 추출
        st_idx = data3[data3['일자'] == st_year + '/' + st_month + '/' + st_day].index[0]
        en_idx = data3[data3['일자'] == en_year + '/' + en_month + '/' + en_day].index[0]
        data3 = data3[st_idx:en_idx]
        
        ## 그룹 만들기
        data3['그룹'] = data3['일자'].astype(str) # 일자를 문자열로 만들기
        #print(data3.iloc[0])
        
        data3['그룹'] = data3['그룹'].str[0:7] # 년/월로 그룹 만들기
        #print(data3.iloc[0])
        
        ## 그룹화하기
        data_group2 = data3.groupby(data3['그룹'])
        
        ## 기관, 개인, 외국인, 기타법인 거래량 합 구하기
        data_trade1 = data_group2[['개인']].agg(['sum'])
        data_trade2 = data_group2[['외국인']].agg(['sum'])
        data_trade3 = data_group2[['기관']].agg(['sum'])
        data_trade4 = data_group2[['기타법인']].agg(['sum'])
        
        ## 월봉 데이터프레임 만들기
        data_how = pd.merge(data_trade1,data_trade2, how='outer', on=['그룹'])
        data_how = pd.merge(data_how,data_trade3, how='outer', on=['그룹'])
        data_how = pd.merge(data_how,data_trade4, how='outer', on=['그룹'])
        data_how.columns = ['개인', '외국인', '기관', '기타법인']
        
        
        ##------------------------------------------------------------------##
        ## 그래프 그리기
        # 캔버스 설정(크기, 배경 설정 등)
        fig = plt.figure(figsize=(40,25)) ## 캔버스 생성
        fig.set_facecolor('white') ## 캔버스 색상 설정
        
        # 그림 뼈대(프레임) 생성 
        #차트 : 월봉차트
        ax = fig.add_subplot(421)
        mpl_finance.candlestick2_ohlc(ax, data_month['시가'], data_month['고가'], data_month['저가'], data_month['종가'], width=0.5, colorup='r', colordown='b')
        plt.xticks(visible=False) # 축값없애기
        plt.grid(True, axis='y') # 그리드(격자)
        
        # 차트 : 거래량차트
        # 1. 거래량 바 차트
        ax2 = fig.add_subplot(425)
        plt.bar(range(len(data_month)), data_month['거래량합'])
        
        # 2. 수급 거래량 차트(개인)
        ax3 = fig.add_subplot(422)
        plt.bar(range(len(data_how)), data_how['개인'])
        
        # 3. 수급 거래량 차트(외국인)
        ax4 = fig.add_subplot(424)
        plt.bar(range(len(data_how)), data_how['외국인'])
        
        # 4. 수급 거래량 차트(기관)
        ax5 = fig.add_subplot(426)
        plt.bar(range(len(data_how)), data_how['기관'])
        
        # 5. 수급 거래량 차트(기타법인)
        ax6 = fig.add_subplot(428)
        plt.bar(range(len(data_how)), data_how['기타법인'])
        
        # 그림보기
        plt.show()
        
        # 메모리제거
        plt.close()
        
        
conn = met1_step3_cls()
conn.exe_step3('에이치엘비')
