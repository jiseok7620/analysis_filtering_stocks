import pandas as pd
import os
import numpy as np
import datetime
import requests # pip install requests

class dartapi_majorstock_cls():
    def exe_ms(self, api_key, corpcode):
        ##---------------------------------------------------------------------##
        ## 대주주들의 주식 수 구하기
        url_json = 'https://opendart.fss.or.kr/api/majorstock.json'
        url_xml = 'https://opendart.fss.or.kr/api/majorstock.xml'
        
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
        
        # rcept_dt : 변동일자, stkqy : 변동주식수, repror : 대주주명, report_resn : 보고 사유
        df_list = df_list[['rcept_dt', 'stkqy', 'repror', 'report_resn']]
        
        # 중복제거하고 마지막만 남기기
        df_list = df_list.drop_duplicates(['repror'], keep = 'last') 
        print(df_list[['rcept_dt', 'stkqy', 'repror']])
        print(df_list['report_resn'])
        
        # , 제거하고, 타입을 int로 바꾸기
        df_list = df_list.replace(',','',regex=True)
        df_list = df_list.astype({'stkqy':'int'})

        # 결과 값
        result = df_list['stkqy'].sum()
        #print(result)
        
        # 리턴하기
        return result
        
#conn = dartapi_majorstock_cls()
#conn.exe_ms('471e09c05ab83538cdb861f334fec507d3068573','00199252')