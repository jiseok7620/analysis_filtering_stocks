import pandas as pd
import os
import numpy as np
import datetime
import requests # pip install requests

class dartapi_hyslrSttus_cls():
    def exe_hs(self, api_key, corpcode, year, code):
        ##---------------------------------------------------------------------##
        ## 최대주주의 주식 수 구하기
        url_json = 'https://opendart.fss.or.kr/api/hyslrSttus.json'
        url_xml = 'https://opendart.fss.or.kr/api/hyslrSttus.xml'
        
        # reprt_code : 1분기(11013), 반기(11012), 3분기(11014), 사업(11011)
        params ={
            'crtfc_key' : api_key,
            'corp_code' : corpcode,
            'bsns_year' : year,
            'reprt_code' : code,
            }
        
        # json 형식으로 가져와서 리스트로 추출
        response = requests.get(url_json, params=params)
        data = response.json()
        
        # 데이터프레임으로 변형
        data_list = data.get('list')
        df_list = pd.DataFrame(data_list)
        #print(df_list)
        
        # nm : 성명, relate : 관계, stock_knd : 주식 종류, bsis_posesn_stock_co : 기초 소유 주식 수, trmend_posesn_stock_co : 기말 소유 주식 수
        print(df_list[['nm', 'relate', 'stock_knd', 'bsis_posesn_stock_co', 'trmend_posesn_stock_co']])
        
        # 대주주의 주식 수 총합 구하기 = 총합이 나와있으므로 제일 큰 값을 리턴하면 됨
        arr_posesn_stock = df_list['trmend_posesn_stock_co']
        
        # 결과 값
        result = arr_posesn_stock.max()
        print(result)
        
        # 리턴하기
        return result
        

#conn = dartapi_hyslrSttus_cls()
#conn.exe_hs('471e09c05ab83538cdb861f334fec507d3068573','00199252', '2021', '11014')