import pandas as pd
import os
import numpy as np
import datetime

class find_today_cls:
    def exe_find(self):
        # 경로에 있는 csv 파일명을 가져와서 배열로 저장
        csv_files_collect = []
        for path, dirs, files in os.walk("oneday_csv/onedaydata"):
            csv_files_collect.append(''.join(files))

        # 배열의 첫번째는 값이 없으므로 제거
        del csv_files_collect[0]
        
        # .csv를 빼서 종목명만 집어넣기
        JongMok = []
        for i in csv_files_collect:
            aa = i.replace('.csv','')
            JongMok.append(aa)

        # 배열선언하기
        dname = [] # 리턴할 종목명
        ddate = [] # 리턴할 일자
        
        # 오늘 날짜 구하기
        d_today = datetime.date.today()
        nowDate = d_today.strftime('%Y%m%d')
        
        # 이전날짜로 할때
        #nowDate = 20211208
        
        # 실행문
        print('시작')
        # 종목 수 만큼 for문 돌려서 조건에 맞는 종목 찾기 
        for name in JongMok:
            print('step1_',name, '...진행중')

            path = "oneday_csv/onedaydata/"+name+'/'+name+'.csv'
            data = pd.read_csv(path, encoding='cp949')
            
            # 가장 최근 인덱스는?
            idx = len(data) - 1
            
            print(data.iloc[idx]['일자'])
            
            if data.iloc[idx]['거래량'] > data.iloc[idx-1]['거래량'] * 10 : # 전일거래량의 10배
                if data.iloc[idx]['등락률'] > 0 and data.iloc[idx]['등락률'] <= 28 : #기준일 봉이 양봉, 등락률이 25% 이하
                    if data.iloc[idx]['종가'] > data[idx-20:idx]['고가'].max() : # 20일전 최고가보다 종가가 큼
                        if data.iloc[idx]['거래대금'] >= 5000000000:
                            if data.iloc[idx]['일자'] == int(nowDate) : # 오늘날짜랑 같아야함
                                dname.append(data.iloc[idx]['종목명']) # 종목명
                                ddate.append(data.iloc[idx]['일자']) # 기준일
            
        # 리턴할 데이터 셋
        dataset = pd.DataFrame({'일자': ddate, '종목명': dname})
        return dataset

#conn = find_today_cls()
#conn.exe_find()
        