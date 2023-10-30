import pandas as pd
import os
import numpy as np
import datetime
import requests # pip install requests

class dartapi_pifricDecsn_cls():
    def exe_pd(self, api_key, corpcode, bgn_de, end_de):
        ## 증자,감자 구하기
        url_json = 'https://opendart.fss.or.kr/api/pifricDecsn.json'
        url_xml = 'https://opendart.fss.or.kr/api/pifricDecsn.xml'
        
        # reprt_code : 1분기(11013), 반기(11012), 3분기(11014), 사업(11011)
        params ={
            'crtfc_key' : api_key,
            'corp_code' : corpcode,
            'bgn_de' : bgn_de,
            'end_de' : end_de,
            }
        
        # json 형식으로 가져와서 리스트로 추출
        response = requests.get(url_json, params=params)
        data = response.json()
        
        # 데이터프레임으로 변형
        data_list = data.get('list')
        df_list = pd.DataFrame(data_list)
        print('개수 : ', len(df_list))
        print(df_list)
        
        
        # istc_totqy : 발행주식의 총수, tesstk_co : 자기주식수, distb_stock_co : 유통주식수
        #print(df_list[['istc_totqy','tesstk_co','distb_stock_co']])
        
        # 자사주를 뺀 주식수
        #result = df_list.iloc[0]['distb_stock_co']
        #print(result)
        
        # 결과값 리턴하기
        #return result
        
conn = dartapi_pifricDecsn_cls()
conn.exe_pd('471e09c05ab83538cdb861f334fec507d3068573','00807397', '20150101', '20190701')