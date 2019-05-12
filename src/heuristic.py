import copy
import time
import numpy as np
import random

loseValI = -1000
loseValJ = -1000
result = np.zeros((8, 8, 8, 8, 8, 8))

def find_next_row(col, map):
    for i in range(6):
        if (map[i][col - 1] == 0):
            return chr(65 + i)
    return -1

def find_max(list):

    secondMaxValue = max(list)
    secondMaxI = list.index(secondMaxValue)
    print(list)
    print("위 휴리스틱 값들이 나와서")
    print(secondMaxValue, " 를 골라 ", secondMaxI, "에 놓습니다.")
    return secondMaxI

def set_trash_value(list, i):
    list[i] = -1000
    return list

def find_row_full(map, row):
    if (map[5][row] != 0):
        return True
    else:
        return False

def check_win(con, map, tableName):
    # WININING 확인
    cur = con.cursor()
    sql = "SELECT LINE FROM " + tableName + " WHERE AI = 1;"
    cur.execute(sql)
    for row in cur:
       # print(row[0])
        splitLine = list(row[0])
        count = 0
        if (map[ord(splitLine[1])-65][int(splitLine[0])-1] == -1):
            count = count + 1
        if (map[ord(splitLine[3])-65][int(splitLine[2])-1] == -1):
            count = count + 1
        if (map[ord(splitLine[5])-65][int(splitLine[4])-1] == -1):
            count = count + 1
        if (map[ord(splitLine[7])-65][int(splitLine[6])-1] == -1):
            count = count + 1

        if (count == 4):
            print("이기수확인")

            return True


def check_lose(con, map, tableName):
    # WININING 확인
    cur = con.cursor()
    sql = "SELECT LINE FROM " + tableName + " WHERE PLAYER = 1;"
    cur.execute(sql)
    for row in cur:
       # print(row[0])
        splitLine = list(row[0])
        count = 0
        if (map[ord(splitLine[1]) - 65][int(splitLine[0]) - 1] == 1):
            count = count + 1
        if (map[ord(splitLine[3]) - 65][int(splitLine[2]) - 1] == 1):
            count = count + 1
        if (map[ord(splitLine[5]) - 65][int(splitLine[4]) - 1] == 1):
            count = count + 1
        if (map[ord(splitLine[7]) - 65][int(splitLine[6]) - 1] == 1):
            count = count + 1
        if (count == 4):
            print("지는수확인")
            return True


def heuristic(con, map):
    global loseValI
    global loseValJ
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

    loseValI = -1000
    loseValJ = -1000


    ## 1depth
    for i in range(1, 8):
        tableName = "WINNING_LINE" + str(i)
        sql = "CREATE TABLE " + tableName + " AS SELECT * FROM WINNING_LINE;"
        cur = con.cursor()
        cur.execute(sql)
        # 다음수 넣기
        nextRow = find_next_row(i, map)
        if (nextRow != -1):  # row 안꽉찼을경우
            sql = "UPDATE " + tableName + " SET PLAYER = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(i) + nextRow + "%"})
            con.commit()
            result[i][0][0][0][0][0] = calculate_heuristic(con, tableName)
            # map 복사
            tempMap = copy.deepcopy(map)
            tempMap[ord(nextRow) - 65][i - 1] = -1
            if (check_win(con, tempMap, tableName)):
                ## 4개가 이어지는 경우
                sql = "DROP TABLE IF EXISTS " + tableName + ";"
                cur.execute(sql)
                return i-1
                break
            else:
                # 2depth
                for j in range(1, 8):
                    print(i,j)
                    go_2_depth(con, tableName, i, j, tempMap, 1)


        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)


    if (loseValJ != -1000) and (loseValI != -1000):
        if (loseValI == loseValJ):
            # i를 놓아서 지는 경우
            list = minmax(0)
            maxI =  find_max(list)

            if (loseValI == maxI):
                print("그러나 그다음수에 지는 경우가 발생하여서 위 값을 제외하고 다시 휴리스틱을 돌린 결과")
                # minmax 했을때 지는 경우의 수에 두는경우
                # 두번째로 큰값을 가져온다
                # del list[maxI]
                list = set_trash_value(list, maxI)
                secondMaxI = find_max(list)

                while (find_row_full(map, secondMaxI)):
                    print("그러나 해당 row가 꽉차서 다시 휴리스틱을 돌린 결과")
                    # del list[secondMaxI]
                    list = set_trash_value(list, secondMaxI)
                    secondMaxI = find_max(list)
                return secondMaxI

            else:

                while (find_row_full(map, maxI)):
                    print("그러나 해당 row가 꽉차서 다시 휴리스틱을 돌린 결과")
                    # del list[maxI]
                    list = set_trash_value(list, maxI)
                    maxI = find_max(list)
                return maxI

        else:  # 방어
            print("방어합니다")
            next = loseValJ - 1
            # while (find_row_full(map, next)):
            #     next = random.randrange(1, 8)
            return next
    else:
        list = minmax(0)

        maxI = find_max(list)

        while (find_row_full(map, maxI)):
            print("그러나 해당 row가 꽉차서 다시 휴리스틱을 돌린 결과")

            # del list[maxI]
            list = set_trash_value(list, maxI)
            maxI = find_max(list)

        return maxI



def go_2_depth(con, originalTableName, i, j, map, turn):
    global loseValI
    global loseValJ
    nextRow = find_next_row(j, map)
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

        tempMap = copy.deepcopy(map)
        tempMap[ord(nextRow) - 65][j - 1] = 1
        if (loseValJ == -1000) and (loseValI == -1000):
            if (check_lose(con, tempMap, tableName)):
                loseValJ = j
                loseValI = i

        for k in range(1, 8):
            go_3_depth(con, tableName, i, j, k, tempMap, 0)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)


def go_3_depth(con, originalTableName, i, j, k, map, turn):
    nextRow = find_next_row(k, map)
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

        tempMap = copy.deepcopy(map)
        tempMap[ord(nextRow) - 65][k - 1] = -1
        for l in range(1, 8):
            go_4_depth(con, tableName, i, j, k, l, tempMap, 1)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)


def go_4_depth(con, originalTableName, i, j, k, l, map, turn):
    nextRow = find_next_row(l, map)
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

        tempMap = copy.deepcopy(map)
        tempMap[ord(nextRow) - 65][l - 1] = 1
        for m in range(1, 8):
            go_5_depth(con, tableName, i, j, k, l, m, tempMap, 0)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)


def go_5_depth(con, originalTableName, i, j, k, l, m, map, turn):
    nextRow = find_next_row(m, map)
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

        tempMap = copy.deepcopy(map)
        tempMap[ord(nextRow) - 65][m - 1] = -1
        for n in range(1, 8):
            go_6_depth(con, tableName, i, j, k, l, m, n, tempMap, 1)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)


def go_6_depth(con, originalTableName, i, j, k, l, m, n, map, turn):
    nextRow = find_next_row(n, map)
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