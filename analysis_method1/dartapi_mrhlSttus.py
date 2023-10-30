import pandas as pd
import os
import numpy as np
import datetime
import requests # pip install requests

class dartapi_mrhlSttus_cls():
    def exe_ms(self, api_key, corpcode, year, code):
        ##---------------------------------------------------------------------##
        ## 소액주주 수 구하기
        url_json = 'https://opendart.fss.or.kr/api/mrhlSttus.json'
        url_xml = 'https://opendart.fss.or.kr/api/mrhlSttus.xml'
        
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
        
        # se : 구분, shrholdr_co : 주주수, shrholdr_tot_co : 전체 주주수, hold_stock_co : 보유 주식수, stock_tot_co : 총발행 주식수
        print(df_list[['se', 'shrholdr_co', 'shrholdr_tot_co', 'hold_stock_co', 'stock_tot_co']])
        

conn = dartapi_mrhlSttus_cls()
conn.exe_ms('471e09c05ab83538cdb861f334fec507d3068573','00807397', '2020', '11011')