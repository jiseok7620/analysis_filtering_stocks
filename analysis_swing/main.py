import pandas as pd
import win32com.client
import pythoncom
from Invest.analysis_swing.ebestapi_login import login_cls
from Invest.analysis_swing.ebestapi_ChartIndex import ChartIndex_cls
from Invest.analysis_swing.ebestapi_t4203 import t4203_cls
from Invest.analysis_swing.ebestapi_t1702 import t1702_cls
from Invest.analysis_swing.ebestapi_t1927 import t1927_cls
from Invest.analysis_swing.ebestapi_t1921 import t1921_cls
from Invest.analysis_swing.make_trendline import trendline_cls
import time
import os

class main_cls:
    def exe_main(self):
        # 파라미터 지정 <- 나중에 실제로 만들기
        #shcode = "045060" # 종목코드
        #edate = "20210101" # 매수일
        #sb = 1 # 0:순매수, 1:매수, 2:매도
        
        
        
        ##-----------------------------------------------------------------------------------##
        ## TEST
        # 미리 만들어놓은 csv 파일 가져오기
        data = pd.read_excel('F:/JusikData/analysis_csv/step/step1/투자시점_777.xlsx', engine='openpyxl')
            
        count = 25 # 몇번째 값 가져오려는지
        
        edate = str(data.iloc[count]['기준일'])
        name = data.iloc[count]['종목명']
        print(str(count)+'. 일자 : '+edate,
              '종목 : '+name,
              '종가 : '+str(data.iloc[count]['종가']),
              '고가 : '+str(data.iloc[count]['고가']),
              '저가 : '+str(data.iloc[count]['저가'])
              )
        
        # 개별종목데이터
        path1 = "F:/JusikData/oneday_csv/onedaydata/"+name+'/'+name+'.csv'
        data_jusiksu = pd.read_csv(path1, encoding='cp949')
        shcode = str(data_jusiksu.iloc[0]['종목코드'])
        
        # 코드에 0붙여주기
        if len(shcode) < 6:
            while True:
                shcode = '0' + shcode 
                if len(shcode) == 6:
                    break
            
        
        
        ##-----------------------------------------------------------------------------------##
        # 수정 시고저종, 거래량 가져오기
        path = 'F:/JusikData/API/data/'+name+'_'+edate+'.xlsx'
        
        num = 1 # 반복횟수
        
        for i in range(num) :
            if os.path.isfile(path) :
                pass
                '''
                # 저장한 엑셀 데이터 가져오기
                data_excel =  pd.read_excel('F:/JusikData/API/data/'+name+'_'+edate+'.xlsx', engine='openpyxl')
                edate_next = data_excel.iloc[0]['일자']
                
                # 데이터 한번 더 조회해서 병합하기
                dataset1 = ChartIndex_cls.exe_ChartIndex(self, shcode, str(edate_next))
                dataset1 = dataset1.drop(index=len(dataset1)-1, axis=0) # 제일 마지막 행 제거
                dataset1.reset_index(drop=True, inplace=True) # 인덱스 초기화
                data_merge = pd.concat([dataset1,data_excel], ignore_index=True) # 데이터프레임 합치기
                data_merge.to_excel('F:/JusikData/API/data/'+name+'_'+edate+'.xlsx', encoding='cp949', index=False)
                '''
            
            else:
                # 처음 조회 후 엑셀로 저장
                dataset1 = ChartIndex_cls.exe_ChartIndex(self, shcode, edate)
                dataset1.to_excel('F:/JusikData/API/data/'+name+'_'+edate+'.xlsx', encoding='cp949', index=False)
                    
                
                
            ##-----------------------------------------------------------------------------------##
            # 추세선, 매물대 그리기
            trendline_cls.exe_trendline(self, name, edate)



            ##-----------------------------------------------------------------------------------##
            # 업종 데이터 가져오기
            #dataset2 = t4203_cls.exe_t4203(self, shcode, edate)
            #print(dataset2)
            
            # 수급 데이터 가져오기
            #dataset3 = t1702_cls.exe_t1702(self, shcode, edate, sb)
            #print(dataset3)
            
            # 공매도 데이터 가져오기
            #dataset4 = t1927_cls.exe_t1927(self, shcode, edate)
            #print(dataset4)
            
            # 융자 데이터 가져오기
            #dataset5 = t1921_cls.exe_t1921(self, shcode, edate)
            #print(dataset5)
            
            
            
conn = main_cls()
conn.exe_main()