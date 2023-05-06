import mysql.connector 

try:
    conn = mysql.connector.connect(
        user="root",
        password="",
        host="127.0.0.1",
        port=3306,
        database="finstate"
    )
except:
    print("Error connecting to DB")
    exit(1)
cur=conn.cursor()
