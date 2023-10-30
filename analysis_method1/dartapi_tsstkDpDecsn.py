import pandas as pd
import os
import numpy as np
import datetime
import requests # pip install requests

class dartapi_tsstkDpDecsn_cls():
    def exe_tsstk(self, api_key, corpcode, bgn_de, end_de):
        ## 자기주식 처분 결정
        url_json = 'https://opendart.fss.or.kr/api/tsstkDpDecsn.json'
        url_xml = 'https://opendart.fss.or.kr/api/tsstkDpDecsn.xml'
        
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
        
        # dppln_stk_ostk : 처분 예정 주식수(보통주식), dppln_stk_estk : 처분 예정 주식수(기타주식)
        # dpstk_prc_ostk : 처분 대상 주식가격(보통주), dpstk_prc_estk : 처분 대상 주식가격(기타주)
        # dp_pp : 처분 목적, 처분방법 : 시장을 통한 매도(dp_m_mkt), 시간 외 대량매매(dp_m_ovtm), 장외처분(dp_m_ovtm), 기타주(dp_m_etc)
        # dp_dd : 처분 결정일, dpprpd_bgd : 처분예상시작일, dpprpd_edd : 처분예상종료일
        print(df_list[['dppln_stk_ostk','dppln_stk_estk',
                       'dpstk_prc_ostk','dpstk_prc_estk',
                      'dp_pp', 'dp_m_mkt', 'dp_m_ovtm', 'dp_m_ovtm', 'dp_m_etc',
                      'dp_dd', 'dpprpd_bgd', 'dpprpd_edd'
                     ]].iloc[0])
        
        # 결과값 리턴하기
        #return result
        
conn = dartapi_tsstkDpDecsn_cls()
conn.exe_tsstk('471e09c05ab83538cdb861f334fec507d3068573','00199252', '20150101', '20211221')