import pandas as pd
import os
import numpy as np
import csv
import datetime
from Invest.backup.GBN1 import GBN1_cls
from Invest.backup.GBN2 import GBN2_cls
from Invest.backup.GBN4 import GBN4_cls
from Invest.backup.GBN5 import GBN5_cls
from Invest.backup.GBA1 import GBA1_cls
from Invest.backup.GBA2 import GBA2_cls
from Invest.backup.GBA3 import GBA3_cls
from Invest.backup.GBA4 import GBA4_cls

class GB_all_cls:
    def Exe_GB_all(self, tr, nday):
        '''
        # 경로에 있는 csv 파일명을 가져와서 배열로 저장
        csv_files_collect = []
        for path, dirs, files in os.walk("F:/JusikData/oneday_csv/onedaydata"):
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
        
        # 테스트를 위한 n번째 자료 추출
        #sr_st = 0 # 카운트
        #st_num = 151 # n번째 자료
        
        ####
        print('시작')
        # 종목 수 만큼 for문 돌려서 조건에 맞는 종목 찾기 
        for name in JongMok:
            print('step1_',name, '...진행중')

            path = "F:/JusikData/oneday_csv/onedaydata/"+name+'/'+name+'.csv'
            data = pd.read_csv(path, encoding='cp949')
            
            for i in data.index:
                try:
                    if data.iloc[i]['거래량'] > data.iloc[i-1]['거래량'] * tr : #거래량이 전일거래량의 tr배
                        if data.iloc[i]['등락률'] > 0 and data.iloc[i]['등락률'] <= 28 : #기준일 봉이 양봉, 등락률이 25% 이하
                            if data.iloc[i]['종가'] > data[i-nday:i]['고가'].max() : # 20일전 최고가보다 종가가 큼
                                        
                                #sr_st += 1 # 테스트 후 지우기
                                #if sr_st == st_num : # 테스트 후 지우기
                                    dname.append(data.iloc[i]['종목명']) # 종목명
                                    ddate.append(data.iloc[i]['일자']) # 기준일
                                        
                    #if sr_st == st_num : # 테스트 후 지우기
                        #break # 테스트 후 지우기
                except:
                    print(name, '_', str(data.iloc[i]['일자']), '_오류')
                    
            #if sr_st == st_num : # 테스트 후 지우기
                #break # 테스트 후 지우기
        
        # 조건에 맞는 종목 찾아서 데이터셋에 저장
        dataset = pd.DataFrame({'일자': ddate, '종목명': dname})
        #dataset.to_csv('F:/JusikData/analysis_csv/data/분석후데이터.csv', encoding='cp949', index = False)
        print('종료')
        ####
        
        
        ##-------------------------------------------------------------------
        # 추출한 종목에 대해서 for문을 돌려서 엑셀 만들기 - GBN 모듈들 불러오기
        dd = dataset.iloc[0]['일자']
        name = dataset.iloc[0]['종목명']
        
        print(dd, name)
        '''
        
        ##-------------------------------------------------------------------
        # 미리 만들어놓은 csv 파일 가져오기
        data = pd.read_excel('F:/JusikData/analysis_csv/step/step2/증가감소_1.xlsx', engine='openpyxl')
        
        # 몇번째
        num = 3
        for i in data.index:
            
            if i <= num-1:
                continue
            
            if i == num+1:
                break
            
            # 추출한 종목에 대해서 for문을 돌려서 엑셀 만들기 - GBN 모듈들 불러오기
            dd = data.iloc[i]['기준일']
            name = data.iloc[i]['종목명']
            
            ##-------------------------------------------------------------------
            ## 분기 구하기
            # dd의 년, 월, 일 나누기
            dd_y = int(str(dd)[0:4])
            dd_m = int(str(dd)[4:6])
            dd_d = int(str(dd)[6:8])
            
            # 현재 분기데이터 구하기
            if dd_m < 4 :
                q_num = 1
            elif dd_m < 7 :
                q_num = 2
            elif dd_m < 10 :
                q_num = 3
            elif dd_m <= 12 :
                q_num = 4
            
            # 해당 경로에 해당 파일이 있으면 최신년도 해당분기를 포함해서 진행
            directory = "F:/JusikData/report_csv/report/" + str(dd_y) + "_" + str(q_num) + "_jaemu_y.csv"
                
            # 해당 재무제표가 없으면 q_num에서 1빼줌
            if os.path.exists(directory) == False:
                q_num -= 1
            
            q = q_num
            
            GBN1_cls.Exe_GBN1(self, name, dd, q)
            GBN2_cls.Exe_GBN2(self, name, dd, q)
            GBN4_cls.Exe_GBN4(self, name, dd)
            GBN5_cls.Exe_GBN5(self, name, dd)
            GBA1_cls.Exe_GBA1(self, name, dd)
            GBA2_cls.Exe_GBA2(self, name, dd)
            GBA3_cls.Exe_GBA3(self, name, dd)
            GBA4_cls.Exe_GBA4(self, name, dd)
        
            print(dd,name)
            
conn = GB_all_cls()
conn.Exe_GB_all(10,20)