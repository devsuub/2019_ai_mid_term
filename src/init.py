winningLine = []

def init_winning_line():
    for i in range(4): # 가로
        for j in range(6):
            string = str(i + 1) + chr(65 + j)
            string += str(i + 2) + chr(65 + j)
            string += str(i + 3) + chr(65 + j)
            string += str(i + 4) + chr(65 + j)
            winningLine.append(string)
    for i in range(7): # 세로
        for j in range(3):
            string = str(i + 1) + chr(65 + j)
            string += str(i + 1) + chr(65 + j+1)
            string += str(i + 1) + chr(65 + j + 2)
            string += str(i + 1) + chr(65 + j + 3)
            winningLine.append(string)
    for i in range(4): # 오른쪽 대각선
        for j in range(3):
            string = str(i + 1) + chr(65 + j)
            string += str(i + 2) + chr(65 + j + 1)
            string += str(i + 3) + chr(65 + j + 2)
            string += str(i + 4) + chr(65 + j + 3)
            winningLine.append(string)
    for i in range(4): # 오른쪽 대각선
        for j in range(3):
            string = str(7 - i) + chr(65 + j)
            string += str(6 - i) + chr(65 + j + 1)
            string += str(5 - i) + chr(65 + j + 2)
            string += str(4 - i) + chr(65 + j + 3)
            winningLine.append(string)

def init_table(con):
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS WINNING_LINE;")
    cur.execute("CREATE TABLE WINNING_LINE(LINE text, AI integer, PLAYER integer);")

def init_data(con):
    cur = con.cursor()
    for line in winningLine:
        cur.execute("INSERT INTO WINNING_LINE Values(:line, 1,1);", {"line": line})
    con.commit()

def init(con):
    print("database init")
    init_table(con)
    init_winning_line()
    init_data(con)
