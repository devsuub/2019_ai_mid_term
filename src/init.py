import sqlite3
con = sqlite3.connect(':memory:')

winningLine = []

def init_winning_line():
    for i in range(4): # 가로
        for j in range(6):
            string = chr(65 + i) + str(j)
            string += chr(65 + i +1) + str(j)
            string += chr(65 + i +2) + str(j)
            string += chr(65 + i +3) + str(j)
            winningLine.append(string)
    for i in range(7): # 세로
        for j in range(3):
            string = chr(65 + i) + str(j)
            string += chr(65 + i) + str(j+1)
            string += chr(65 + i) + str(j + 2)
            string += chr(65 + i) + str(j + 3)
            winningLine.append(string)
    for i in range(4): # 오른쪽 대각선
        for j in range(3):
            string = chr(65 + i) + str(j)
            string += chr(65 + i+1) + str(j + 1)
            string += chr(65 + i+2) + str(j + 2)
            string += chr(65 + i+3) + str(j + 3)
            winningLine.append(string)
    for i in range(4): # 오른쪽 대각선
        for j in range(3):
            string = chr(65 + 6 - i) + str(j)
            string += chr(65 + 5 - i) + str(j + 1)
            string += chr(65 + 4 - i) + str(j + 2)
            string += chr(65 + 3 - i) + str(j + 3)
            winningLine.append(string)

def init_table():
    cur = con.cursor()
    cur.execute("CREATE TABLE WINNING_LINE(LINE text, CPU integer, PEOPLE integer);")

def init_data():
    cur = con.cursor()
    for line in winningLine:
        cur.execute("INSERT INTO WINNING_LINE Values(:line, 1,1);", {"line": line})


init_table()
init_winning_line()
init_data()