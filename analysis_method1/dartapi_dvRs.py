import pandas as pd
import os
import numpy as np
import datetime
import requests # pip install requests

class dartapi_dvRs_cls():
    def exe_dvRs(self, api_key, corpcode, bgn_de, end_de):
        ## 분할 결정
        url_json = 'https://opendart.fss.or.kr/api/dvRs.json'
        url_xml = 'https://opendart.fss.or.kr/api/dvRs.xml'
        
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
        # cv_rt : 전환비율, cv_prc : 전환가액, cvisstk_knd : 전환에 따라 발행할 주식 종류, cvisstk_cnt : 전환에 따라 발행할 주식 수
        #print(df_list[['bddd','bd_knd','bd_fta', 'bd_mtd',
        #               'cv_rt', 'cv_prc', 'cvisstk_knd', 'cvisstk_cnt'
        #               ]].iloc[4])
        
        # 결과값 리턴하기
        #return result
        
conn = dartapi_dvRs_cls()
conn.exe_dvRs('471e09c05ab83538cdb861f334fec507d3068573','00126380', '20150101', '20211221')