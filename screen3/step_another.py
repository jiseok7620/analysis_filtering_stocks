import pandas as pd
import openpyxl
from Invest.screen3.step_another4 import step_another4_cls

class step_another_cls:
    def make_step_another(self):
        
        tf = True
        num = 1
        nbarall = [30,40,50,60,70,80,90,100,110,120]
        
        while tf:
            for nbar in nbarall:
                # 경로에 있는 csv 파일명을 가져와서 배열로 저장
                data_plus = pd.read_excel('F:/JusikData/analysis_csv/step/step3/Test1/증가감소(추가)_'+str(num)+'.xlsx', sheet_name='증가', engine='openpyxl')
                data_minus = pd.read_excel('F:/JusikData/analysis_csv/step/step3/Test1/증가감소(추가)_'+str(num)+'.xlsx', sheet_name='감소', engine='openpyxl')
                    
                arr_roi_max = []
                arr_roi_min = []
                arr_roi_max2 = []
                arr_roi_min2 = []
                for i in data_plus.index:
                    print('stepanother_',data_plus.iloc[i]['종목명'], '...진행중')
                    # 자료가져오기
                    data_ori_plus = pd.read_csv("F:/JusikData/oneday_csv/onedaydata/"+data_plus.iloc[i]['종목명']+'/'+data_plus.iloc[i]['종목명']+'.csv', encoding='cp949')
   
                    # 해당 기준일의 인덱스 구하기
                    index_num_plus = data_ori_plus[data_ori_plus['일자'] == data_plus.iloc[i]['기준일']].index.tolist()
                    
                    # 기준일 종가, 기준일 이후 20봉 이내에 최댓값과 최솟값 구하기
                    now_close_plus = data_ori_plus.iloc[index_num_plus[0]]['종가']
                        
                    # 최댓값
                    bar_20_max = data_ori_plus[index_num_plus[0]+1:index_num_plus[0]+nbar]['고가'].max()
                    roi_max = ((bar_20_max - now_close_plus) / now_close_plus) * 100
                    arr_roi_max.append(roi_max)
                        
                    # 최솟값
                    bar_20_min = data_ori_plus[index_num_plus[0]+1:index_num_plus[0]+nbar]['저가'].min()
                    roi_min = ((bar_20_min - now_close_plus) / now_close_plus) * 100
                    arr_roi_min.append(roi_min)
                    
                    
                for j in data_minus.index:
                    print('stepanother_',data_minus.iloc[j]['종목명'], '...진행중')
                    
                    # 자료가져오기
                    data_ori_minus = pd.read_csv("F:/JusikData/oneday_csv/onedaydata/"+data_minus.iloc[j]['종목명']+'/'+data_minus.iloc[j]['종목명']+'.csv', encoding='cp949')                    
                    
                    # 인덱스구하기
                    index_num_minus = data_ori_minus[data_ori_minus['일자'] == data_minus.iloc[j]['기준일']].index.tolist()                    
                    
                    # 종가
                    now_close_minus = data_ori_minus.iloc[index_num_minus[0]]['종가']
                    
                    # 최댓값
                    bar_20_max2 = data_ori_minus[index_num_minus[0]+1:index_num_minus[0]+nbar]['고가'].max()
                    roi_max2 = ((bar_20_max2 - now_close_minus) / now_close_minus) * 100
                    arr_roi_max2.append(roi_max2)
                        
                    # 최솟값
                    bar_20_min2 = data_ori_minus[index_num_minus[0]+1:index_num_minus[0]+nbar]['저가'].min()
                    roi_min2 = ((bar_20_min2 - now_close_minus) / now_close_minus) * 100
                    arr_roi_min2.append(roi_min2)
                    
                # 데이터 교체   
                data_plus['종가-최대값 증가율'] = arr_roi_max    
                data_plus['종가-최소값 감소율'] = arr_roi_min
                data_minus['종가-최대값 증가율'] = arr_roi_max2    
                data_minus['종가-최소값 감소율'] = arr_roi_min2
                
                # 형식 읽기
                inde_form = pd.read_excel('F:/JusikData/analysis_csv/step/step3/Test1/증가감소(추가)_'+str(num)+'.xlsx', sheet_name='증가감소비교분석', engine='openpyxl')
                        
                # excel파일로 저장
                with pd.ExcelWriter('F:/JusikData/analysis_csv/step/step3/another/매도시점교체_'+str(num)+'_'+str(nbar)+'.xlsx') as writer:
                    data_plus.to_excel(writer, sheet_name='증가', encoding='cp949', index=False)
                    data_minus.to_excel(writer, sheet_name='감소', encoding='cp949', index=False)
                    inde_form.to_excel(writer, sheet_name='증가감소비교분석', encoding='cp949', index=False)
                    
                step_another4_cls.make_step4_another4(self, num, nbar)
                
            # num과 tf
            num += 1
                
            if num == 210:
                tf = False
                
conn = step_another_cls()
conn.make_step_another()
