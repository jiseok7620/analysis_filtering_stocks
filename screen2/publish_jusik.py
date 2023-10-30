# 발행한 주식수가 몇년사이 엄청많아졌다?? => 증자를 많이 했다 => 안좋은 회사다

import pandas as pd
import os
import numpy as np
import csv
import datetime

class publish_jusik_cls:
    def publish_jusik(self, start_dd, end_dd, publ):
        
        '''
        # 경로안에 csv파일을 배열에 2차원으로 넣기
        csv_files = []
        dirs_arr = []
        a = 0
        for path, dirs, files in os.walk("D:/oneday_csv/onedaydata"):
            #print('files:',files)
            # a=1일 때는 폴더 이름을 배열로 저장하기
            # []가 추가되는것을 피하기위해서 a=1일때는 append 하지 않기
            a = a + 1
            
            if a == 1:
                dirs_arr = dirs
            
            if a != 1:
                csv_files.append(files)
        
        # 발행한 주식이 n년사이에 2배이상증가한 종목들 찾기
        # 마지막행 - 첫행으로 구하기
        jongmuk = []
        for dir in dirs_arr:
            df = pd.read_csv("D:/oneday_csv/onedaydata/"+dir+"/"+dir+'.csv', encoding='cp949')
            jongmuk.append({(df['상장주식수'].iloc[-1]-df['상장주식수'].iloc[0])/df['상장주식수'].iloc[0]})
            
        print(jongmuk)
        '''
        
        ##############################################################################################
        ## => 위 방법보다 n년n일 하루 전체종목 데이터 가져오고, m년m일 하루 전체 종목데이터를 가져와서
        ## 두 데이터 프레임에서 빼는게 훨씬 빠를듯!
        
        # csv파일
        start_csv = pd.read_csv('F:/JusikData/oneday_csv/alldata/'+start_dd+'.csv', encoding='cp949')
        end_csv = pd.read_csv('F:/JusikData/oneday_csv/alldata/'+end_dd+'.csv', encoding='cp949')
        
        # 시작데이타, 끝데이타
        start_data = start_csv[['종목코드', '종목명', '상장주식수']]
        end_data = end_csv[['종목코드', '상장주식수']]
        
        # 병합
        data = pd.merge(start_data, end_data, how='outer',on=['종목코드'])
        
        # 컬럼명 바꾸기
        data.columns = ['종목코드', '종목명', '시작주식수', '끝주식수']
        
        # 주식차 컬럼 추가하기
        data['주식차'] = data['끝주식수'] - data['시작주식수']
        data['종목코드'] = '[' + data['종목코드'] + ']'
        
        ####################################################################
        # 발행주식수가 publ 이상인 종목들을 배열에 저장하기
        publish_name = []
        for i in data.index:
            if data.loc[i,'주식차'] >= publ:
                publish_name.append(data.loc[i,'종목코드'])
        
        # 확인
        #print(publish_name)
        #print(len(publish_name),'개')
        
        #리턴값을 입력하시오#
        return publish_name
        ####################################################################

# 테스트    
#aa = publish_jusik_cls()
#aa.publish_jusik('20210622', '20180201', 500000000)
        