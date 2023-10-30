import pandas as pd
import numpy as np
from datetime import datetime
import mpl_finance
import matplotlib.pyplot as plt
import matplotlib as mat
import matplotlib.ticker as ticker
from matplotlib import gridspec

class Grape_cls:
    # name : 종목명
    # start : 시작일
    # end : 종료일
    # pm_day : 이전, 이후 n일
    def Make_Grape(self, name, start, end, pm_day):
        #############################################################
        # 설치된 폰트정보보기
        #font_list = [font.name for font in fonm.fontManager.ttflist]
        #for f in font_list:
            #print(f"{f}.ttf")
            
        # 한글 깨짐 방지
        mat.rcParams['font.family'] = 'Malgun Gothic'
        #############################################################
        #
        #
        #
        #
        #############################################################
        # 데이터 가져오기
        df = pd.read_csv("F:/JusikData/oneday_csv/onedaydata/"+name+"/"+name+".csv", encoding='cp949')
        
        # 필요한 열만 가져오기
        df = df.iloc[:,[0,5,7,8,9,10,11]]
        
        # 데이터 프레임에서 필요한 열만 추출하여 리스트로 만들기
        x_data_date = df['일자'].values.tolist()
        y_data_fluctuation_rate = df['등락률'].values.tolist()
        y_data_close = df['종가'].values.tolist()
        y_data_start = df['시가'].values.tolist()
        y_data_high = df['고가'].values.tolist()
        y_data_low = df['저가'].values.tolist()
        y_data_trade = df['거래량'].values.tolist()
        
        # 일자를 datetime 형식으로 바꾼뒤 배열에 저장하기
        x_date_arr = []
        x_day_arr = []
        for i in x_data_date:
            # 방법1. x레이블을 연도형식으로
            # 2020-01-01 형식으로 데이터를 배열에 저장
            #sl_date = str(i)[0:4] + '-' + str(i)[4:6] + '-' + str(i)[6:8]
            #real_date = datetime.strptime(sl_date, "%Y-%m-%d").date()
            
            # 방법2. x레이블을 일자형식으로
            # 일자만 배열에 저장
            sl_date = str(i)[0:4] + '-' + str(i)[4:6] + '-' + str(i)[6:8]
            real_date = datetime.strptime(sl_date, "%Y-%m-%d").date()
            x_date_arr.append(sl_date)
            #x_day_arr.append(real_date.strftime('%m%d'))
            x_day_arr.append(x_data_date.index(i))
        ###############################################################
        #
        #
        #
        #
        ###############################################################
        ## 변수 선언 ##
        # 이동평균 데이터
        ma5 = df['종가'].rolling(window=5).mean()
        ma20 = df['종가'].rolling(window=20).mean()
        ma60 = df['종가'].rolling(window=60).mean()
        ma120 = df['종가'].rolling(window=120).mean()
        
        # 시작일과 종료일의 인덱스를 저장하는 변수
        start_idx = x_date_arr.index(start)
        end_idx = x_date_arr.index(end)
        
        # 시작일과 종료일에서 앞 뒤로 pm_day일 씩 더 보여줘보기
        start_idx_before = start_idx - pm_day
        end_idx_after = end_idx + pm_day - 30
        
        # 차트에 텍스트를 표시하기위해 텍스트를 위치할 x와 y 구하기
        text_x_first = pm_day
        text_x_last = pm_day + (end_idx - start_idx)
        text_y_first = y_data_high[start_idx] # 시작값의 최대값
        text_y_last = y_data_high[end_idx] # 종료값의 최대값
        text_y_first_min = y_data_low[start_idx] # 시작값의 최소값
        text_y_last_min = y_data_low[end_idx] # 종료값의 최소값
        
        # 해당 인덱스 동안의 데이터
        x_day_arr = x_day_arr[start_idx_before:end_idx_after]
        y_data_fluctuation_rate = y_data_fluctuation_rate[start_idx_before:end_idx_after] # 등락률
        y_data_close = y_data_close[start_idx_before:end_idx_after] # 종가
        y_data_start = y_data_start[start_idx_before:end_idx_after] # 시가
        y_data_high = y_data_high[start_idx_before:end_idx_after] # 고가
        y_data_low = y_data_low[start_idx_before:end_idx_after] # 저가
        y_data_trade = y_data_trade[start_idx_before:end_idx_after] # 거래량
        
        # 해당 인덱스 동안의 이동평균데이터
        avgline_5 = ma5[start_idx_before:end_idx_after]
        avgline_20 = ma20[start_idx_before:end_idx_after]
        avgline_60 = ma60[start_idx_before:end_idx_after]
        avgline_120 = ma120[start_idx_before:end_idx_after]
        #############################################################
        #
        #
        #
        #
        #############################################################
        ## 차트그리기 ##
        # 폰트 지정
        font1 = {'family': 'serif',
                 'color':  'red',
                 'weight': 'normal',
                 'size': 10}
        
        font2 = {'family': 'serif',
                 'color':  'black',
                 'weight': 'bold',
                 'size': 18}
        
        # 차트에 표시할 데이터
        #plt.plot(x_date_arr, y_data_close, 'b-')
        ## 1번 차트 ##
        # 주가 일봉 차트
        fig = plt.figure(figsize=(18, 9))
        gs = gridspec.GridSpec(nrows=2, # row 몇 개 
                       ncols=1, # col 몇 개 
                       height_ratios=[4, 1], 
                       width_ratios=[18]
                      )
        ax1 = fig.add_subplot(gs[0])
        mpl_finance.candlestick2_ohlc(ax1, y_data_start, y_data_high, y_data_low, y_data_close, width=0.5, colorup='r', colordown='b')
        
        # 1번 차트 x축 레이블에 값 입력하기
        ax1.xaxis.set_major_locator(ticker.FixedLocator(range(len(x_day_arr))))
        ax1.xaxis.set_major_formatter(ticker.FixedFormatter(x_day_arr))
        
        # 1번 차트설정
        plt.title('종목명 : ' + name, fontsize=15) # 차트 제목
        plt.grid(True, axis='y') # 그리드(격자)
        plt.xlabel('순번') # x레이블 제목
        plt.ylabel('종가') # y레이블 제목
        plt.text(text_x_first, text_y_first+(text_y_first/20), start, rotation=60) # 내가 구할 첫번째 봉에 날짜 표시
        plt.text(text_x_first, text_y_first_min-(text_y_first_min/20), str(y_data_close[text_x_first]), fontdict=font1) # 내가 구할 첫번째 봉에 종가 표시
        plt.text(text_x_first, text_y_first_min-(text_y_first_min/10), str(y_data_fluctuation_rate[text_x_first]), fontdict=font1) # 내가 구할 첫번째 봉에 등락률 표시
        #plt.axvline(text_x_first, color='black', linestyle='--', linewidth=1) # 내가 구할 첫번째 봉에 수직선 표시 
        
        # 1번 차트에 이동평균선 그리기
        plt.plot(range(len(x_day_arr)), avgline_5, 'b', label='5이평') # 5일 이동평균선 그리기
        plt.plot(range(len(x_day_arr)), avgline_20, 'r', label='20이평') # 차트 그리기
        plt.plot(range(len(x_day_arr)), avgline_60, 'g', label='60이평') # 차트 그리기
        plt.plot(range(len(x_day_arr)), avgline_120, label='120이평') # 차트 그리기
        plt.legend(frameon=True)

        
        ## 2번 차트 ##
        # 거래량 바 차트
        ax2 = fig.add_subplot(gs[1], sharex=ax1) # 축 공유하기
        plt.bar(np.arange(len(x_day_arr)), y_data_trade)
        
        # 2번 차트설정
        # 저장
        plt.savefig('F:/JusikData/analysis_csv/test조건(2)/'+name+'_'+start+'.png')
        
        # plt 메모리 제거
        plt.close()
        #########################################################################
        #
        #
        #
        #
# 증가한 종목의 기준일 파일.csv      
increase_data = pd.read_csv('F:/JusikData/analysis_csv/increase/조건(2).csv', encoding='cp949')

# 객체 생성 및 함수 동작
conn = Grape_cls()
err = []
print('동작시작')
for index, row in increase_data.iterrows():
    try:
        # 시작 알림
        print(row['종목명'],'_시작')
        
        # 해당 종목의 데이터 가져오기
        data = pd.read_csv("F:/JusikData/oneday_csv/onedaydata/"+row['종목명']+"/"+row['종목명']+".csv", encoding='cp949')
        data_day = data['일자'].tolist()
        
        # 일자리스트에서 기준일의 인덱스 가져오기
        stday_index = data_day.index(row['기준일'])
        
        # 기준일 + n일의 인덱스에서 일자를 가져오기
        n_index = stday_index
        end_day = data_day[n_index]
        end_day = str(end_day)[0:4] + '-' + str(end_day)[4:6] + '-' + str(end_day)[6:8]
        
        # row['기준일']의 형식을 변경하기
        sl_date = str(row['기준일'])[0:4] + '-' + str(row['기준일'])[4:6] + '-' + str(row['기준일'])[6:8]
        
        # 함수 실행
        conn.Make_Grape(row['종목명'], sl_date, end_day, 90)
    except:
        coment = row['종목명'] + sl_date + end_day + '_오류'
        print(coment)
        err.append(coment)
    
print('에러는 : ', err)
print('동작끝') 

