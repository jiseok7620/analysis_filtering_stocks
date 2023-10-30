import openpyxl
import pandas as pd
from datetime import datetime
import mplfinance as mpf
from matplotlib import gridspec
from _ast import If
from matplotlib.pyplot import xlabel
from openpyxl.drawing.image import Image

class all_chart_cls:
    def Exe_all_chart(self,name,dd):
        ##---------------------------------------------------------------------##
        # 엑셀 파일 열기
        wb = openpyxl.load_workbook('analysis_csv/HJS/'+name+'_'+str(dd)+'.xlsx')
        
        # 시트 지정 하기
        sheet = wb['Sheet1']



        ##---------------------------------------------------------------------##
        # 데이터 가져오기
        ## data1 = 개별 종목 데이터 ##
        path1 = "F:/JusikData/oneday_csv/onedaydata/"+name+'/'+name+'.csv'
        data1 = pd.read_csv(path1, encoding='cp949')
        #print(data1.columns)
        
        
        
        ##---------------------------------------------------------------------##
        # 그래프 만들기
        # 필요한 열만 가져오기
        # 0(일자),8(시가),9(고가),10(저가),5(종가),11(거래량)
        df = data1.iloc[:,[0,8,9,10,5,11]]
        
        # 일자를 datetime형식으로 바꾸기
        x_data_date = df['일자'].values.tolist()
        
        # 일자를 datetime 형식으로 바꾼뒤 배열에 저장하기
        x_date_arr = []
        for i in x_data_date:
            # 일자만 배열에 저장
            sl_date = str(i)[0:4] + '-' + str(i)[4:6] + '-' + str(i)[6:8]
            real_date = datetime.strptime(sl_date, "%Y-%m-%d").date()
            x_date_arr.append(sl_date)
        
        # df의 인덱스를 datetime 형식으로 바꾸기
        df.index = pd.to_datetime(x_date_arr)
        
        # 일자 열은 없애기
        df = df.drop(['일자'],axis=1)
        
        # 컬럼명 바꾸기 - 바꿔야 그려짐
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        
        # 차트 설정
        colorset = mpf.make_marketcolors(up='tab:red', down='tab:blue', volume='tab:blue')
        s = mpf.make_mpf_style(base_mpf_style='default', marketcolors=colorset)
        
        # 그래프의 시작과 끝 정하기
        today_index = data1.loc[data1['일자'] == dd]['일자'].index[0]
        arr_start = [today_index, 240]
        
        # 그래프 번호 메기기
        grape_num = 1
        for i in arr_start:
                
            # 그래프 그리기
            mpf.plot(df[today_index-i+1:today_index+1],              # 데이터 지정
                     volume=True,           # 거래량 표시 지정
                     mav=(20,60,120,240),   # 이동평균선 지정
                     figscale=1.5,          # 그림 크기 지정
                     figratio=(15,5),       # 그림 높이, 너비 비율 지정
                     savefig=dict(fname='F:/JusikData/analysis_csv/HJS/img/'+name+'_'+str(dd)+'_'+str(grape_num)+'_일봉차트.png',dpi=100,pad_inches=0.25),    # 저장
                     type='candle',         # 차트 종류 지정
                     style=s,               # 차트 스타일 지정(blueskies, checkers, classic, default, sas)
                     tight_layout=True,     # 레이아웃 지정
                     ylabel='Price')        # y축 라벨 지정
            
            #이미지 경로지정, 이미지 붙이기
            img_path = 'analysis_csv/HJS/img/'+name+'_'+str(dd)+'_'+str(grape_num)+'_일봉차트.png'
            img = Image(img_path)
            
            if grape_num == 1:
                sheet.add_image(img,'AG60')
            elif grape_num == 2:
                sheet.add_image(img,'AG27')
            
            # 번호 1씩 증가
            grape_num += 1
        
        
        
        ##---------------------------------------------------------------------##
        # 저장
        wb.save('analysis_csv/HJS/'+name+'_'+str(dd)+'.xlsx')
        wb.close()
        
#conn = all_chart_cls()
#conn.Exe_all_chart('삼성전자',20200504)