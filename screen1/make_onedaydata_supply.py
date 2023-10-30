import pandas as pd
import os
import numpy as np
import csv
import datetime

# csv파일의 이름을 담을 배열 생성
csv_files_collect = []

# 해당 경로의 csv 파일 이름 가져와서 배열에 담기        
for path, dirs, files in os.walk("F:/JusikData/oneday_csv/Downloads"):
    csv_files_collect = files

# 파일 하나 하나를 오름차순 정렬하여 저장하기     
for csvfile in csv_files_collect :
    df = pd.read_csv("F:/JusikData/oneday_csv/Downloads/" + csvfile, encoding='cp949')
    
    # 일자를 기준으로 오름차순
    df = df.sort_values('일자', ascending=True)
    
    # 인덱스 초기화
    df = df.reset_index(drop=True)
    
    # 이름에 !빼서 저장하기
    name = csvfile.replace('!.csv','')
    df.to_csv("F:/JusikData/oneday_csv/onedaydata_supply/" + name + ".csv", encoding='cp949', index = False)
