import openpyxl
import pandas as pd
from datetime import datetime
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image

class GBA3_cls:
    def make_roc(self, name, data1, dd):
        ##---------------------------------------------------------------------##
        # 그래프 만들기
        # ROC = (당일종가 - n일전 종가) / n일전 종가 * 100
        
        #arr_roc_14 = []
        arr_roc_20 = []
        #arr_roc_25 = []
        count_num = 60
        idx = data1.loc[data1['일자'] == dd]['일자'].index[0]
        
        while True:
            if count_num < 0:
                break
            
            당일종가 = data1.iloc[idx-count_num]['종가']
            #종가_14 = data1.iloc[idx-count_num-14]['종가']
            종가_20 = data1.iloc[idx-count_num-20]['종가']
            #종가_25 = data1.iloc[idx-count_num-25]['종가']
            
            #roc_14 = ((당일종가 - 종가_14) / 종가_14) *100
            roc_20 = ((당일종가 - 종가_20) / 종가_20) *100
            #roc_25 = ((당일종가 - 종가_25) / 종가_25) *100
            
            #arr_roc_14.append(roc_14)
            arr_roc_20.append(roc_20)
            #arr_roc_25.append(roc_25)
            
            count_num -= 1
        
        # 캔버스 설정(크기, 배경 설정 등)
        fig = plt.figure(figsize=(15,5)) ## 캔버스 생성
        fig.set_facecolor('white') ## 캔버스 색상 설정
        ax = fig.add_subplot() ## 그림 뼈대(프레임) 생성
        
        # 선그래프 그리기
        #ax.plot(arr_roc_14, color='red', marker='o', markersize=3)
        ax.plot(arr_roc_20, color='red', marker='o', markersize=3)
        #ax.plot(arr_roc_25, color='blue', marker='o', markersize=3)
        
        # 0에 수평선 긋기
        ax.axhline(0,color='green') 
        
        # 그래프 보기
        #plt.show()

        # 저장
        plt.savefig('F:/JusikData/analysis_csv/HJS/img/'+name+'_'+str(dd)+'_roc차트.png')
        
        # 메모리 제거
        plt.close()
        
    ##---------------------------------------------------------------------##
    def make_rsi(self, data1, period):
        ##---------------------------------------------------------------------##
        # RSI 구하기
        U = np.where(np.diff(data1['종가']) > 0, np.diff(data1['종가']), 0)
        D = np.where(np.diff(data1['종가']) < 0, np.diff(data1['종가']) *(-1), 0)
        
        AU = pd.DataFrame(U).rolling(window=period).mean()
        AD = pd.DataFrame(D).rolling(window=period).mean()
        RSI = AU.div(AD+AU) *100
        
        return RSI
        
    ##---------------------------------------------------------------------##
    def Exe_GBA3(self,name,dd):
        # 엑셀 파일 열기
        wb = openpyxl.load_workbook('F:/JusikData/analysis_csv/HJS/'+name+'_'+str(dd)+'.xlsx')
        
        # 시트 지정 하기
        sheet = wb['Sheet1']

        ##---------------------------------------------------------------------##
        # 데이터 가져오기
        ## data1 = 개별 종목 데이터 ##
        path1 = "F:/JusikData/oneday_csv/onedaydata/"+name+'/'+name+'.csv'
        data1 = pd.read_csv(path1, encoding='cp949')
        #print(data1.columns)


        
        ##---------------------------------------------------------------------##
        # ROC 그래프 구하기
        conn = GBA3_cls()
        conn.make_roc(name, data1, dd)


        
        ##---------------------------------------------------------------------##
        # RSI 그래프 구하기
        #RSI_14 = conn.make_rsi(data1, 14)
        #RSI_25 = conn.make_rsi(data1, 25)
        RSI_20 = conn.make_rsi(data1, 60)
        
        # 현재날짜의 인덱스
        idx = data1.loc[data1['일자'] == dd]['일자'].index[0]
        
        # 캔버스 설정(크기, 배경 설정 등)
        fig = plt.figure(figsize=(15,5)) ## 캔버스 생성
        fig.set_facecolor('white') ## 캔버스 색상 설정
        ax = fig.add_subplot() ## 그림 뼈대(프레임) 생성
        
        # 선그래프 그리기
        #ax.plot(RSI_14[idx-59:idx+1], color='red', marker='o', markersize=3)
        #ax.plot(RSI_25[idx-59:idx+1], color='blue', marker='o', markersize=3)
        ax.plot(RSI_20[idx-59:idx+1], color='blue', marker='o', markersize=3)
        
        # 0에 수평선 긋기
        ax.axhline(50,color='green') 
        
        # 그래프 보기
        #plt.show()
        
        # 저장
        plt.savefig('F:/JusikData/analysis_csv/HJS/img/'+name+'_'+str(dd)+'_rsi차트.png')
        
        # 메모리 제거
        plt.close()
        
        
        
        ##---------------------------------------------------------------------##
        # 그래프 붙여넣기
        #이미지 경로지정, 이미지 붙이기
        # 1. roc 차트
        img_path1 = 'F:/JusikData/analysis_csv/HJS/img/'+name+'_'+str(dd)+'_roc차트.png'
        img1 = Image(img_path1)
            
        sheet.add_image(img1,'W161')
            
        # 1. rsi 차트
        img_path2 = 'F:/JusikData/analysis_csv/HJS/img/'+name+'_'+str(dd)+'_rsi차트.png'
        img2 = Image(img_path2)
            
        sheet.add_image(img2,'AJ161')
        
        
        
        ##---------------------------------------------------------------------##        
        # 저장
        wb.save('F:/JusikData/analysis_csv/HJS/'+name+'_'+str(dd)+'.xlsx')
        wb.close()
        
#conn = GBA3_cls()
#conn.Exe_GBA3('삼성전자',20200504)