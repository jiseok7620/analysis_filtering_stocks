import pandas as pd
import os
import requests # pip install requests
import zipfile
import xml.etree.ElementTree as ET
# 종목의 고유 코드를 가져오기

class met_corpcode_cls():
    def convert(self, tag: ET.Element) -> dict:
        conv = {}
        for child in list(tag):
            conv[child.tag] = child.text
        return conv
    
    def make_corpcode(self):
        # 파일존재확인
        check_file = os.path.isfile("F:/JusikData/report_csv/report_xml/CORPCODE.xml/CORPCODE.xml")
        
        if check_file :
            pass
        else:
            ## dart open api
            ## API key : 471e09c05ab83538cdb861f334fec507d3068573
            # 고유 번호 가져오기
            url = "https://opendart.fss.or.kr/api/corpCode.xml"
            api_key = "471e09c05ab83538cdb861f334fec507d3068573"
            params = {
                    'crtfc_key' : api_key
                }
            response = requests.get(url,params=params)
            
            # xml의 zip 파일을 로컬에 저장하기
            with open('F:/JusikData/report_csv/report_xml/number.zip', 'wb') as fp:
                fp.write(response.content)
                
            # zip 파일 저장하기
            zf = zipfile.ZipFile('F:/JusikData/report_csv/report_xml/number.zip')
            zf.extractall('F:/JusikData/report_csv/report_xml/CORPCODE.xml')
        
        # xml 저장경로
        xml_path = os.path.abspath('F:/JusikData/report_csv/report_xml/CORPCODE.xml/CORPCODE.xml')
        
        # xml 파싱하기
        tree = ET.parse(xml_path)
        root = tree.getroot()
        tags_list = root.findall('list')
        
        # xml 파싱한 것을 데이터프레임으로 만들기
        conn = met_corpcode_cls()
        tags_list_dict = [conn.convert(x) for x in tags_list]
        df = pd.DataFrame(tags_list_dict)
        
        return df
        
#conn = met_corpcode_cls()
#conn.make_corpcode('코이즈')
