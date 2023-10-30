import pandas as pd
import os
import numpy as np
import csv
import datetime

class Decrease_cls:
    def Make_Decrease(self):
        ####  ####
        # 경로에 있는 csv 파일명을 가져와서 배열로 저장
        csv_files_collect = []
        for path, dirs, files in os.walk("F:/JusikData/oneday_csv/onedaydata"):
            csv_files_collect.append(''.join(files))

        # 배열의 첫번째는 값이 없으므로 제거
        del csv_files_collect[0]
        
        # 확인
        #print(csv_files_collect)
        ##########
        
        
        ####  ####
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
        
        
        ####  #### 
        # 기준일로부터 n일 동안 증가율이 n% 이하일때의 기간 및 값 구하기
        # 구하고 이차원 배열로 저장
        dname = []
        ddate = []
        n_day = []
        for name in JongMok:
            # 경로를 만들고 해당경로의 csv 파일 가져오기
            path = "F:/JusikData/oneday_csv/onedaydata/"+name+'/'+name+'.csv'
            data = pd.read_csv(path, encoding='cp949')
            
            # 인덱스 0부터 시작
            data_index = 0
            
            # 인덱스 마지막 번호는
            max_index = len(data)
            
            while True:
                # 기준일로부터 n일 = 5, 10, 20, 30일 동안의 최고가, 최저가 구하기
                during_day = [5, 10, 20, 30]
                for i in during_day:
                    data2 = data.loc[data_index:data_index+i,:]
                    max_val = data2['고가'].max()
                    now_val = data['종가'][data_index]
                    min_val = data2['저가'].min()
                    #print(max_val, min_val)
                
                    # 최고가, 최저가 기준 현재주가 위치 구하기
                    roi = round((now_val - min_val) / min_val * 100, 1)
                    #print(roi) # 최저가로부터 몇 % 떨어졌는지
                    
                    if roi >= 50 :
                        dname.append(name)
                        ddate.append(data['일자'][data_index])
                        n_day.append(i)
                        add = []
                        
                data_index += 30
                
                if data_index >= max_index:
                    break
        ##########
        
        ####  ####
        # 이차원 배열을 데이터프레임 형태로 바꾼다음 엑셀로 저장하기
        dataset = pd.DataFrame({'종목명': dname, '기준일': ddate, 'n일': n_day})
        dataset = dataset.drop_duplicates(['종목명', '기준일'])
        print(dataset)
        dataset.to_csv('F:/JusikData/analysis_csv/increase/분석_감소데이터.csv', encoding='cp949', index = False)
        ##########
            
# 테스트
conn = Decrease_cls()
conn.Make_Decrease()