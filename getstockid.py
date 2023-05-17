import csv
from dbConfig import conn,cur

# 寫入全部股票代號,名稱
with open('MI_INDEX_ALL_20230517.csv', newline='') as csvfile:
    rows = list(csv.reader(csvfile))
    for i in range(271,len(rows)-6):
        #print(rows[i][0].replace('"',"").replace("=",""),rows[i][1],rows[i][8])
        sql = "INSERT INTO allstock(stockid,stockname) values (%s,%s);"
        cur.execute(sql,(rows[i][0].replace('"',"").replace("=",""),rows[i][1]))
    conn.commit()