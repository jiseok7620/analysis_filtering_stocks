import pandas as pd
import os
import numpy as np
import datetime

# 거래량이 상장주식수의 n%인 봉 찾기

class met1_step2_cls():
    def exe_step2(self,name):
        ## data1 = 개별 종목 데이터 ##
        path1 = "F:/JusikData/oneday_csv/onedaydata/"+name+'/'+name+'.csv'
        data1 = pd.read_csv(path1, encoding='cp949')
        #print(data1.columns)
        
        ## data3 = 수급데이터 ##
        path3 = "F:/JusikData/oneday_csv/onedaydata_supply/"+name+'.csv'
        data3 = pd.read_csv(path3, encoding='cp949')
        
        # 배열선언하기
        dname = [] # 리턴할 종목명
        ddate = [] # 리턴할 일자
        dtrade = [] # 거래량
        dmoney = [] # 거래대금
        djusik = [] # 상장주식수
        ddate_cor = [] # 수정일자 '-' 붙임
            
        # 조건에 맞는 데이터 찾기
        for i in data1.index:
            try:
                if data1.iloc[i]['거래량'] >= data1.iloc[i]['상장주식수'] * 0.1 :
                        dname.append(data1.iloc[i]['종목명']) # 종목명
                        ddate.append(data1.iloc[i]['일자']) # 기준일
                        dtrade.append(data1.iloc[i]['거래량']) # 거래량
                        dmoney.append(data1.iloc[i]['거래대금']) # 거래대금
                        djusik.append(data1.iloc[i]['상장주식수']) # 상장주식수
                        
                        date = str(data1.iloc[i]['일자'])[0:4] + '/' + str(data1.iloc[i]['일자'])[4:6] + '/' + str(data1.iloc[i]['일자'])[6:8]
                        ddate_cor.append(date)
            except:
                print(name, '_', str(data1.iloc[i]['일자']), '_오류')        
        
        dataset = pd.DataFrame({'일자': ddate, '종목명': dname, '수정일자' : ddate_cor, '거래량'  : dtrade, '거래대금' : dmoney, '상장주식수' : djusik})
        print(dataset)
        
        '''
        ##---------------------------------------------------------------------##
        ## 해당봉의 수급 구하기
        if dataset.empty :
            print('데이터프레임이 비어있습니다.')
        else :
            # 날짜 형식 바꾸기
            for i in dataset.index:
                if i == 0 :
                    df = data3[data3['일자'] == dataset.iloc[i]['수정일자']]
                else :
                    df = df.append(data3[data3['일자'] == dataset.iloc[i]['수정일자']], ignore_index=True)
                    
            print(df)
        '''
        
conn = met1_step2_cls()
conn.exe_step2('에이치엘비')
