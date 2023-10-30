# 매출액에 비해 매출채권이 지나치게 높은기업 거르기
# 매출액 -> 포괄손익계산서 상 매출액
# 매출채권 -> 재무상태표 내 유동자산의 매출채권

# 매출채권회전율 = 매출액 / 매출채권
# 매출채권회수기간 = 365 / 매출채권회전율

# 매출채권 = (기초 매출채권 + 기말매출채권) / 2

# 매출채권회수기간은 5개월 이내가 적정 = 150일
# 매출채권 회전율은 4이상이 적정
#####################################

import pandas as pd
import datetime

# 년도, 분기, 연결여부 별 데이터프레임 형성하기
class trade_receivable_cls:
    def result_receivable(self, year, q, term):
        df_report = pd.read_csv('F:/JusikData/report_csv/report_make/재무정보_'+q+'분기.csv', encoding='cp949')
        
        # 전년도 구하기
        year_ago = str(int(year) - 1)
        
        #### 매출채권회전율, 매출채권회수기간 구하기 ####
        # 매출채권 = (기초 매출채권 + 기말매출채권) / 2
        # 매출채권회전율 = 매출액 / 매출채권
        # 매출채권회수기간 = 365 / 매출채권회전율
        
        # 매출채권을 담을 데이터프레임 만들기
        receivable_data = df_report[['종목코드', '업종명']]
        
        # 매출채권 = (기초 매출채권 + 기말매출채권) / 2 구하기
        receivable_data['기초+기말매출채권/2'] = (df_report[year+'_매출채권(유동)_'+q] + df_report[year_ago+'_매출채권(유동)_'+q]) / 2
        
        # 매출채권회전율 구하기 : 매출채권회전율 = 매출액 / 매출채권
        receivable_data['매출채권회전율'] = df_report[year+'_매출액_'+q] / receivable_data['기초+기말매출채권/2']
        
        # 매출채권회수기간 구하기
        receivable_data['매출채권회수기간'] = 365 / receivable_data['매출채권회전율']
        
        # 회전율(turnover) 3이하, 회수기간(term) 150일 이상은 부적정
        recv_name = []
        for i in receivable_data.index:
            if receivable_data.loc[i,'매출채권회수기간'] >= term:
                recv_name.append(receivable_data.loc[i,'종목코드'])

        #print(recv_name)
        #print(len(recv_name))
        
        #리턴값을 입력하시오#
        return recv_name
        ####################################################################
# 테스트
#conn = trade_receivable_cls()
#conn.result_receivable('2020', '2', 150)