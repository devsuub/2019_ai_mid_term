import sqlite3
con = sqlite3.connect(':memory:')

def update_people_play(position):
    cur = con.cursor()
    cur.execute("UPDATE WINNING_LINE SET CPU = 0 WHERE LINE LIKE :position", {"position": "%" + position + "%"})


def update_ai_play(position):
    cur = con.cursor()
    cur.execute("UPDATE WINNING_LINE SET PEOPLE = 0 WHERE LINE LIKE :position", {"position": "%" + position + "%"})