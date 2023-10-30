import pandas as pd
import os
import numpy as np
import csv
import datetime
from analysis_excel.chart_all import all_chart_cls
from analysis_excel.chart_bong import bong_chart_cls
from analysis_excel.chart_compo import compo_chart_cls
from analysis_excel.info_basic import basic_info_cls
from analysis_excel.info_chart import chart_info_cls
from analysis_excel.info_jaemu import jaemu_info_cls
from analysis_excel.info_jaemu_all import info_jaemu_all_cls
from analysis_excel.find_today import find_today_cls
from analysis_excel.all_add_summary import all_add_summary_cls

class all_cls:
    def Exe_all(self):
        
        # A or B = A : 과거데이터, B : 오늘데이터 분석
        AorB = 'A'
        
        if AorB == 'A':
            ##-------------------------------------------------------------------
            ## 방법 1. 과거데이터 분석하기 ##
            # 미리 만들어놓은 csv 파일 가져오기
            data = pd.read_excel('analysis_csv/step/step2/증가감소테스트(1).xlsx', engine='openpyxl')
            
            # 몇번째
            on_off = 2 # 1: on, 2: off
            num = 2
            count_num = 555 # 반복문 시작 인덱스 설정
            for i in data.index:
                
                if on_off ==1 :
                    if i <= num-1:
                        continue
                    
                    if i == num+1:
                        break
                else :
                    if i < count_num:
                        continue 
                    
                    if data.iloc[i]['일자'] < 20140101:
                        continue
                    
                # 최대증가율, 최대감소율
                max20 = data.iloc[i]['20일최대증가율']
                min20 = data.iloc[i]['20일최대감소율']
                max60 = data.iloc[i]['60일최대증가율']
                min60 = data.iloc[i]['60일최대감소율']
                max120 = data.iloc[i]['120일최대증가율']
                min120 = data.iloc[i]['120일최대감소율']
                max20dd = data.iloc[i]['20일최대증가일자']
                min20dd = data.iloc[i]['20일최대감소일자']
                max60dd = data.iloc[i]['60일최대증가일자']
                min60dd = data.iloc[i]['60일최대감소일자']
                max120dd = data.iloc[i]['120일최대증가일자']
                min120dd = data.iloc[i]['120일최대감소일자']
                
                # 추출한 종목에 대해서 for문을 돌려서 엑셀 만들기 - GBN 모듈들 불러오기
                dd = data.iloc[i]['일자']
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
                
                print(i,'번째 자료')
                print(q_num,'분기')
                # 해당 경로에 해당 파일이 있으면 최신년도 해당분기를 포함해서 진행
                directory = "F:/JusikData/report_csv/report/" + str(dd_y) + "_" + str(q_num) + "_jaemu_y.csv"
                    
                # 해당 재무제표가 없으면 q_num에서 1빼줌
                if os.path.exists(directory) == False:
                    q_num = q_num - 1
                '''
                try:
                    basic_info_cls.Exe_basic_info(self, name, dd, q_num)
                    jaemu_info_cls.Exe_jaemu_info(self, name, dd, q_num)
                    bong_chart_cls.Exe_bong_chart(self, name, dd)
                    all_chart_cls.Exe_all_chart(self, name, dd)
                    compo_chart_cls.Exe_compo_chart(self, name, dd)
                    chart_info_cls.exe_chart_info(self, name, dd)
                    #info_jaemu_all_cls.exe_info_jaemu_all(self, name, dd, q_num)
                    all_add_summary_cls.exe_all_add_summary(self, name, dd, 최대증가율, 최소감소율)
                except:
                    pass
                '''
                try:
                    basic_info_cls.Exe_basic_info(self, name, dd, q_num)
                    jaemu_info_cls.Exe_jaemu_info(self, name, dd, q_num)
                    bong_chart_cls.Exe_bong_chart(self, name, dd)
                    #all_chart_cls.Exe_all_chart(self, name, dd)
                    compo_chart_cls.Exe_compo_chart(self, name, dd)
                    chart_info_cls.exe_chart_info(self, name, dd)
                    #info_jaemu_all_cls.exe_info_jaemu_all(self, name, dd, q_num)
                    all_add_summary_cls.exe_all_add_summary(self, name, dd, max20, min20, max60, min60, max120, min120, max20dd, min20dd, max60dd, min60dd, max120dd, min120dd)   
                except:
                    pass
                    
                print(dd,name)
        
        
        
        elif AorB == 'B':
            ##-------------------------------------------------------------------
            ## 방법 2. 오늘데이터 분석하기 ##
            dataset = find_today_cls.exe_find(self)
            print(dataset)
            
            for i in dataset.index:
                # 추출한 종목에 대해서 for문을 돌려서 엑셀 만들기 - GBN 모듈들 불러오기
                dd = dataset.iloc[i]['일자']
                name = dataset.iloc[i]['종목명']
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
                    q_num -= 1
                
                basic_info_cls.Exe_basic_info(self, name, dd, q_num)
                jaemu_info_cls.Exe_jaemu_info(self, name, dd, q_num)
                bong_chart_cls.Exe_bong_chart(self, name, dd)
                all_chart_cls.Exe_all_chart(self, name, dd)
                compo_chart_cls.Exe_compo_chart(self, name, dd)
                chart_info_cls.exe_chart_info(self, name, dd)
                info_jaemu_all_cls.exe_info_jaemu_all(self, name, dd, q_num)
            
                print(dd,name)
            
conn = all_cls()
conn.Exe_all()