import pandas as pd
import os
import numpy as np
import csv
import datetime

'''
step1에서 나온 데이터를 분석하여 추가 데이터를 표시 후 분류하여 저장하기
'''

class step2_cls:
    # number = 문서번호
    # nbar = 이후 n봉의 최대 최소값 구하기
    # nmore = 최대증가율을 n이상, 이하로 구분하기
    def make_step2(self, number, nbar, nmore):
        num = number

        # 데이터 가져오기
        data = pd.read_excel('F:/JusikData/analysis_csv/step/step1/투자시점_'+str(num)+'.xlsx', engine='openpyxl')
        
        arr_roi_max = []
        arr_roi_min = []
        for i in data.index:
            print('step2_',data.iloc[i]['종목명'], '...진행중')
            
            # 자료가져오기
            data_ori = pd.read_csv("F:/JusikData/oneday_csv/onedaydata/"+data.iloc[i]['종목명']+'/'+data.iloc[i]['종목명']+'.csv', encoding='cp949')
            
            # 해당 기준일의 인덱스 구하기
            index_num = data_ori[data_ori['일자'] == data.iloc[i]['기준일']].index.tolist()
            
            # 기준일 종가, 기준일 이후 20봉 이내에 최댓값과 최솟값 구하기
            now_close = data_ori.iloc[index_num[0]]['종가']
            
            # 최댓값
            bar_20_max = data_ori[index_num[0]+1:index_num[0]+nbar+1]['고가'].max()
            roi_max = ((bar_20_max - now_close) / now_close) * 100
            arr_roi_max.append(roi_max)
            
            # 최솟값
            bar_20_min = data_ori[index_num[0]+1:index_num[0]+nbar+1]['저가'].min()
            roi_min = ((bar_20_min - now_close) / now_close) * 100
            arr_roi_min.append(roi_min)
        
        # 새로운 컬럼에 추가    
        data['종가-최대값 증가율'] = arr_roi_max    
        data['종가-최소값 감소율'] = arr_roi_min
        
        # 데이터프레임 필터링(1) - 증가율 0이상
        data_plus = data[data['종가-최대값 증가율'] >= nmore]
        data_minus = data[data['종가-최대값 증가율'] < nmore]
        
        # 데이터프레임 필터링(2) - 증가율 30%이상
        #data_plus = data[data['종가-최대값 증가율'] >= 30]
        #data_minus = data[data['종가-최대값 증가율'] < 30]
        
        
        # csv파일로 저장하기
        #data_plus.to_csv('F:/JusikData/analysis_csv/step/step2/증가_'+str(num)+'.csv', encoding='cp949', index = False)
        #data_minus.to_csv('F:/JusikData/analysis_csv/step/step2/감소_'+str(num)+'.csv', encoding='cp949', index = False)
        
        # excel파일로 저장
        with pd.ExcelWriter('F:/JusikData/analysis_csv/step/step2/증가감소_'+str(num)+'.xlsx') as writer:
            data.to_excel(writer, encoding='cp949', index=False)
            #data_plus.to_excel(writer, sheet_name='증가', encoding='cp949', index=False)
            #data_minus.to_excel(writer, sheet_name='감소', encoding='cp949', index=False)
                
#conn = step2_cls()
#conn.make_step2(1)