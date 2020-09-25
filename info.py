import sqlite3

def openinfo(username, password):
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()
        sql = "select * from user where username = ? and password = ?"
        cur.execute(sql, (username, password))
        rows = cur.fetchall()
        for row in rows:
                print(row)
