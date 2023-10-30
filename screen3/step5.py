import pandas as pd
import os
import numpy as np
import csv
import datetime
import openpyxl

class step5_cls:
    def make_step5(self, number):
        
        num = number
        
        # 파일 읽기
        data = pd.read_excel('F:/JusikData/analysis_csv/step/step3/증가감소(추가)_'+str(num)+'.xlsx', sheet_name='증가', engine='openpyxl')
        
        con1 = []
        con2 = []
        con3 = []
        con4 = []
        
        # data안에 있는거 읽기
        for i in data.index:
            try:
                if data.iloc[i]['기준일거래량_60전의_몇배']  > 1:
                    if data.iloc[i]['기준일거래량_20전의_많은수'] == 0:
                        #if data.iloc[i]['기준일종가_60전최소값의_몇배'] <1.3:
                            #if data.iloc[i]['20전_15%이상의_봉수'] <4:
                                #if data.iloc[i]['1년전최대최소의중간값_기준일종가의_몇배'] >= 0.5:
                                    #if data.iloc[i]['기준일저가_1년전최소값의_몇배'] >= 1.3:
                                        con1.append(data.iloc[i]['기준일'])
                                        con2.append(data.iloc[i]['종목명'])
                                        con3.append(data.iloc[i]['종가-최대값 증가율'])
                                        con4.append(data.iloc[i]['종가-최소값 감소율'])            
            except:
                print('오류')
        dataset = pd.DataFrame({'기준일': con1,'종목명': con2,'종가-최대값 증가율': con3,'종가-최소값 감소율': con4})
        dataset.to_excel('F:/JusikData/analysis_csv/step/step5/증가(필터링)_'+str(num)+'.xlsx', sheet_name='sheet1', encoding='cp949', index=False)    
        
        
        
        # 파일 읽기
        data_de = pd.read_excel('F:/JusikData/analysis_csv/step/step3/증가감소(추가)_'+str(num)+'.xlsx', sheet_name='감소', engine='openpyxl')
        
        con1_de = []
        con2_de = []
        con3_de = []
        con4_de = []
        
        # data안에 있는거 읽기
        for i in data_de.index:
            try:
                if data_de.iloc[i]['기준일거래량_60전의_몇배']  > 1:
                    if data_de.iloc[i]['기준일거래량_20전의_많은수'] == 0:
                        #if data_de.iloc[i]['기준일종가_60전최소값의_몇배'] <1.3:
                            #if data_de.iloc[i]['20전_15%이상의_봉수'] <4:
                                #if data_de.iloc[i]['1년전최대최소의중간값_기준일종가의_몇배'] >= 0.5:
                                    #if data_de.iloc[i]['기준일저가_1년전최소값의_몇배'] >= 1.3:
                                        con1_de.append(data_de.iloc[i]['기준일'])
                                        con2_de.append(data_de.iloc[i]['종목명'])
                                        con3_de.append(data_de.iloc[i]['종가-최대값 증가율'])
                                        con4_de.append(data_de.iloc[i]['종가-최소값 감소율'])            
            except:
                print('오류2')
                
        dataset_de = pd.DataFrame({'기준일': con1_de,'종목명': con2_de,'종가-최대값 증가율': con3_de,'종가-최소값 감소율': con4_de})
        dataset_de.to_excel('F:/JusikData/analysis_csv/step/step5/감소(필터링)_'+str(num)+'.xlsx', sheet_name='sheet1', encoding='cp949', index=False)
            
            
#conn = step5_cls()
#conn.make_step5(110)