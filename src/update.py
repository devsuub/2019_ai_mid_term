import sqlite3

def update_people_play(con, position):
    print("hi")
    cur = con.cursor()
    cur.execute("UPDATE WINNING_LINE SET CPU = 0 WHERE LINE LIKE :position", {"position": "%" + position + "%"})

def update_ai_play(con, position):
    cur = con.cursor()
    cur.execute("UPDATE WINNING_LINE SET PEOPLE = 0 WHERE LINE LIKE :position", {"position": "%" + position + "%"})

