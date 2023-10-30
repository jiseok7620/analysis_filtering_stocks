import pandas as pd
import os
import numpy as np
import csv
import datetime

'''
육안으로 쉽게 보이는 투자시점과 똑같은 데이터들 모두 찾기
'''

class step1_cls:
    def make_step1(self, number, tr, nday ):
        # 경로에 있는 csv 파일명을 가져와서 배열로 저장
        csv_files_collect = []
        for path, dirs, files in os.walk("F:/JusikData/oneday_csv/onedaydata"):
            csv_files_collect.append(''.join(files))

        # 배열의 첫번째는 값이 없으므로 제거
        del csv_files_collect[0]
        
        # 확인
        #print(csv_files_collect)
        
        # .csv를 빼서 종목명만 집어넣기
        JongMok = []
        for i in csv_files_collect:
            aa = i.replace('.csv','')
            '''
            if aa == 'JYP Ent.JYP Ent':
                JongMok.append('JYP Ent')
            else :
                JongMok.append(aa)
            '''
            JongMok.append(aa)
            
        # 배열선언하기
        dname = [] # 리턴할 종목명
        ddate = [] # 리턴할 일자
        dopen = [] # 리턴할 시가
        dhigh = [] # 리턴할 고가
        dlow = [] # 리턴할 저가
        dclose = [] # 리턴할 종가
        dflate = [] # 리턴할 등락률
        dtrade = [] # 리턴할 거래량
        
        print('시작')
        # 종목 수 만큼 for문 돌리기    
        for name in JongMok:
            print('step1_',name, '...진행중')

            path = "F:/JusikData/oneday_csv/onedaydata/"+name+'/'+name+'.csv'
            data = pd.read_csv(path, encoding='cp949')
            
            # 인덱스 0부터 시작
            data_index = 0
            # 인덱스 마지막 번호는
            max_index = len(data)
            
            for i in data.index:
                try:
                    if data.iloc[i]['거래량'] > data.iloc[i-1]['거래량'] * tr : #거래량이 전일거래량의 ( )배
                        if data.iloc[i]['등락률'] > 0 and data.iloc[i]['등락률'] <= 28 :#기준일 봉이 양봉, 고가~저가봉이 28%이하
                            if data.iloc[i]['종가'] > data[i-nday:i]['고가'].max() : # 20일전 최고가보다 종가가 큼
                                if data.iloc[i]['거래대금'] >= 5000000000:
                                    dname.append(data.iloc[i]['종목명']) # 종목명
                                    ddate.append(data.iloc[i]['일자']) # 기준일
                                    dopen.append(data.iloc[i]['시가']) # 시가
                                    dhigh.append(data.iloc[i]['고가']) # 고가
                                    dlow.append(data.iloc[i]['저가']) # 저가
                                    dclose.append(data.iloc[i]['종가']) # 종가
                                    dflate.append(data.iloc[i]['등락률']) # 등락률
                                    dtrade.append(data.iloc[i]['거래량']) # 거래량
                except:
                    print(name, '_', str(data.iloc[i]['일자']), '_오류')
            
        num = number
        dataset = pd.DataFrame({'기준일': ddate, '종목명': dname, '시가': dopen, '고가': dhigh, '저가' : dlow, '종가': dclose, '등락률': dflate, '거래량': dtrade})
        dataset.to_excel('F:/JusikData/analysis_csv/step/step1/투자시점_'+str(num)+'.xlsx', sheet_name='sheet1', encoding='cp949', index=False)
        
        dataset.to_csv('F:/JusikData/analysis_csv/step/step1/투자시점_'+str(num)+'.csv', encoding='cp949', index = False)   
        print('종료')
            
#conn = step1_cls()
#conn.make_step1(777, 10, 20)