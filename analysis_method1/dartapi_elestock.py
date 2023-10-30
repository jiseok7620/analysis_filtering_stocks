import pandas as pd
import os
import numpy as np
import datetime
import requests # pip install requests

class dartapi_elestock_cls():
    def exe_et(self, api_key, corpcode):
        ##---------------------------------------------------------------------##
        ## 임원ㆍ주요주주 소유보고 개발
        url_json = 'https://opendart.fss.or.kr/api/elestock.json'
        url_xml = 'https://opendart.fss.or.kr/api/elestock.xml'
        
        params ={
            'crtfc_key' : api_key,
            'corp_code' : corpcode,
            }
        
        # json 형식으로 가져와서 리스트로 추출
        response = requests.get(url_json, params=params)
        data = response.json()
        
        # 데이터프레임으로 변형
        data_list = data.get('list')
        df_list = pd.DataFrame(data_list)
        print(df_list)
        print(df_list.iloc[8])
        
        # 필요한 컬럼만 가져오기 
        df_list = df_list[['corp_name', 'repror', 'isu_exctv_ofcps', 'sp_stock_lmp_cnt']]
        print(df_list)
        
        # , 제거하고, 타입을 int로 바꾸기
        #df_list = df_list.replace(',','',regex=True)
        #df_list = df_list.astype({'stkqy':'int'})

        # 결과 값
        #result = df_list['stkqy'].sum()
        #print(result)
        
        # 리턴하기
       # return result
        
conn = dartapi_elestock_cls()
conn.exe_et('471e09c05ab83538cdb861f334fec507d3068573','00199252')