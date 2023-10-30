import pandas as pd
import os
import numpy as np
import datetime
import requests # pip install requests

class dartapi_piicDecsn_cls():
    def exe_piic(self, api_key, corpcode, bgn_de, end_de):
        ## 유상증자 결정
        url_json = 'https://opendart.fss.or.kr/api/piicDecsn.json'
        url_xml = 'https://opendart.fss.or.kr/api/piicDecsn.json'
        
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
        
        # nstk_ostk_cnt : 보통주식 발행 수, nstk_estk_cnt : 기타주식 발행 수, ic_mthn : 증자방식
        print(df_list[['nstk_ostk_cnt','nstk_estk_cnt','ic_mthn']])
        
        # 결과값 리턴하기
        #return result
        
conn = dartapi_piicDecsn_cls()
conn.exe_piic('471e09c05ab83538cdb861f334fec507d3068573','00199252', '20150101', '20211221')