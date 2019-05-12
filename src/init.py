def init_table(con):
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS WINNING_LINE;")
    cur.execute("CREATE TABLE WINNING_LINE(LINE text, AI integer, PLAYER integer);")

def init_data(con):
    cur = con.cursor()
    f = open("./init.txt", 'r')
    lines = f.readlines()
    for line in lines:
        print(line)
        cur.execute(line)
    con.commit()

def init(con):
    init_table(con)
    init_data(con)
