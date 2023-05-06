# -*- coding: utf-8 -*-
from dbConfig import conn,cur
import requests
from bs4 import BeautifulSoup
def financial_statement(stockid,year,season):
    url1 = "https://mops.twse.com.tw/mops/web/ajax_t164sb03" # 資產負債表
    url2 = "https://mops.twse.com.tw/mops/web/ajax_t164sb04" # 綜合損益表
    url3 = "https://mops.twse.com.tw/mops/web/ajax_t164sb05" # 現金流量表
    url4 = "https://mops.twse.com.tw/mops/web/ajax_t164sb06" # 權益變動表
    url = [url1,url2,url3,url4]
    #for i in range(len(url)):
    for i in range(1):
        r = requests.post(url[i], {
            'encodeURIComponent':1,
            'step':1,
            'firstin':1,
            'off':1,
            'TYPEK':'all',
            'year':str(year),
            'season':"0"+str(season),
            'co_id':str(stockid),
            'queryName':str(stockid),
            'inputType':str(stockid),
            'isnew':False,
        })
        #print(r.text)
        if i == 0: # 資產負債表
            soup = BeautifulSoup(r.text,'html.parser')
            result = soup.findAll(True, {'class':['odd', 'even']})
            #for j in range(len(result)):
                #print(j,result[j].getText())
            period = len(soup.findAll(True,{'class':['tblHead']})) # 計算期數(有時候報表是2期或3期)
            period = (period-4)/3 # 扣掉基本標頭後/3=期數
            div = 2*period+1 # 每項都是標頭+(該期數字+百分比)*期數 => 只要取最新一期 (餘1和餘2)
            insertNum = []
            insertPercent = []
            for j in range(len(result)):
                try:
                    num = float(result[j].getText().strip().replace(",","")) # 把數字的","拿掉
                    if j%div == 1: # 金額
                        insertNum.append(int(num))
                    elif j%div == 2: # 百分比
                        insertPercent.append(num)
                except: # 過濾掉沒數字的欄位(分類的標題)
                    pass
            #print(len(insertNum))
            #print(len(insertPercent))
            #for j in range(len(insertNum)):
                #print(j,insertNum[j])
            #print("------------------")
            #for j in range(len(insertPercent)):
                #print(j,insertPercent[j])
            # 寫入資料庫
            # 數值
            #sql = "INSERT INTO `balancesheet`(`stockid`, `year`, `season`, `現金及約當現金`, `透過損益按公允價值衡量之金融資產－流動`, `透過其他綜合損益按公允價值衡量之金融資產－流動`, `按攤銷後成本衡量之金融資產－流動`, `避險之金融資產－流動`, `應收帳款淨額`, `應收帳款－關係人淨額`, `其他應收款－關係人淨額`, `存貨`, `其他流動資產`, `流動資產合計`, `透過其他綜合損益按公允價值衡量之金融資產－非流動`, `按攤銷後成本衡量之金融資產－非流動`, `採用權益法之投資`, `不動產、廠房及設備`, `使用權資產`, `無形資產`, `遞延所得稅資產`, `其他非流動資產`, `非流動資產合計`, `資產總額`, `短期借款`, `透過損益按公允價值衡量之金融負債－流動`, `避險之金融負債－流動`, `應付帳款`, `應付帳款－關係人`, `其他應付款`, `本期所得稅負債`, `其他流動負債`, `流動負債合計`, `應付公司債`, `長期借款`, `遞延所得稅負債`, `租賃負債－非流動`, `其他非流動負債`, `非流動負債合計`, `負債總額`, `普通股股本`, `股本合計`, `資本公積－發行溢價`, `資本公積－實際取得或處分子公司股權價格與帳面價值差額`, `資本公積-認列對子公司所有權權益變動數`, `資本公積－受贈資產`, `資本公積－採用權益法認列關聯企業及合資股權淨值之變動數`, `資本公積－合併溢額`, `資本公積－限制員工權利股票`, `資本公積合計`, `法定盈餘公積`, `特別盈餘公積`, `未分配盈餘（或待彌補虧損）`, `保留盈餘合計`, `其他權益合計`, `庫藏股票`, `歸屬於母公司業主之權益合計`, `非控制權益`, `權益總額`, `負債及權益總計`, `預收股款（權益項下）之約當發行股數（單位：股）`, `母公司暨子公司所持有之母公司庫藏股股數（單位：股）`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #cur.execute(sql,(stockid,year,season,insertNum[0],insertNum[1],insertNum[2],insertNum[3],insertNum[4],insertNum[5],insertNum[6],insertNum[7],insertNum[8],insertNum[9],insertNum[10],insertNum[11],insertNum[12],insertNum[13],insertNum[14],insertNum[15],insertNum[16],insertNum[17],insertNum[18],insertNum[19],insertNum[20],insertNum[21],insertNum[22],insertNum[23],insertNum[24],insertNum[25],insertNum[26],insertNum[27],insertNum[28],insertNum[29],insertNum[30],insertNum[31],insertNum[32],insertNum[33],insertNum[34],insertNum[35],insertNum[36],insertNum[37],insertNum[38],insertNum[39],insertNum[40],insertNum[41],insertNum[42],insertNum[43],insertNum[44],insertNum[45],insertNum[46],insertNum[47],insertNum[48],insertNum[49],insertNum[50],insertNum[51],insertNum[52],insertNum[53],insertNum[54],insertNum[55],insertNum[56],insertNum[57],insertNum[58]))
            # 百分比
            #sql = "INSERT INTO `balancesheetpct`(`stockid`, `year`, `season`, `現金及約當現金`, `透過損益按公允價值衡量之金融資產－流動`, `透過其他綜合損益按公允價值衡量之金融資產－流動`, `按攤銷後成本衡量之金融資產－流動`, `避險之金融資產－流動`, `應收帳款淨額`, `應收帳款－關係人淨額`, `其他應收款－關係人淨額`, `存貨`, `其他流動資產`, `流動資產合計`, `透過其他綜合損益按公允價值衡量之金融資產－非流動`, `按攤銷後成本衡量之金融資產－非流動`, `採用權益法之投資`, `不動產、廠房及設備`, `使用權資產`, `無形資產`, `遞延所得稅資產`, `其他非流動資產`, `非流動資產合計`, `資產總額`, `短期借款`, `透過損益按公允價值衡量之金融負債－流動`, `避險之金融負債－流動`, `應付帳款`, `應付帳款－關係人`, `其他應付款`, `本期所得稅負債`, `其他流動負債`, `流動負債合計`, `應付公司債`, `長期借款`, `遞延所得稅負債`, `租賃負債－非流動`, `其他非流動負債`, `非流動負債合計`, `負債總額`, `普通股股本`, `股本合計`, `資本公積－發行溢價`, `資本公積－實際取得或處分子公司股權價格與帳面價值差額`, `資本公積-認列對子公司所有權權益變動數`, `資本公積－受贈資產`, `資本公積－採用權益法認列關聯企業及合資股權淨值之變動數`, `資本公積－合併溢額`, `資本公積－限制員工權利股票`, `資本公積合計`, `法定盈餘公積`, `特別盈餘公積`, `未分配盈餘（或待彌補虧損）`, `保留盈餘合計`, `其他權益合計`, `庫藏股票`, `歸屬於母公司業主之權益合計`, `非控制權益`, `權益總額`, `負債及權益總計`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #cur.execute(sql,(stockid,year,season,insertPercent[0],insertPercent[1],insertPercent[2],insertPercent[3],insertPercent[4],insertPercent[5],insertPercent[6],insertPercent[7],insertPercent[8],insertPercent[9],insertPercent[10],insertPercent[11],insertPercent[12],insertPercent[13],insertPercent[14],insertPercent[15],insertPercent[16],insertPercent[17],insertPercent[18],insertPercent[19],insertPercent[20],insertPercent[21],insertPercent[22],insertPercent[23],insertPercent[24],insertPercent[25],insertPercent[26],insertPercent[27],insertPercent[28],insertPercent[29],insertPercent[30],insertPercent[31],insertPercent[32],insertPercent[33],insertPercent[34],insertPercent[35],insertPercent[36],insertPercent[37],insertPercent[38],insertPercent[39],insertPercent[40],insertPercent[41],insertPercent[42],insertPercent[43],insertPercent[44],insertPercent[45],insertPercent[46],insertPercent[47],insertPercent[48],insertPercent[49],insertPercent[50],insertPercent[51],insertPercent[52],insertPercent[53],insertPercent[54],insertPercent[55],insertPercent[56]))
            #conn.commit()
            #print("------------------------------------")
            #print("資產負債表寫入完成")
            #input("輸入任意鍵繼續...")
            
            
    #print("------------------------------------")
    #print("全部報表寫入完成")
    #input("輸入任意鍵繼續...")
def main():
    print("請輸入股票代號:")
    stockid = int(input())
    print("請輸入報表年分")
    year = int(input())
    print("請輸入報表季別")
    season = int(input())
    
    financial_statement(stockid,year,season)

main()