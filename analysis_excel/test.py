import pandas as pd
import os
import numpy as np
import datetime


data_ori = pd.read_csv("F:/JusikData/oneday_csv/onedaydata/삼성전자/삼성전자.csv", encoding='cp949')
print(data_ori)

# 해당 기준일의 인덱스 구하기
index_num = data_ori[data_ori['일자'] == 20200504].index.tolist()
print(index_num[0])

bar_20_arr = data_ori[index_num[0]+1:index_num[0]+20+1]['고가']
print(bar_20_arr)

bar_20_max = data_ori[index_num[0]+1:index_num[0]+20+1]['고가'].max() # 1개월 중 최대 증가
print(bar_20_max)
print(bar_20_arr.max())

#print(bar_20_arr[bar_20_arr == bar_20_max].index[0])

#print(data_ori.iloc[bar_20_arr[bar_20_arr == bar_20_max].index[0]]['일자'])