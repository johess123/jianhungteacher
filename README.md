# 程式碼:

## getstockid.py 取得所有股票代號
爬蟲網址:
"https://stock.wespai.com/p/3752"

## getPrice.py 取得股票收盤價
爬蟲網址:
"https://histock.tw/stock/rank.aspx?p=all"
ubuntu crontab 設定每周一到五晚上6點爬取

## finstate.py 取得報表資料
爬蟲網址:
"https://mops.twse.com.tw/mops/web/ajax_t164sb03" # 資產負債表
"https://mops.twse.com.tw/mops/web/ajax_t164sb04" # 綜合損益表
"https://mops.twse.com.tw/mops/web/ajax_t164sb05" # 現金流量表
"https://mops.twse.com.tw/mops/web/ajax_t164sb06" # 權益變動表

# 資料庫:

allstock # 記錄所有股票代號、名稱,PK股票代號<br>
allprice # 存所有股價,PK流水號,FK股票代號<br>
balancesheet # 資產負債表(金額)<br>
balancesheetpct # 資產負債表(百分比)
