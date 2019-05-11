import copy
import time
import numpy as np

result = np.zeros((8, 8, 8, 8, 8, 8))


def find_next_row(col, map):
    for i in range(6):
        if (map[i][col - 1] == 0):
            return chr(65 + i)
    return -1


def heuristic(con, map):
    print("hhhhhhhheuristic")
    start_time = time.time()

    ## 1depth
    for i in range(1, 8):
        start2_time = time.time()
        tableName = "WINNING_LINE" + str(i)
        sql = "CREATE TABLE " + tableName + " AS SELECT * FROM WINNING_LINE;"
        cur = con.cursor()
        cur.execute(sql)
        # 다음수 넣기
        nextRow = find_next_row(i, map)
        if (nextRow != -1):  # row 안꽉찼을경우
            sql = "UPDATE " + tableName + " SET AI = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(i) + nextRow + "%"})
            con.commit()
            result[i][0][0][0][0][0] = calculate_heuristic(con, tableName)
            # map 복사
            tempMap = copy.deepcopy(map)
            tempMap[ord(nextRow) - 65][i - 1] = -1
            # 2depth
            for j in range(1, 8):
                print(i, j)
                go_2_depth(con, tableName, i, j, tempMap, 0)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)

        print("--- %s seconds ---" % (time.time() - start2_time))

    print("=============================================rrr")
    print(minmax(1))
    return (minmax(1))
    print("--- %s seconds ---" % (time.time() - start_time))


def minmax(turn):
    result2 = np.zeros((8, 8, 8, 8, 8, 8))
    # if (curDepth == targetDepth):
    #    return result
    # if (maxTurn):
    #    return max(minmax(curDepth + 1, nodeIndex*2, False, result, targetDepth),
    #              minmax(curDepth + 1, nodeIndex*2+1, False, result, targetDepth))
    # else:
    #    return min(minmax(curDepth + 1, nodeIndex*2, True, result, targetDepth),
    #                minmax(curDepth + 1, nodeIndex*2+1, True, result, targetDepth))
    for i in range(1, 8):
        for j in range(1, 8):
            for k in range(1, 8):
                for l in range(1, 8):
                    for m in range(1, 8):
                        result2[i][j][k][l][m][0] = -2000
                        for n in range(1, 8):
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
                        result2[i][j][k][l][0][0] = -2000
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
                    result2[i][j][k][0][0][0] = -2000
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
                result2[i][j][0][0][0][0] = -2000
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
            result2[i][0][0][0][0][0] = -2000
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

    for i in range(1, 8):
        result2[0][0][0][0][0][0] = -2000
        if turn == 0:
            if result2[0][0][0][0][0][0] == -2000:
                result2[0][0][0][0][0][0] = result2[i][0][0][0][0][0]
            else:
                result2[0][0][0][0][0][0] = (result2[i][0][0][0][0][0] if result2[0][0][0][0][0][0] > \
                                                                          result2[i][0][0][0][0][0] else \
                                                 result2[0][0][0][0][0][0])
        else:
            if result2[0][0][0][0][0][0] == 2000:
                result2[0][0][0][0][0][0] = result2[i][0][0][0][0][0]
            else:
                result2[0][0][0][0][0][0] = (result2[i][0][0][0][0][0] if result2[0][0][0][0][0][0] < \
                                                                          result2[i][0][0][0][0][0] else \
                                                 result2[0][0][0][0][0][0])
    for i in range(1, 8):
        if result2[i][0][0][0][0][0] == result2[0][0][0][0][0][0]:
            return i-1


def go_2_depth(con, originalTableName, i, j, map, turn):
    nextRow = find_next_row(j, map)
    if (nextRow != -1):  # row 안꽉찼을경우
        cur = con.cursor()
        tableName = "WINNING_LINE" + str(i) + str(j) + str(3)
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
        tempMap[ord(nextRow) - 65][j - 1] = -1
        for k in range(1, 8):
            go_3_depth(con, tableName, i, j, k, tempMap, 1)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)


def go_3_depth(con, originalTableName, i, j, k, map, turn):
    nextRow = find_next_row(k, map)
    if (nextRow != -1):  # row 안꽉찼을경우
        cur = con.cursor()
        tableName = "WINNING_LINE" + str(i) + str(j) + str(k) + str(3)
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
            go_4_depth(con, tableName, i, j, k, l, tempMap, 0)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)


def go_4_depth(con, originalTableName, i, j, k, l, map, turn):
    nextRow = find_next_row(l, map)
    if (nextRow != -1):  # row 안꽉찼을경우
        cur = con.cursor()
        tableName = "WINNING_LINE" + str(i) + str(j) + str(k) + str(l) + str(3)
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
        tempMap[ord(nextRow) - 65][l - 1] = -1
        for m in range(1, 8):
            go_5_depth(con, tableName, i, j, k, l, m, tempMap, 1)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)


def go_5_depth(con, originalTableName, i, j, k, l, m, map, turn):
    nextRow = find_next_row(m, map)
    if (nextRow != -1):  # row 안꽉찼을경우
        cur = con.cursor()
        tableName = "WINNING_LINE" + str(i) + str(j) + str(k) + str(l) + str(m) + str(3)
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
            go_6_depth(con, tableName, i, j, k, l, m, n, tempMap, 0)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)


def go_6_depth(con, originalTableName, i, j, k, l, m, n, map, turn):
    nextRow = find_next_row(n, map)
    if (nextRow != -1):  # row 안꽉찼을경우
        cur = con.cursor()
        tableName = "WINNING_LINE" + str(i) + str(j) + str(k) + str(l) + str(m) + str(n) + str(3)
        sql = "CREATE TABLE " + tableName + " AS SELECT * FROM " + originalTableName + ";"
        cur.execute(sql)
        if (turn == 0):  # AI가 놓는경우
            sql = "UPDATE " + tableName + " SET PLAYER = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(n) + nextRow + "%"})
        else:
            sql = "UPDATE " + tableName + " SET AI = 0 WHERE LINE LIKE :position"
            cur.execute(sql, {"position": "%" + str(n) + nextRow + "%"})

        result[i][j][k][l][m][n] = calculate_heuristic(con, tableName)

        # tempMap = copy.deepcopy(map)
        # tempMap[ord(nextRow) - 65][n - 1] = -1
        # for o in range(1, 8):
        #     go_7_depth(con, tableName, i, j, k, l, m, n, o, tempMap, 1)

        sql = "DROP TABLE IF EXISTS " + tableName + ";"
        cur.execute(sql)


# def go_7_depth(con, originalTableName, i, j, k, l, m, n, o, map, turn):
#     nextRow = find_next_row(o, map)
#     if (nextRow != -1):  # row 안꽉찼을경우
#         cur = con.cursor()
#         tableName = "WINNING_LINE" + str(i) + str(j) + str(k) + str(l) + str(m) + str(n) + str(o) + str(3)
#         sql = "CREATE TABLE " + tableName + " AS SELECT * FROM " + originalTableName + ";"
#         cur.execute(sql)
#         if (turn == 0): # AI가 놓는경우
#             sql = "UPDATE " + tableName + " SET PLAYER = 0 WHERE LINE LIKE :position"
#             cur.execute(sql, {"position": "%" + str(o) + nextRow + "%"})
#         else:
#             sql = "UPDATE " + tableName + " SET AI = 0 WHERE LINE LIKE :position"
#             cur.execute(sql, {"position": "%" + str(o) + nextRow + "%"})
#
#         result[i][j][k][l][m][n][o][0] = calculate_heuristic(con, tableName)
#         tempMap = copy.deepcopy(map)
#         tempMap[ord(nextRow) - 65][o - 1] = -1
#
#         for p in range(1, 8):
#             go_8_depth(con, tableName, i, j, k, l, m, n, o, p, tempMap, 0)
#
#         sql = "DROP TABLE IF EXISTS " + tableName + ";"
#         cur.execute(sql)
#
# def go_8_depth(con, originalTableName, i, j, k, l, m, n, o, p, map, turn):
#     nextRow = find_next_row(p, map)
#     if (nextRow != -1):  # row 안꽉찼을경우
#         cur = con.cursor()
#         tableName = "WINNING_LINE" + str(i) + str(j) + str(k) + str(l) + str(m) + str(n) + str(o) + str(p) + str(3)
#         sql = "CREATE TABLE " + tableName + " AS SELECT * FROM " + originalTableName + ";"
#         cur.execute(sql)
#         if (turn == 0): # AI가 놓는경우
#             sql = "UPDATE " + tableName + " SET PLAYER = 0 WHERE LINE LIKE :position"
#             cur.execute(sql, {"position": "%" + str(p) + nextRow + "%"})
#         else:
#             sql = "UPDATE " + tableName + " SET AI = 0 WHERE LINE LIKE :position"
#             cur.execute(sql, {"position": "%" + str(p) + nextRow + "%"})
#
#         result[i][j][k][l][m][n][o][p] = calculate_heuristic(con, tableName)
#
#         sql = "DROP TABLE IF EXISTS " + tableName + ";"
#         cur.execute(sql)


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