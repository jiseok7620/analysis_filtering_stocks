import pandas as pd
import os
import numpy as np
import csv
import datetime

class Find_Goodone_cls:
    def Find_Fnc(self, move_diff, trading_diff, n_day, trading_diff2, n_day_var, n_day_max):
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
        for name in JongMok:
            # 경로를 만들고 해당경로의 csv 파일 가져오기
            path = "F:/JusikData/oneday_csv/onedaydata/"+name+'/'+name+'.csv'
            data = pd.read_csv(path, encoding='cp949')
            data['20이평'] = data['종가'].rolling(window=20).mean()
            data['60이평'] = data['종가'].rolling(window=60).mean()
            data['120이평'] = data['종가'].rolling(window=120).mean()
            #print(data.columns)
            #
            #
            # 이동평균선이 정배열일때 true, 아닐때 false 넣기
            tf_arr = []
            for index, row in data.iterrows():
                if row['20이평'] >= row['60이평'] and row['60이평'] >= row['120이평']:
                    tf_arr.append("true")
                else:
                    tf_arr.append("false")
            data['정배열'] = tf_arr
            #print('정배열 개수 : ',len(data.loc[(data['정배열'] == 'true')])) # 조건에 맞는 개수 구하기
            #
            #
            # 기울기 구하기(x축은 한칸에 1이므로, 기울기 = 이평선의 차이와같다)
            # 20일선의 기울기가 (+) 일때 true, 아닐때 false 
            # [추가] 정확하지 않으면 1. n일 연속 기울기가 (+) 또는 '전보다 기울기가 커졌다'라는 조건을 더 걸어주기
            tf_arr1 = []
            for index, row in data.iterrows():
                if index > 0 :
                    # 20이평이 전보다 올라갔다면
                    if data.iloc[index][15] - data.iloc[index-1][15] > 0 :
                        tf_arr1.append("true")
                    else:
                        tf_arr1.append("false")  
                else:
                    tf_arr1.append("false")
                    
            data['20이평기울기'] = tf_arr1
            #print('20이평 기울기 (+) : ',len(data.loc[(data['20이평기울기'] == 'true')]))
            ########################################################################################
            # 60일이 20일보다 클때 20일이평과 60일이평의 차이가 n보다 작고, 
            # 차이구하는 예 data.iloc[index][11] => 해당인덱스의 11번째 열의 값을 가져옴
            tf_arr2 = []
            # 60일과 20일의 차이를 어떻게 정해야할까??
            # move_diff = 현 주가의 1% 정도?? => 일단 이걸로
            for index, row in data.iterrows():
                if row['60이평'] > row['120이평'] and row['60이평'] > row['20이평'] and (row['60이평'] - row['20이평']) <= row['종가'] * move_diff:
                    tf_arr2.append("true")
                else:
                    tf_arr2.append("false")
            data['2060이평차이'] = tf_arr2
            #print('2060이평차이 : ',len(data.loc[(data['2060이평차이'] == 'true')]))
            #####
            #
            #
            # 거래량이 전일의 n배 이상 차이가 남
            tf_arr3 = []
            # trading_diff = 거래량이 n배
            for index, row in data.iterrows():
                if index > 0:
                    if data.iloc[index][11] >= trading_diff * data.iloc[index-1][11] :
                        tf_arr3.append('true')
                    else :
                        tf_arr3.append('false')
                else :
                    tf_arr3.append('false')
                
            data['거래량차이'] = tf_arr3
            #print('거래량차이 : ',len(data.loc[(data['거래량차이'] == 'true')]))
            #print(data)
            ###########################################################################
            # 거래량이 전일 n일 평균의 a배 이상
            tf_arr4 = []
            #n_day = 15 # 전 n일
            #trading_diff2 = 10 # a배
            for index, row in data.iterrows():
                if index > n_day:
                    if data.iloc[index][11] >= trading_diff * data[index-n_day-1:index-1]['거래량'].mean() :
                        tf_arr4.append('true')
                    else :
                        tf_arr4.append('false')
                else :
                    tf_arr4.append('false')
            data['거래량평균과차이'] = tf_arr4
            #print('거래량평균과차이 : ',len(data.loc[(data['거래량평균과차이'] == 'true')]))
            #####
            #
            #
            # 전 n일 동안의 분산이 a보다 작아야함
            tf_arr5 = []
            #n_day_var = 20 # 20일 동안
            # 분산 = (종가 - 종가의 평균)제곱 / 10
            var_diff = 10 # 분산이 a보다 작다는 a값은 뭐로정하는게 좋을까 => 나중에 분석 데이터를 보고 결정해보자
            # => 일단 이거 안쓰고 종가의 평균보다 작아야된다고 해보자
            for index, row in data.iterrows():
                if index > n_day_var:
                    if data[index-n_day_var-1:index-1]['종가'].var() < data[index-n_day_var-1:index-1]['종가'].mean() :
                        tf_arr5.append('true')
                    else :
                        tf_arr5.append('false')
                else :
                    tf_arr5.append('false')
                
            data['분산'] = tf_arr5
            #print('분산 : ',len(data.loc[(data['분산'] == 'true')]))
            #####
            #
            #
            #
            #
            # 전 n일의 최대값보다 기준일가가 더 큼(전 n일의 고가보다, 현재 종가가 더커야됨)
            tf_arr6 = []
            #n_day_max = 15
            for index, row in data.iterrows():
                if index > n_day_max:
                    if data[index-n_day_max-1:index-1]['고가'].max() < data.iloc[index][5] :
                        tf_arr6.append('true')
                    else :
                        tf_arr6.append('false')
                else :
                    tf_arr6.append('false')
                
            data['전n일최대값보다큼'] = tf_arr6
            #print('전n일최대값보다큼 : ',len(data.loc[(data['전n일최대값보다큼'] == 'true')]))
            ####
            #
            #
            #
            #
            #print(data.columns)
            #print('-----')
            # 결과(조건에 맞는 종목의 데이터 배열로 저장해서 csv로 넘기기)
            # 1, 봉은 양봉이려면
            # '대비' 행이 양수이면됨
            # 2. 봉이 10% 이상 증가하지 않았으려면
            # '대비' 행이 10 이하면 됨
            
            dname = [] # 리턴할 종목명
            ddate = [] # 리턴할 일자
            
            for index, row in data.iterrows():
                # 조건1
                # 봉은 양봉, 당일 봉은 10% 이하 증가
                #if 10 >= data.iloc[index][6] > 0 :
                    if data.iloc[index][18] == 'true' and data.iloc[index][19] == 'true' and data.iloc[index][21] == 'true':
                        if data.iloc[index][22] == 'true' and data.iloc[index][23] =='true' and data.iloc[index][24] == 'true':
                            print(data.iloc[index][0], data.iloc[index][2])
                            dname.append(data.iloc[index][2])
                            ddate.append(data.iloc[index][0])
            
        # 데이터 csv로 저장
        dataset = pd.DataFrame({'종목명': dname, '기준일': ddate})
        print(dataset)
        #dataset.to_csv('F:/JusikData/analysis_csv/increase/조건(1).csv', encoding='cp949', index = False)
        ##########
        #
    #   
#
# 테스트
conn = Find_Goodone_cls()
conn.Find_Fnc(1/100, 5, 20, 5, 20, 20)