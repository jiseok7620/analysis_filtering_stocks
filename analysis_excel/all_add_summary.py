import pandas as pd
import os
import numpy as np
import csv
import datetime
import openpyxl
import win32com.client

class all_add_summary_cls:
    def exe_all_add_summary(self,name,dd,max20,min20,max60,min60,max120,min120,max20dd,min20dd,max60dd,min60dd,max120dd,min120dd):
        # win32com을 이용해 엑셀 한번 저장하기
        excel = win32com.client.Dispatch("Excel.Application")
        workbook = excel.Workbooks.Open('analysis_csv/HJS/'+name+'_'+str(dd)+'.xlsx')
        workbook.Close(SaveChanges=1)
        excel.quit()
        
        # 만들어진 데이터 열기
        data_out = openpyxl.load_workbook('analysis_csv/HJS/'+name+'_'+str(dd)+'.xlsx', data_only=True)
        
        # 시트지정하기
        sheet = data_out['Sheet1']
        
        # 데이터 가져오기
        자본잠식 = sheet['R11'].value
        매출액 = sheet['R16'].value
        시가총액 = sheet['R21'].value
        현금흐름 = sheet['R26'].value
        매출액흑자 = sheet['R31'].value
        부채비율유동비율 = sheet['R37'].value
        영업이익당기순이익흑자 = sheet['R47'].value
        매출채권재고자산회전율 = sheet['R57'].value
        영업이익률순이익률 = sheet['R67'].value
        PER = sheet['R78'].value
        PBR = sheet['R86'].value
        ROE = sheet['R94'].value
        ROA = sheet['R101'].value
        시장강도 = sheet['T11'].value
        봉차트 = sheet['T24'].value
        이격도 = sheet['T31'].value
        ROC = sheet['T38'].value
        RSI  = sheet['T43'].value
        OBV = sheet['T48'].value
        VR = sheet['T58'].value
        하락상승세 = sheet['T63'].value
        과거수급1 = sheet['T71'].value
        과거수급2 = sheet['T73'].value
        과거수급3 = sheet['T75'].value
        당일수급1 = sheet['T80'].value
        당일수급2 = sheet['T82'].value
        당일수급3 = sheet['T84'].value
        주가상승수급1 = sheet['T89'].value
        주가상승수급2 = sheet['T91'].value
        주가상승수급3 = sheet['T93'].value
        주가하락수급1 = sheet['T95'].value
        주가하락수급2 = sheet['T97'].value
        주가하락수급3 = sheet['T99'].value
        
        # 엑셀 닫기
        data_out.close()
        
        # 데이터 리스트로 만들기
        data_add = []
        data_add.append(str(name))
        data_add.append(str(dd))
        data_add.append(str(자본잠식))
        data_add.append(str(매출액))
        data_add.append(str(시가총액))
        data_add.append(str(현금흐름))
        data_add.append(str(매출액흑자))
        data_add.append(str(부채비율유동비율))
        data_add.append(str(영업이익당기순이익흑자))
        data_add.append(str(매출채권재고자산회전율))
        data_add.append(str(영업이익률순이익률))
        data_add.append(str(PER))
        data_add.append(str(PBR))
        data_add.append(str(ROE))
        data_add.append(str(ROA))
        data_add.append(str(시장강도))
        data_add.append(str(봉차트))
        data_add.append(str(이격도))
        data_add.append(str(ROC))
        data_add.append(str(RSI))
        data_add.append(str(OBV))
        data_add.append(str(VR))
        data_add.append(str(하락상승세))
        data_add.append(str(과거수급1))
        data_add.append(str(과거수급2))
        data_add.append(str(과거수급3))
        data_add.append(str(당일수급1))
        data_add.append(str(당일수급2))
        data_add.append(str(당일수급3))
        data_add.append(str(주가상승수급1))
        data_add.append(str(주가상승수급2))
        data_add.append(str(주가상승수급3))
        data_add.append(str(주가하락수급1))
        data_add.append(str(주가하락수급2))
        data_add.append(str(주가하락수급3))
        data_add.append(str(max20))
        data_add.append(str(min20))
        data_add.append(str(max20dd))
        data_add.append(str(min20dd))
        data_add.append(str(max60))
        data_add.append(str(min60))
        data_add.append(str(max60dd))
        data_add.append(str(min60dd))
        data_add.append(str(max120))
        data_add.append(str(min120))
        data_add.append(str(max120dd))
        data_add.append(str(min120dd))
        #print(data_add)
        
        # 추가할 엑셀 열기
        data_in = openpyxl.load_workbook('analysis_csv/HJS/01전체요약.xlsx')
        sheet2 = data_in.active
        
        # 추가하기
        sheet2.append(data_add)
        
        # 저장하기
        data_in.save('analysis_csv/HJS/01전체요약.xlsx')
        data_in.close()
        
#conn = all_add_summary_cls()
#conn.exe_all_add_summary('3S', 20180719,300,100)