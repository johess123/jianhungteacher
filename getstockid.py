import requests
from dbConfig import conn,cur
import datetime

def main():
    date = datetime.datetime.now().strftime("%Y%m%d")
    while True:
        # 重複爬取直到成功
        try:
            url = "https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date="+date+"&type=ALL&response=csv"
            file = requests.get(url).text.split("\n")
            break
        except:
            pass
    if file != ['']:
        for i in range(271,len(file)-7):
            stock = file[i].split('","')
            if stock[8] != "--":
                #print(stock[0].replace("=","").replace('"',""),stock[1],stock[8].replace(",",""))
                sql = "INSERT INTO allstock(stockid,stockname) values (%s,%s);"
                cur.execute(sql,(stock[0].replace("=","").replace('"',""),stock[1]))
        conn.commit()
        print("寫入完成!")
    else:
        print("今日沒有開盤")

main()