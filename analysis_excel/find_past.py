import pandas as pd
import os
import numpy as np
import datetime

class find_past_cls:
    def exe_find_past(self):
        # 조건
        조건 = '테스트(1)'
        
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
            
            # 인덱스 0부터 시작
            data_index = 0
            # 인덱스 마지막 번호는
            max_index = len(data)
            
            # 조건1 : 거래량 전일 10배, 양봉, 봉이 상한가 X, 20일 최대값 돌파, 거래대금 50억
            for i in data.index:
                try:
                    if data.iloc[i]['거래량'] > data.iloc[i-1]['거래량'] * 10 : #거래량이 전일거래량의 10배
                        if data.iloc[i]['등락률'] > 0 and data.iloc[i]['등락률'] <= 28 :#기준일 봉이 양봉, 고가~저가봉이 28%이하
                            if data.iloc[i]['종가'] > data[i-20:i]['고가'].max() : # 20일전 최고가보다 종가가 큼
                                if data.iloc[i]['거래대금'] >= 5000000000:
                                    dname.append(data.iloc[i]['종목명']) # 종목명
                                    ddate.append(data.iloc[i]['일자']) # 기준일
                except:
                    print(name, '_', str(data.iloc[i]['일자']), '_오류')
            
            # 조건 2: 
            
            
        # 리턴할 데이터 셋
        dataset = pd.DataFrame({'일자': ddate, '종목명': dname})
    
        # 리턴하려면
        #return dataset
        
        
        
        ##---------------------------------------------------------------------##
        ## 데이터 증가율 정보 넣기
        arr_roi_max_20 = []
        arr_roi_min_20 = []
        arr_day_max_20 = []
        arr_day_min_20 = []
        
        arr_roi_max_60 = []
        arr_roi_min_60 = []
        arr_day_max_60 = []
        arr_day_min_60 = []

        arr_roi_max_120 = []
        arr_roi_min_120 = []
        arr_day_max_120 = []
        arr_day_min_120 = []
        for i in dataset.index:
            print('step2_',dataset.iloc[i]['종목명'], '...진행중')
            
            # 자료가져오기
            data_ori = pd.read_csv("oneday_csv/onedaydata/"+dataset.iloc[i]['종목명']+'/'+dataset.iloc[i]['종목명']+'.csv', encoding='cp949')
            
            # 해당 기준일의 인덱스 구하기
            index_num = data_ori[data_ori['일자'] == dataset.iloc[i]['일자']].index.tolist()
            
            # 기준일 종가, 기준일 이후 20봉 이내에 최댓값과 최솟값 구하기
            now_close = data_ori.iloc[index_num[0]]['종가']
            
            # 최댓값
            try:
                bar_20_arr = data_ori[index_num[0]+1:index_num[0]+20+1]['고가']
                bar_20_max = bar_20_arr.max() # 1개월 중 최대 증가
                roi_max_20 = ((bar_20_max - now_close) / now_close) * 100 # 1개월 중 최대 증가율
                arr_roi_max_20.append(roi_max_20) # 배열로 만들기
            except:
                arr_roi_max_20.append(10000)
                
            try:
                idx_bar_20 = bar_20_arr[bar_20_arr == bar_20_max].index[0] # 최대값의 인덱스 구하기
                bar_20_date = data_ori.iloc[idx_bar_20]['일자'] # 최대값의 일자 구하기
                arr_day_max_20.append(bar_20_date) # 배열로 만들기
            except:
                arr_day_max_20.append(11111111)
            
            try:
                bar_60_arr = data_ori[index_num[0]+1:index_num[0]+60+1]['고가']
                bar_60_max = bar_60_arr.max() # 3개월 중 최대 증가
                roi_max_60 = ((bar_60_max - now_close) / now_close) * 100 # 3개월 중 최대 증가율
                arr_roi_max_60.append(roi_max_60) # 배열로 만들기
            except:
                arr_roi_max_60.append(10000)
                
            try:
                idx_bar_60 = bar_60_arr[bar_60_arr == bar_60_max].index[0] # 최대값의 인덱스 구하기
                bar_60_date = data_ori.iloc[idx_bar_60]['일자'] # 최대값의 일자 구하기
                arr_day_max_60.append(bar_60_date) # 배열로 만들기
            except:
                arr_day_max_60.append(11111111)
                
            try:    
                bar_120_arr = data_ori[index_num[0]+1:index_num[0]+120+1]['고가']
                bar_120_max = bar_120_arr.max() # 6개월 중 최대 증가
                roi_max_120 = ((bar_120_max - now_close) / now_close) * 100 # 6개월 중 최대 증가율
                arr_roi_max_120.append(roi_max_120) # 배열로 만들기
            except:
                arr_roi_max_120.append(10000)
            
            try:
                idx_bar_120 = bar_120_arr[bar_120_arr == bar_120_max].index[0] # 최대값의 인덱스 구하기
                bar_120_date = data_ori.iloc[idx_bar_120]['일자'] # 최대값의 일자 구하기
                arr_day_max_120.append(bar_120_date) # 배열로 만들기
            except:
                arr_day_max_120.append(11111111)
                
            # 최솟값
            try:
                bar_20_arrm = data_ori[index_num[0]+1:index_num[0]+20+1]['저가']
                bar_20_min = bar_20_arrm.min()
                roi_min_20 = ((bar_20_min - now_close) / now_close) * 100
                arr_roi_min_20.append(roi_min_20)
            except:
                arr_roi_min_20.append(-10000)
                
            try:
                idx_bar_20m = bar_20_arrm[bar_20_arrm == bar_20_min].index[0] # 최소값의 인덱스 구하기
                bar_20_datem = data_ori.iloc[idx_bar_20m]['일자'] # 최소값의 일자 구하기
                arr_day_min_20.append(bar_20_datem) # 배열로 만들기
            except:
                arr_day_min_20.append(11111111)
            
            try:
                bar_60_arrm = data_ori[index_num[0]+1:index_num[0]+60+1]['저가']
                bar_60_min = bar_60_arrm.min()
                roi_min_60 = ((bar_60_min - now_close) / now_close) * 100
                arr_roi_min_60.append(roi_min_60)
            except:
                arr_roi_min_60.append(-10000)
                
            try:
                idx_bar_60m = bar_60_arrm[bar_60_arrm == bar_60_min].index[0] # 최소값의 인덱스 구하기
                bar_60_datem = data_ori.iloc[idx_bar_60m]['일자'] # 최소값의 일자 구하기
                arr_day_min_60.append(bar_60_datem) # 배열로 만들기
            except:
                arr_day_min_60.append(11111111)
            
            try:
                bar_120_arrm = data_ori[index_num[0]+1:index_num[0]+120+1]['저가']
                bar_120_min = bar_120_arrm.min()
                roi_min_120 = ((bar_120_min - now_close) / now_close) * 100
                arr_roi_min_120.append(roi_min_120)
            except:
                arr_roi_min_120.append(-10000)
            
            try:
                idx_bar_120m = bar_120_arrm[bar_120_arrm == bar_120_min].index[0] # 최소값의 인덱스 구하기
                bar_120_datem = data_ori.iloc[idx_bar_120m]['일자'] # 최소값의 일자 구하기
                arr_day_min_120.append(bar_120_datem) # 배열로 만들기
            except:
                arr_day_min_120.append(11111111)
                
        # 새로운 컬럼에 추가    
        dataset['20일최대증가율'] = arr_roi_max_20    
        dataset['20일최대감소율'] = arr_roi_min_20
        dataset['60일최대증가율'] = arr_roi_max_60    
        dataset['60일최대감소율'] = arr_roi_min_60
        dataset['120일최대증가율'] = arr_roi_max_120    
        dataset['120일최대감소율'] = arr_roi_min_120
        dataset['20일최대증가일자'] = arr_day_max_20
        dataset['20일최대감소일자'] = arr_day_min_20
        dataset['60일최대증가일자'] = arr_day_max_60
        dataset['60일최대감소일자'] = arr_day_min_60
        dataset['120일최대증가일자'] = arr_day_max_120 
        dataset['120일최대감소일자'] = arr_day_min_120
        
        # excel파일로 저장
        with pd.ExcelWriter('analysis_csv/step/step2/증가감소'+조건+'.xlsx') as writer:
            dataset.to_excel(writer, encoding='cp949', index=False)

conn = find_past_cls()
conn.exe_find_past()