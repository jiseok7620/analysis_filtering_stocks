import pandas as pd
import os
import numpy as np
import csv
import datetime

class Find_Goodone_cls:
    def Find_Fnc(self):
        #### 경로에 있는 파일, 폴더명 가져오기 ####
        # 경로에 있는 csv 파일명을 가져와서 배열로 저장
        csv_files_collect = []
        for path, dirs, files in os.walk("F:/JusikData/oneday_csv/onedaydata"):
            csv_files_collect.append(''.join(files))

        # 배열의 첫번째는 값이 없으므로 제거
        del csv_files_collect[0]
        
        # 확인
        #print(csv_files_collect)
        ##########
        #
        #
        #
        #
        #### 종목명 배열 만들기 ####
        # .csv를 빼서 종목명만 집어넣기
        JongMok = []
        for i in csv_files_collect:
            aa = i.replace('.csv','')
            if aa == 'JYP Ent.JYP Ent':
                JongMok.append('JYP Ent')
            else :
                JongMok.append(aa)
                
        # 확인
        #print(JongMok)
        ##########
        #
        #
        #
        #
        #### 종목명 배열을 반복문으로 돌려서 모든종목의 데이터 분석 #####
        dname = [] # 리턴할 종목명
        ddate = [] # 리턴할 일자
        
        for name in JongMok:
            # 경로를 만들고 해당경로의 csv 파일 가져오기
            path = "F:/JusikData/oneday_csv/onedaydata/"+name+'/'+name+'.csv'
            data = pd.read_csv(path, encoding='cp949')
            data['5이평'] = data['종가'].rolling(window=5).mean()
            data['20이평'] = data['종가'].rolling(window=20).mean()
            #print(data.columns)
            ##############
            
            for i in data.index:
                if i > 90 :
                    if data.iloc[i-1]['거래량'] * 30 < data.iloc[i]['거래량']: # 거래량조건 : 30배
                        if data[i-20:i-1]['거래량'].max() < data.iloc[i]['거래량']: # 거래량조건 : 20일전 최대값보다 큼
                            if data.iloc[i]['시가'] < data.iloc[i]['종가']: # 봉조건 : 양봉
                                if data.iloc[i]['20이평'] < data.iloc[i]['5이평'] and data.iloc[i]['5이평'] < data.iloc[i]['종가']: # 봉조건 : 20<5<종
                                    if data.iloc[i]['시가'] < data.iloc[i-1]['종가'] * 1.1: # 봉조건 : 갭상승 10% 미만
                                        if data.iloc[i]['등락률'] < 25: # 봉조건 : 봉의 등락률이 25% 미만
                                            if ((data.iloc[i]['종가'] - data[i-30:i-1]['종가'].min()) / data.iloc[i]['종가']) * 100 < 30 : # 봉조건 : 30전에 비해 30% 이상 상승 제외
                                                if data.iloc[i]['고가'] - data.iloc[i]['종가'] < data.iloc[i]['종가'] - data.iloc[i]['저가'] : # 봉조건 : 위꼬리가 몸통보다 작도록
                                                    if (data.iloc[i]['고가'] + data.iloc[i]['저가']) / 2 > data.iloc[i]['5이평'] : # 봉조건 : 당일봉 중간값 > 5이평
                                                        if data[i-20:i-1]['종가'].max() < data.iloc[i]['종가']: # 고가/저가조건 : 20전고가 < 종가
                                                            if data[i-30:i-16]['종가'].min() < data[i-15:i-1]['종가'].min(): # 고가/저가조건 : 30전저가 < 15전저가
                                                                if ((data[i-45:i-1]['종가'].max() - data[i-45:i-1]['종가'].min()) / data[i-45:i-1]['종가'].max()) * 100 < 20 : # 고가/저가조건 : 45전저가와 고가차이 20%
                                                                    dname.append(data.iloc[i]['종목명'])
                                                                    ddate.append(data.iloc[i]['일자'])
            #print(dname)
            #print(ddate)
            print(name)
            
        # 데이터 csv로 저장
        dataset = pd.DataFrame({'종목명': dname, '기준일': ddate})
        dataset.to_csv('F:/JusikData/analysis_csv/increase/조건(2).csv', encoding='cp949', index = False)
        ##########
        
        
# 테스트
conn = Find_Goodone_cls()
conn.Find_Fnc()