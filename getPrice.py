from dbConfig import conn,cur
import requests
from bs4 import BeautifulSoup
import datetime
# 爬取所有股票當日收盤價

def main():
    print("開始寫入各股收盤價...")
    # 當天日期 (要再改)
    nowTime = datetime.datetime.now()
    nowTime1 = nowTime.strftime("%Y-%m-%d %H:%M:%S")
    date = nowTime1[0:10]
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
    print("爬蟲抓取完畢,開始存入DB")
    # 取出所有需要存的股票代號
    sql = "select * from allstock;" # 檢查這支股票有沒有在股票名稱table裡
    cur.execute(sql,())
    record = cur.fetchall()
    allStockID = []
    for i in record:
        allStockID.append(i[0])
    # 處理資料並寫入資料庫
    i = 4
    while i < len(allStock)-1:
        thisStockid = allStock[i]
        thisStockprice = float(allStock[i+3])*100 # 因精準度問題,所以存的價格*100,需取出計算時再除以100
        # 是要儲存的股票
        if thisStockid in allStockID:
            allStockID.remove(thisStockid)
            #sql = "INSERT INTO allprice(stockid,date,stockprice) values (%s,%s,%s);"
            #cur.execute(sql,(thisStockid,date,thisStockprice))
            #print(thisStockid,thisStockprice)
        i += 16
    conn.commit()
    print("開始寫入缺漏的股票價格...")
    # 把剩下沒爬到的股價分別爬取存進DB
    for i in range(len(allStockID)):
        url = "https://tw.stock.yahoo.com/quote/"+str(allStockID[i])+".TWO"
        # 重複抓直到成功
        do = True
        while do:
            try:
                r = requests.get(url,headers=headers)
                soup = BeautifulSoup(r.text, "html.parser")
                stockprice = soup.find("span",{"class":"Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"})
                #sql = "INSERT INTO allprice(stockid,date,stockprice) values (%s,%s,%s);"
                #cur.execute(sql,(allStockID[i],date,stockprice.getText()))
                print(allStockID[i],stockprice.getText())
                do = False
                conn.commit()
            except:
                pass
    print("各股收盤價寫入完成!")

main()