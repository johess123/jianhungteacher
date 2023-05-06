from dbConfig import conn,cur
import requests
from bs4 import BeautifulSoup
import datetime
# 爬取所有股票當日收盤價

def main():
    # 當天日期
    nowTime = datetime.datetime.now()
    nowTime1 = nowTime.strftime("%Y/%m/%d %H:%M:%S")
    date = nowTime1[0:4]+"-"+nowTime1[5:7]+"-"+nowTime1[8:10]
    # 爬股價
    headers = {
        'content-type': 'text/html; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    url = "https://histock.tw/stock/rank.aspx?p=all"
    # 重複抓直到成功
    do = True
    while do:
        try:
            r = requests.get(url,headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            allStock = soup.find('table',id='CPHB1_gv')
            allStock = allStock.getText().split("\n")
            do = False
        except:
            pass
    # 處理資料並寫入資料庫
    i = 4
    while i < len(allStock)-1:
        thisStockid = allStock[i]
        thisStockprice = allStock[i+3]
        sql = "select * from allstock where stockid = %s;" # 檢查這支股票有沒有在股票名稱table裡
        cur.execute(sql,(thisStockid,))
        record = cur.fetchall()
        sql = "select * from allprice where stockid = %s and date = %s;" # 檢查這支股票今天是否已被寫入過
        cur.execute(sql,(thisStockid,date))
        record1 = cur.fetchall()
        if len(record) != 0 and len(record1) == 0:
            print(thisStockid,thisStockprice)
            sql = "INSERT INTO allprice(stockid,date,stockprice) values (%s,%s,%s);"
            cur.execute(sql,(thisStockid,date,thisStockprice))
        i += 16
    conn.commit()

main()