import requests
from dbConfig import conn,cur
import datetime

def main():
    # 今天日期
    date = datetime.datetime.now().strftime("%Y%m%d")
    #date = "20230517"
    # 爬取股票資訊
    print("爬取股票資訊...")
    while True:
        # 重複爬取直到成功
        try:
            url = "https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date="+date+"&type=ALL&response=csv"
            file = requests.get(url).text.split("\n")
            break
        except:
            pass
    date = date[0:4]+"-"+date[4:6]+"-"+date[6:]
    # 今天是否有開盤
    if file != ['']:
        print("開始寫入各股收盤價...")
        for i in range(271,len(file)-7):
            stock = file[i].split('","')
            if stock[8] != "--":
                #print(stock[0].replace("=","").replace('"',""),stock[1],stock[8].replace(",",""))
                sql = "INSERT INTO allprice(stockid,date,stockprice) values (%s,%s,%s);"
                cur.execute(sql,(stock[0].replace("=","").replace('"',""),date,float(stock[8].replace(",",""))*100))
        conn.commit()
        print("寫入完成!")
    else:
        print("今日沒有開盤")
main()