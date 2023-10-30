import pandas as pd
import os
import numpy as np
import csv
import datetime

# 경로에 있는 csv 파일명을 가져와서 배열로 저장
csv_files_collect = []
for path, dirs, files in os.walk("F:/JusikData/oneday_csv/onedaydata"):
    csv_files_collect.append(''.join(files))

# 배열의 첫번째는 값이 없으므로 제거
del csv_files_collect[0]
        
# .csv를 빼서 종목명만 집어넣기
JongMok = []
for i in csv_files_collect:
    aa = i.replace('.csv','')
    JongMok.append(aa)

# 파일 하나 하나를 오름차순 정렬하여 저장하기     
for name in JongMok :
    df = pd.read_csv("F:/JusikData/oneday_csv/onedaydata/"+name+"/"+name+".csv", encoding='cp949')
    
    print(df)
    
    # 일자를 기준으로 오름차순
    df = df.sort_values('일자', ascending=True)
    
    print(df)
    
    # 인덱스 초기화
    df = df.reset_index(drop=True)
    
    print(df)
    
    # 저장하기
    df.to_csv("F:/JusikData/oneday_csv/onedaydata/"+name+"/"+name+".csv", encoding='cp949', index = False)
