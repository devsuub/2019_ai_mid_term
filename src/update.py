import sqlite3

def update_people_play(con, position):
    print("hi")
    cur = con.cursor()
    cur.execute("UPDATE WINNING_LINE SET AI = 0 WHERE LINE LIKE :position", {"position": "%" + position + "%"})
    con.commit()

def update_ai_play(con, position):
    cur = con.cursor()
    cur.execute("UPDATE WINNING_LINE SET PLAYER = 0 WHERE LINE LIKE :position", {"position": "%" + position + "%"})
    con.commit()

