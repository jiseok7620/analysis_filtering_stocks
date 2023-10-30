import pandas as pd
import os
import numpy as np
import csv
import datetime
import matplotlib.pyplot as plt
import mpl_finance

class jisu_grape_cls:
    def exe_jisu_grape(self):
        # 미리 만들어놓은 csv 파일 가져오기
        신호data = pd.read_excel('F:/JusikData/analysis_csv/step/step2/증가감소_1.xlsx', engine='openpyxl')
        
        # 신호데이터의 인덱스
        i = 20
        
        # 종목명과 일자
        dd = 신호data.iloc[i]['기준일']
        name = 신호data.iloc[i]['종목명']
        date = str(dd)[0:4] + '-' + str(dd)[4:6] + '-' + str(dd)[6:8]
        
        
        
        
        
        
        
        # 지수를 데이터 프레임으로 가져오기
        종류 = '코스피지수' # or 코스닥지수
        
        # 지수데이터, 종목데이터 가져오기
        jisudata = pd.read_csv("F:/JusikData/oneday_csv/jisu/" + 종류 + '.csv', encoding='cp949')
        path1 = "F:/JusikData/oneday_csv/onedaydata/"+name+'/'+name+'.csv'
        jongmokdata = pd.read_csv(path1, encoding='cp949')
        print(jisudata.columns)
        print(jongmokdata.columns)
        
        # 해당일자의 인덱스 만들기
        idx = jisudata[jisudata['일자'] == date].index[0]
        idx2 = jongmokdata[jongmokdata['일자'] == dd].index[0]
        
        # 지수와 종목을 넣을 배열만들기
        arr_지수기준 = []
        arr_지수대비 = []
        arr_지수등락률 = []
        arr_종목기준 = []
        arr_종목대비 = []
        arr_종목등락률 = []
        
        # 반복문 카운트
        count_num = 60
        
        while True:
            if count_num == 0:
                break
            
            # 지수 차트 만들기
            지수기준일 = jisudata.iloc[idx-60]['종가']
            지수종가 = jisudata.iloc[idx-count_num]['종가']
            지수선 = 지수종가 / 지수기준일
            arr_지수기준.append(지수선)

            # 종목 차트 만들기
            종목기준일 = jongmokdata.iloc[idx2-60]['종가']
            종목종가 = jongmokdata.iloc[idx2-count_num]['종가']
            종목선 = 종목종가 / 종목기준일
            arr_종목기준.append(종목선)
            
            # 대비와 등락률 넣기
            arr_지수대비.append(jisudata.iloc[idx-count_num]['대비'])
            arr_지수등락률.append(jisudata.iloc[idx-count_num]['등락률'])
            arr_종목대비.append(jongmokdata.iloc[idx2-count_num]['대비'])
            arr_종목등락률.append(jongmokdata.iloc[idx2-count_num]['등락률'])
            
            count_num -= 1
        
        # 나누기
        nanugi_1 = 종목기준일 / 지수기준일
        
        # 지수의 봉 차트구하기위해 시고저종 구하기
        y_data_close_2 = jisudata['종가'].values.tolist()
        y_data_start_2 = jisudata['시가'].values.tolist()
        y_data_high_2 = jisudata['고가'].values.tolist()
        y_data_low_2 = jisudata['저가'].values.tolist()
        
        y_data_close_2 = y_data_close_2[idx-60:idx+1] # 종가
        y_data_start_2 = y_data_start_2[idx-60:idx+1] # 시가
        y_data_high_2 = y_data_high_2[idx-60:idx+1] # 고가
        y_data_low_2 = y_data_low_2[idx-60:idx+1] # 저가
        
        # 종목의 봉 차트구하기위해 시고저종 구하기
        y_data_close = jongmokdata['종가'].values.tolist() / nanugi_1
        y_data_start = jongmokdata['시가'].values.tolist() / nanugi_1
        y_data_high = jongmokdata['고가'].values.tolist() / nanugi_1
        y_data_low = jongmokdata['저가'].values.tolist() / nanugi_1
        
        y_data_close = y_data_close[idx2-60:idx2+1] # 종가
        y_data_start = y_data_start[idx2-60:idx2+1] # 시가
        y_data_high = y_data_high[idx2-60:idx2+1] # 고가
        y_data_low = y_data_low[idx2-60:idx2+1] # 저가
        
        # 캔버스 설정(크기, 배경 설정 등)
        fig = plt.figure(figsize=(15,5)) ## 캔버스 생성
        fig.set_facecolor('white') ## 캔버스 색상 설정
        ax = fig.add_subplot(311) ## 그림 뼈대(프레임) 생성
        ax2 = fig.add_subplot(312)
        ax3 = fig.add_subplot(313)
        
        # 선그래프 그리기
        ax.plot(arr_지수기준, color='black', marker='o', markersize=3)
        ax3.plot(arr_종목기준, color='red', marker='o', markersize=3)
        mpl_finance.candlestick2_ohlc(ax2, y_data_start, y_data_high, y_data_low, y_data_close, width=0.5, colorup='r', colordown='b')
        mpl_finance.candlestick2_ohlc(ax2, y_data_start_2, y_data_high_2, y_data_low_2, y_data_close_2, width=0.5, colorup='green', colordown='black')
        
        # 1에 수평선 긋기
        ax2.axhline(지수기준일,color='green') 
        
        # 그래프 보기
        plt.show()

        # 저장
        #plt.savefig('F:/JusikData/analysis_csv/HJS/img/'+name+'_'+str(dd)+'_roc차트.png')
        
        # 메모리 제거
        plt.close()
        
conn = jisu_grape_cls()
conn.exe_jisu_grape()
        