import copy
import numpy as np

loseVal = []
result = np.zeros((8, 8, 8, 8, 8, 8))

def find_next_row(col, board):

    for i in range(6):
        if (board[i][col - 1] == 0):
            return chr(65 + i)
    return -1

def find_max(list):
    secondMaxValue = max(list)
    secondMaxI = list.index(secondMaxValue)
    print(list)
    print("위 휴리스틱 값들이 나와서")
    print(secondMaxValue, " 를 골라 ", int(secondMaxI)+1, "에 놓습니다.")
    return secondMaxI

def set_trash_value(list, i):
    list[i] = -1000
    return list

def find_row_full(board, row):
    if (board[5][row] != 0):
        return True
    else:
        return False

def check_win(con, board, tableName):
    # WININING 확인
    cur = con.cursor()
    sql = "SELECT LINE FROM " + tableName + " WHERE AI = 1;"
    cur.execute(sql)
    for row in cur:
       # print(row[0])
        splitLine = list(row[0])
        count = 0
        if (board[ord(splitLine[1])-65][int(splitLine[0])-1] == -1):
            count = count + 1
        if (board[ord(splitLine[3])-65][int(splitLine[2])-1] == -1):
            count = count + 1
        if (board[ord(splitLine[5])-65][int(splitLine[4])-1] == -1):
            count = count + 1
        if (board[ord(splitLine[7])-65][int(splitLine[6])-1] == -1):
            count = count + 1

        if (count == 4):
            return True
            break


def check_lose(con, board, tableName):
    # WININING 확인
    cur = con.cursor()
    sql = "SELECT LINE FROM " + tableName + " WHERE PLAYER = 1;"
    cur.execute(sql)
    for row in cur:
       # print(row[0])
        splitLine = list(row[0])
        count = 0
        if (board[ord(splitLine[1]) - 65][int(splitLine[0]) - 1] == 1):
            count = count + 1
        if (board[ord(splitLine[3]) - 65][int(splitLine[2]) - 1] == 1):
            count = count + 1
        if (board[ord(splitLine[5]) - 65][int(splitLine[4]) - 1] == 1):
            count = count + 1
        if (board[ord(splitLine[7]) - 65][int(splitLine[6]) - 1] == 1):
            count = count + 1
        if (count == 4):
            return True
            break


def heuristic(con, board):
    global loseVal
    global result
    result = np.zeros((8, 8, 8, 8, 8, 8))
    ## init
    for i in range(1, 8):
        for j in range(1, 8):
            for k in range(1, 8):
                for l in range(1, 8):
                    for m in range(1, 8):
                        for n in range(1, 8):
                            result[i][j][k][l][m][n] = -2000

    # loseValI = -1000
    # loseValJ = -1000
    loseVal = []

    ## 1depth
    for i in range(1, 8):
        tableName = "WINNING_LINE" + str(i)
        sql = "CREATE TABLE " + tableName + " AS SELECT * FROM WINNING_LINE;"
        cur = con.cursor()
        cur.execute(sql)
        # 다음수 넣기
        nextRow = find_next_row(i, board)
        if (nextRow != -1):  # row 안꽉찼을경우
            sql = "UPDATE " + tableName + " SET PLAYER = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(i) + nextRow + "%"})
            con.commit()
            result[i][0][0][0][0][0] = calculate_heuristic(con, tableName)
            # board 복사
            tempBoard = copy.deepcopy(board)
            tempBoard[ord(nextRow) - 65][i - 1] = -1
            if (check_win(con, tempBoard, tableName)):
                ## 4개가 이어지는 경우
                sql = "DROP TABLE IF EXISTS " + tableName + ";"
                cur.execute(sql)
                return i-1
                break
            else:
                # 2depth
                for j in range(1, 8):
                    go_2_depth(con, tableName, i, j, tempBoard, 1)

        if (i != 7):
            print(i*13, '% 완료')
        else:
            print("90  % 완료")
        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)

    if (len(loseVal) != 0):
        for i in range(len(loseVal)):
            loseValI = loseVal[i].split(',')[0]
            loseValJ = loseVal[i].split(',')[1]
            print(loseValI, loseValJ)
            if (loseValI == loseValJ):
                # i를 놓아서 지는 경우
                list = minmax(0)
                maxI = find_max(list)

                if (int(loseValI) == int(maxI) + 1):
                    print("그러나 그다음수에 지는 경우가 발생하여서 위 값을 제외하고 다시 휴리스틱을 돌린 결과")
                    # minmax 했을때 지는 경우의 수에 두는경우
                    # 두번째로 큰값을 가져온다
                    # del list[maxI]
                    list = set_trash_value(list, maxI)
                    secondMaxI = find_max(list)

                    while (find_row_full(board, secondMaxI)):
                        print("그러나 해당 row가 꽉차서 다시 휴리스틱을 돌린 결과")
                        # del list[secondMaxI]
                        list = set_trash_value(list, secondMaxI)
                        secondMaxI = find_max(list)
                    return secondMaxI
                    break

                else:
                    if (i == int(len(loseVal)) - 1):
                        while (find_row_full(board, maxI)):
                            print("그러나 해당 row가 꽉차서 다시 휴리스틱을 돌린 결과")
                            # del list[maxI]
                            list = set_trash_value(list, maxI)
                            maxI = find_max(list)
                            if (int(loseValI) == int(maxI) + 1):
                                print("그러나 그다음수에 지는 경우가 발생하여서 위 값을 제외하고 다시 휴리스틱을 돌린 결과")
                                list = set_trash_value(list, maxI)
                                maxI = find_max(list)
                        return maxI
                        break
                    else:
                        continue

            else:  # 방어
                next = int(loseValJ) - 1
                if (find_row_full(board, next)):
                    continue
                else:
                    print("방어합니다")
                    return next
                    break
    else:
        list = minmax(0)

        maxI = find_max(list)

        while (find_row_full(board, maxI)):
            print("그러나 해당 row가 꽉차서 다시 휴리스틱을 돌린 결과")
            # del list[maxI]
            list = set_trash_value(list, maxI)
            maxI = find_max(list)

        return maxI



def go_2_depth(con, originalTableName, i, j, board, turn):
    global loseVal
    nextRow = find_next_row(j, board)
    if (nextRow != -1):  # row 안꽉찼을경우
        cur = con.cursor()
        tableName = "WINNING_LINE" + str(i) + str(j)
        sql = "CREATE TABLE " + tableName + " AS SELECT * FROM " + originalTableName + ";"
        cur.execute(sql)
        if (turn == 0):  # AI가 놓는경우
            sql = "UPDATE " + tableName + " SET PLAYER = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(j) + nextRow + "%"})
        else:
            sql = "UPDATE " + tableName + " SET AI = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(j) + nextRow + "%"})

        result[i][j][0][0][0][0] = calculate_heuristic(con, tableName)

        tempBoard = copy.deepcopy(board)
        tempBoard[ord(nextRow) - 65][j - 1] = 1
        if (check_lose(con, tempBoard, tableName)):
            loseVal.append(str(i) + "," + str(j))

        for k in range(1, 8):
            go_3_depth(con, tableName, i, j, k, tempBoard, 0)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)


def go_3_depth(con, originalTableName, i, j, k, board, turn):
    nextRow = find_next_row(k, board)
    if (nextRow != -1):  # row 안꽉찼을경우
        cur = con.cursor()
        tableName = "WINNING_LINE" + str(i) + str(j) + str(k)
        sql = "CREATE TABLE " + tableName + " AS SELECT * FROM " + originalTableName + ";"
        cur.execute(sql)
        if (turn == 0):  # AI가 놓는경우
            sql = "UPDATE " + tableName + " SET PLAYER = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(k) + nextRow + "%"})
        else:
            sql = "UPDATE " + tableName + " SET AI = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(k) + nextRow + "%"})

        result[i][j][k][0][0][0] = calculate_heuristic(con, tableName)

        tempBoard = copy.deepcopy(board)
        tempBoard[ord(nextRow) - 65][k - 1] = -1
        for l in range(1, 8):
            go_4_depth(con, tableName, i, j, k, l, tempBoard, 1)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)


def go_4_depth(con, originalTableName, i, j, k, l, board, turn):
    nextRow = find_next_row(l, board)
    if (nextRow != -1):  # row 안꽉찼을경우
        cur = con.cursor()
        tableName = "WINNING_LINE" + str(i) + str(j) + str(k) + str(l)
        sql = "CREATE TABLE " + tableName + " AS SELECT * FROM " + originalTableName + ";"
        cur.execute(sql)
        if (turn == 0):  # AI가 놓는경우
            sql = "UPDATE " + tableName + " SET PLAYER = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(l) + nextRow + "%"})
        else:
            sql = "UPDATE " + tableName + " SET AI = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(l) + nextRow + "%"})

        result[i][j][k][l][0][0] = calculate_heuristic(con, tableName)

        tempBoard = copy.deepcopy(board)
        tempBoard[ord(nextRow) - 65][l - 1] = 1
        for m in range(1, 8):
            go_5_depth(con, tableName, i, j, k, l, m, tempBoard, 0)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)


def go_5_depth(con, originalTableName, i, j, k, l, m, board, turn):
    nextRow = find_next_row(m, board)
    if (nextRow != -1):  # row 안꽉찼을경우
        cur = con.cursor()
        tableName = "WINNING_LINE" + str(i) + str(j) + str(k) + str(l) + str(m)
        sql = "CREATE TABLE " + tableName + " AS SELECT * FROM " + originalTableName + ";"
        cur.execute(sql)
        if (turn == 0):  # AI가 놓는경우
            sql = "UPDATE " + tableName + " SET PLAYER = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(m) + nextRow + "%"})
        else:
            sql = "UPDATE " + tableName + " SET AI = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(m) + nextRow + "%"})

        result[i][j][k][l][m][0] = calculate_heuristic(con, tableName)

        tempBoard = copy.deepcopy(board)
        tempBoard[ord(nextRow) - 65][m - 1] = -1
        for n in range(1, 8):
            go_6_depth(con, tableName, i, j, k, l, m, n, tempBoard, 1)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)


def go_6_depth(con, originalTableName, i, j, k, l, m, n, board, turn):
    nextRow = find_next_row(n, board)
    if (nextRow != -1):  # row 안꽉찼을경우
        cur = con.cursor()
        tableName = "WINNING_LINE" + str(i) + str(j) + str(k) + str(l) + str(m) + str(n)
        sql = "CREATE TABLE " + tableName + " AS SELECT * FROM " + originalTableName + ";"
        cur.execute(sql)
        if (turn == 0):  # AI가 놓는경우
            sql = "UPDATE " + tableName + " SET PLAYER = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(n) + nextRow + "%"})
        else:
            sql = "UPDATE " + tableName + " SET AI = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(n) + nextRow + "%"})

        result[i][j][k][l][m][n] = calculate_heuristic(con, tableName)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)

def calculate_heuristic(con, tableName):
    cur = con.cursor()
    sql = "SELECT COUNT(*) FROM " + tableName + " WHERE AI = 1"
    cur.execute(sql)
    myHeuristic = 0
    for row in cur:
        myHeuristic = row[0]
    sql = "SELECT COUNT(*) FROM " + tableName + " WHERE PLAYER = 1"
    cur.execute(sql)
    yourHeuristic = 0
    for row in cur:
        yourHeuristic = row[0]
    return myHeuristic - yourHeuristic

def minmax(turn):
    result2 = np.zeros((8, 8, 8, 8, 8, 8))
    for i in range(1, 8):
        for j in range(1, 8):
            for k in range(1, 8):
                for l in range(1, 8):
                    for m in range(1, 8):
                        for n in range(1, 8):
                            result2[i][j][k][l][m][n] == -2000


    for i in range(1, 8):
        for j in range(1, 8):
            for k in range(1, 8):
                for l in range(1, 8):
                    for m in range(1, 8):
                        for n in range(1, 8):
                            if result[i][j][k][l][m][n] == -2000:
                                continue
                            else:
                                if turn == 0:
                                    if result2[i][j][k][l][m][0] == -2000:
                                        result2[i][j][k][l][m][0] = result[i][j][k][l][m][n]
                                    else:
                                        result2[i][j][k][l][m][0] = (
                                            result[i][j][k][l][m][n] if result2[i][j][k][l][m][0] > result[i][j][k][l][m][
                                                n] else result2[i][j][k][l][m][0])
                                else:
                                    if result2[i][j][k][l][m][0] == 2000:
                                        result2[i][j][k][l][m][0] = result[i][j][k][l][m][n]
                                    else:
                                        result2[i][j][k][l][m][0] = (
                                            result[i][j][k][l][m][n] if result2[i][j][k][l][m][0] < result[i][j][k][l][m][
                                                n] else result2[i][j][k][l][m][0])

    for i in range(1, 8):
        for j in range(1, 8):
            for k in range(1, 8):
                for l in range(1, 8):
                    for m in range(1, 8):
                        if result2[i][j][k][l][m][0] == -2000:
                            continue
                        else:
                            if turn == 0:
                                if result2[i][j][k][l][0][0] == -2000:
                                    result2[i][j][k][l][0][0] = result2[i][j][k][l][m][0]
                                else:
                                    result2[i][j][k][l][0][0] = (
                                        result2[i][j][k][l][m][0] if result2[i][j][k][l][0][0] > result2[i][j][k][l][m][
                                            0] else result2[i][j][k][l][0][0])
                            else:
                                if result2[i][j][k][l][0][0] == 2000:
                                    result2[i][j][k][l][0][0] = result2[i][j][k][l][0][0]
                                else:
                                    result2[i][j][k][l][0][0] = (
                                        result2[i][j][k][l][m][0] if result2[i][j][k][l][0][0] < result2[i][j][k][l][m][
                                            0] else result2[i][j][k][l][0][0])
    for i in range(1, 8):
        for j in range(1, 8):
            for k in range(1, 8):
                for l in range(1, 8):
                    if result2[i][j][k][l][0][0] == -2000:
                        continue
                    else:
                        if turn == 0:
                            if result2[i][j][k][0][0][0] == -2000:
                                result2[i][j][k][0][0][0] = result2[i][j][k][l][0][0]
                            else:
                                result2[i][j][k][0][0][0] = (
                                    result2[i][j][k][l][0][0] if result2[i][j][k][0][0][0] > result2[i][j][k][l][0][0] else \
                                        result2[i][j][k][0][0][0])
                        else:
                            if result2[i][j][k][0][0][0] == 2000:
                                result2[i][j][k][0][0][0] = result2[i][j][k][l][0][0]
                            else:
                                result2[i][j][k][0][0][0] = (result2[i][j][k][l][0][0] if result2[i][j][k][0][0][0] < \
                                                                                          result2[i][j][k][l][0][0] else \
                                                                 result2[i][j][k][0][0][0])

    for i in range(1, 8):
        for j in range(1, 8):
            for k in range(1, 8):
                if result2[i][j][k][0][0][0] == -2000:
                    continue
                else:
                    if turn == 0:
                        if result2[i][j][0][0][0][0] == -2000:
                            result2[i][j][0][0][0][0] = result2[i][j][k][0][0][0]
                        else:
                            result2[i][j][0][0][0][0] = (result2[i][j][k][0][0][0] if result2[i][j][0][0][0][0] > \
                                                                                      result2[i][j][k][0][0][0] else \
                                                             result2[i][j][0][0][0][0])
                    else:
                        if result2[i][j][0][0][0][0] == 2000:
                            result2[i][j][0][0][0][0] = result2[i][j][k][0][0][0]
                        else:
                            result2[i][j][0][0][0][0] = (result2[i][j][k][0][0][0] if result2[i][j][0][0][0][0] < \
                                                                                      result2[i][j][k][0][0][0] else \
                                                             result2[i][j][0][0][0][0])

    for i in range(1, 8):
        for j in range(1, 8):
            if result2[i][j][0][0][0][0] == -2000:
                continue
            else:
                if turn == 0:
                    if result2[i][0][0][0][0][0] == -2000:
                        result2[i][0][0][0][0][0] = result2[i][j][0][0][0][0]
                    else:
                        result2[i][0][0][0][0][0] = (result2[i][j][0][0][0][0] if result2[i][0][0][0][0][0] > \
                                                                                  result2[i][j][0][0][0][0] else \
                                                         result2[i][0][0][0][0][0])
                else:
                    if result2[i][0][0][0][0][0] == 2000:
                        result2[i][0][0][0][0][0] = result2[i][j][0][0][0][0]
                    else:
                        result2[i][0][0][0][0][0] = (result2[i][j][0][0][0][0] if result2[i][0][0][0][0][0] < \
                                                                                  result2[i][j][0][0][0][0] else \
                                                         result2[i][0][0][0][0][0])
    list = []

    for i in range(1, 8):
        list.append(result2[i][0][0][0][0][0])


    return list