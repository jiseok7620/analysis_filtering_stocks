import pandas as pd
import os
import numpy as np
import datetime
import requests # pip install requests
from Invest.analysis_method1.corpcode_xml_parse import met_corpcode_cls
from Invest.analysis_method1.dartapi_stockTotqySttus import dartapi_stockTotqySttus_cls
from Invest.analysis_method1.dartapi_majorstock import dartapi_majorstock_cls 

# 유통주식수를 구해서 거래량이 유통주식 수의 n% 인 봉찾기

class met1_step1_cls():
    def exe_step1(self,name):
        ## data1 = 개별 종목 데이터 ##
        path1 = "F:/JusikData/oneday_csv/onedaydata/"+name+'/'+name+'.csv'
        data1 = pd.read_csv(path1, encoding='cp949')
        
        ## data3 = 수급데이터 ##
        path3 = "F:/JusikData/oneday_csv/onedaydata_supply/"+name+'.csv'
        data3 = pd.read_csv(path3, encoding='cp949')
        
        # 인증키
        api_key = '471e09c05ab83538cdb861f334fec507d3068573'
        
        ## 고유 번호 가져오기
        corpcode_df = met_corpcode_cls.make_corpcode(self)
        corpcode_num = corpcode_df[corpcode_df['corp_name'] == name]['corp_code']
        corpcode_num = str(corpcode_num.iloc[-1])
        print(corpcode_num)
        
        ## 년도, 분기 지정
        # 1분기(11013), 반기(11012), 3분기(11014), 사업(11011)
        year = '2021'
        code = '11014'
        
        ## 자사주를 제외한 주식수 가져오기
        stock_totqy = dartapi_stockTotqySttus_cls.exe_sts(self, api_key, corpcode_num, year, code)
        stock_totqy = stock_totqy.replace(',','') # , 기호 제거하기
        print('자사주 제외 유통주식수 : ', stock_totqy)
        
        ## 대주주 주식 수 가져오기
        stock_hyslr = dartapi_majorstock_cls.exe_ms(self, api_key, corpcode_num)
        print('대주주 주식수 : ', stock_hyslr)
        
        
        ##---------------------------------------------------------------------##
        ## 종목에서 의미있는 봉 찾기
        # 유통주식 수 구하기
        real_stock_num = int(stock_totqy) - int(stock_hyslr)
        print('유통주식 수 : ', real_stock_num)
        
        # 배열선언하기
        dname = [] # 리턴할 종목명
        ddate = [] # 리턴할 일자
        ddate_cor = [] # 수정일자 '-' 붙임
            
        # 조건에 맞는 데이터 찾기
        for i in data1.index:
            try:
                if data1.iloc[i]['거래량'] >= real_stock_num * 0.3 :
                        dname.append(data1.iloc[i]['종목명']) # 종목명
                        ddate.append(data1.iloc[i]['일자']) # 기준일
                        
                        date = str(data1.iloc[i]['일자'])[0:4] + '/' + str(data1.iloc[i]['일자'])[4:6] + '/' + str(data1.iloc[i]['일자'])[6:8]
                        ddate_cor.append(date)
            except:
                print(name, '_', str(data1.iloc[i]['일자']), '_오류')        
        
        dataset = pd.DataFrame({'일자': ddate, '종목명': dname, '수정일자' : ddate_cor })
        
        
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
        
        
conn = met1_step1_cls()
conn.exe_step1('삼성전자')
