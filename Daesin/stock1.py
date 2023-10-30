# 종목명과 종목코드로 전체 종목 조회하기

import win32com.client
import re

class stock:
    # 종목명으로 조회 시 실행함수
    def SearchNameListByName(self, name):
        nameList = []
        codeList = []
        
        # CpStockCode = 주식코드조회작업을 함
        instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
        
        # GetCount = 종목코드 수를 반환함
        maxCodeNum = instCpStockCode.GetCount()
        for i in range(0,maxCodeNum) :
            nameList.append(instCpStockCode.GetData(1,i))

        name = name.upper()
        regex = re.compile(name)
        matches = [string for string in nameList if re.match(regex, string)]
        print('matches는?', matches)

        dataDict = { }
        nameList = []

        for i in matches :
            nameList.append(i)
            codeList.append(instCpStockCode.NameToCode(i))

        self.dataDict = {'name' : nameList , 'code' : codeList}
        print('dataDict는?',self.dataDict)

        print('instCpStockCode.NameToCode(name)는?',instCpStockCode.NameToCode(name))
        
    
    # 종목코드로 조회 시 실행함수
    def SearchNameListByCode(self, code ):
        nameList = []
        codeList = []

        instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
        maxCodeNum = instCpStockCode.GetCount()

        for i in range(0,maxCodeNum) :
            codeList.append(instCpStockCode.GetData(0,i))



        name = code.upper()
        regex = re.compile(name)


        matches = [string for string in codeList if re.match(regex, re.split("\D",string)[1])]
        print(matches)

        dataDict = { }
        codeList = []

        for i in matches :
            codeList.append(i)
            nameList.append(instCpStockCode.CodeToName(i))

        self.dataDict = {'name' : nameList , 'code' : codeList}
        