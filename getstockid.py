from dbConfig import conn,cur
import requests
from bs4 import BeautifulSoup
# 爬取所有股票代號和名稱

def main():
    headers = {
        'content-type': 'text/html; charset=UTF-8',
        'user-agent': 'Chrome/76.0.3809.132'
    }
    url = "https://stock.wespai.com/p/3752"
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    stockid = soup.find_all("td")
    for i in range(0,len(stockid),3):
        #print(i,stockid[i].getText())
        #print(i,stockid[i+1].getText())
        sql = "INSERT INTO allstock(stockid,stockname) values (%s,%s);"
        cur.execute(sql,(stockid[i].getText(),stockid[i+1].getText()))
    conn.commit()

main()