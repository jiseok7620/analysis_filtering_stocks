import pandas as pd
import os
import numpy as np
import csv
import datetime
from Invest.analysis_olderday.GBN1 import GBN1_cls
from Invest.analysis_olderday.GBN2 import GBN2_cls
from Invest.analysis_olderday.GBN4 import GBN4_cls
from Invest.analysis_olderday.GBN5 import GBN5_cls
from Invest.analysis_olderday.GBA1 import GBA1_cls
from Invest.analysis_olderday.GBA2 import GBA2_cls
from Invest.analysis_olderday.GBA3 import GBA3_cls
from Invest.analysis_olderday.GBA4 import GBA4_cls
#from Invest.analysis_olderday.find_today import find_today_cls

class GB_all_cls:
    def Exe_GB_all(self):
        
        # A or B = A : 과거데이터, B : 오늘데이터 분석
        AorB = 'A'
        
        if AorB == 'A':
            ##-------------------------------------------------------------------
            ## 방법 1. 과거데이터 분석하기 ##
            # 미리 만들어놓은 csv 파일 가져오기
            data = pd.read_excel('F:/JusikData/analysis_csv/step/step2/증가감소_1.xlsx', engine='openpyxl')
            
            # 몇번째
            on_off = 1 # 1: on, 2: off
            num = 3260
            for i in data.index:
                
                if on_off ==1 :
                    if i <= num-1:
                        continue
                    
                    if i == num+1:
                        break
                
                # 추출한 종목에 대해서 for문을 돌려서 엑셀 만들기 - GBN 모듈들 불러오기
                dd = data.iloc[i]['기준일']
                name = data.iloc[i]['종목명']
                print(dd,name)
                
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
                    q = q_num - 1
                
                GBN1_cls.Exe_GBN1(self, name, dd, q, q_num)
                GBN2_cls.Exe_GBN2(self, name, dd, q)
                GBN4_cls.Exe_GBN4(self, name, dd)
                GBN5_cls.Exe_GBN5(self, name, dd)
                GBA1_cls.Exe_GBA1(self, name, dd)
                GBA2_cls.Exe_GBA2(self, name, dd)
                GBA3_cls.Exe_GBA3(self, name, dd)
                GBA4_cls.Exe_GBA4(self, name, dd)
            
                print(dd,name)
        '''
        elif AorB == 'B':
            ##-------------------------------------------------------------------
            ## 방법 2. 오늘데이터 분석하기 ##
            dataset = find_today_cls.exe_find(self)
            print(dataset)
            
            for i in dataset.index:
                # 추출한 종목에 대해서 for문을 돌려서 엑셀 만들기 - GBN 모듈들 불러오기
                dd = dataset.iloc[i]['일자']
                name = dataset.iloc[i]['종목명']
                
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
            '''
conn = GB_all_cls()
conn.Exe_GB_all()