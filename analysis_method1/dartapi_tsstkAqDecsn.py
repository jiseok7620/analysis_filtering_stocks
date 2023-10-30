import pandas as pd
import os
import numpy as np
import datetime
import requests # pip install requests

class dartapi_tsstkAqDecsn_cls():
    def exe_tsstkA(self, api_key, corpcode, bgn_de, end_de):
        ## 자기주식 취득 결정
        url_json = 'https://opendart.fss.or.kr/api/tsstkAqDecsn.json'
        url_xml = 'https://opendart.fss.or.kr/api/tsstkAqDecsn.xml'
        
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
        #print(df_list.iloc[0])
        
        # aqpln_stk_ostk : 취득 예정 주식(보통주), aqpln_stk_estk : 취득 예정 주식(기타주)
        # aq_dd : 취득 결정일, aqexpd_bgd : 취득 예상 시작일, aqexpd_edd : 취득 예상 종료일
        # aq_mth : 취득방법, aq_pp : 취득 목적
        print(df_list[['aqpln_stk_ostk','aqpln_stk_estk',
                       'aq_dd','aqexpd_bgd', 'aqexpd_edd',
                       'aq_mth', 'aq_pp'
                     ]].iloc[0])
        
        # 결과값 리턴하기
        #return result
        
conn = dartapi_tsstkAqDecsn_cls()
conn.exe_tsstkA('471e09c05ab83538cdb861f334fec507d3068573','00126380', '20150101', '20211221')