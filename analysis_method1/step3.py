import pandas as pd
import os
import numpy as np
import datetime
import mpl_finance
import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image

# 로컬에 저장된 데이터로 월봉 그리기

class met1_step3_cls():
    def exe_step3(self,name):
        ## data1 = 개별 종목 데이터 ##
        path1 = "F:/JusikData/oneday_csv/onedaydata/"+name+'/'+name+'.csv'
        data1 = pd.read_csv(path1, encoding='cp949')
        print(data1.columns)
        
        ## data3 = 수급데이터 ##
        path3 = "F:/JusikData/oneday_csv/onedaydata_supply/"+name+'.csv'
        data3 = pd.read_csv(path3, encoding='cp949')
        
        ## 그룹 만들기
        data1['그룹'] = data1['일자'].astype(str) # 일자를 문자열로 만들기
        #print(data1.iloc[0])
        
        data1['그룹'] = data1['그룹'].str[0:6] # 년/월로 그룹 만들기
        #print(data1.iloc[0])
        
        ## 그룹화하기
        data_group = data1.groupby(data1['그룹'])
        #print(data_group.size())
        
        ## 시고저종, 거래량 구하기
        data_trade = data_group[['거래량']].agg(['sum', 'max', 'min']) # 거래량, 합 / 최고 / 최저
        data_max = data_group[['고가']].agg(['max'])
        data_min = data_group[['저가']].agg(['min']) # 저가, 최저가
        data_first = data1.drop_duplicates(['그룹'], keep="first")
        data_first = data_first[['시가','그룹']]
        data_last = data1.drop_duplicates(['그룹'], keep="last")
        data_last = data_last[['종가', '그룹']]
        
        ## 월봉 데이터프레임 만들기
        data_month = pd.merge(data_trade,data_max, how='outer', on=['그룹'])
        data_month = pd.merge(data_month,data_min, how='outer', on=['그룹'])
        data_month = pd.merge(data_month,data_first, how='outer', on=['그룹'])
        data_month = pd.merge(data_month,data_last, how='outer', on=['그룹'])
        data_month.columns = ['그룹', '거래량합', '거래량최대', '거래량최소', '고가', '저가', '시가', '종가']
        print(len(data_month))
        print(data_month['거래량합'])
        print(data_month.columns)
        
        
        
        ##------------------------------------------------------------------##
        ## 그래프 그리기
        # 캔버스 설정(크기, 배경 설정 등)
        fig = plt.figure(figsize=(40,25)) ## 캔버스 생성
        fig.set_facecolor('white') ## 캔버스 색상 설정
        
        # 그림 뼈대(프레임) 생성 
        #차트 : 월봉차트
        ax = fig.add_subplot(211)
        mpl_finance.candlestick2_ohlc(ax, data_month['시가'], data_month['고가'], data_month['저가'], data_month['종가'], width=0.5, colorup='r', colordown='b')
        plt.xticks(visible=False) # 축값없애기
        plt.grid(True, axis='y') # 그리드(격자)
        
        # 차트7 : 거래량차트
        # 거래량 바 차트
        ax2 = fig.add_subplot(212)
        plt.bar(range(len(data_month)), data_month['거래량합'])
        
        # 그림보기
        plt.show()
        
        # 메모리제거
        plt.close()
        
conn = met1_step3_cls()
conn.exe_step3('에이치엘비')
