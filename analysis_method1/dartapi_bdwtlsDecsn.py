import pandas as pd
import os
import numpy as np
import datetime
import requests # pip install requests

class dartapi_bdwtIsDecsn_cls():
    def exe_bdwtIsDecsn(self, api_key, corpcode, bgn_de, end_de):
        ## 전환사채 발행 결정
        url_json = 'https://opendart.fss.or.kr/api/bdwtIsDecsn.json'
        url_xml = 'https://opendart.fss.or.kr/api/bdwtIsDecsn.xml'
        
        # bgn_de : 시작일, end_de : 종료일
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
        print(df_list.iloc[0])
        
        # bddd : 일자, bd_knd : 사채 종류, bd_fta : 사채 총액. bd_mtd :  사채 만기일
        #print(df_list[['bddd','bd_knd','bd_fta', 'bd_mtd',
        #               ]].iloc[4])
        
        # 결과값 리턴하기
        #return result
        
conn = dartapi_bdwtIsDecsn_cls()
conn.exe_bdwtIsDecsn('471e09c05ab83538cdb861f334fec507d3068573','00364306', '20150101', '20211221')