def ruleBase(map):
    # 첫번째 줄 3번칸이 비었을 경우 3에 넣는다
    if (map[0][2] == 0):
        print("AI : 첫번째 줄 3번칸이 비어서 3에다 놓았습니다")
        return 2
    # 첫번째 줄 4번이 비었을경우 4에 넣는다
    elif (map[0][3] == 0):
        print("AI : 어랏, 첫번째 줄 4번이 비어서 여기다 놓습니다")
        return 3
    else:
        return -1

    # 가로확인

    # 세로확인

    # 대각선 확인
    # for i in range(6):
    #     for j in range(7):
    #         if map[i][j] == -1:
    #             if (i != 5) and (j != 0) and (map[i][j-1] != 0) and (map[i+1][j-1] == 0): # 왼쪽 대각선으로 하나 놓을수있는지 확인
    #                 if (i != 0) and (j != 6) and (map[i-1][j+1] == -1): # 2개연결됬는지 확인
    #                     if (i - 1 != 0) and (j + 1 != 6) and (map[i - 2][j + 2] == -1):  # 3개 연결됬는지 확인
    #                         return i+1,j-1
    #                         break
    #                     else:
    #                         if (i + 1 != 5) and (j-1 != 0) and (map[i+2][j-2] == 0): # 2개 연결할 공간있는지 확인
    #                             #2칸
    #                             break
    #                 # else:
    #                 #     if (i + 1 != 5) and (j - 1 != 0) and (map[i + 2][j - 2] == 0):  # 2개 연결할 공간있는지 확인
    #                 #         if (i + 2 != 5) and (j - 2 != 0) and (map[i + 3][j - 3] == 0):  # 3개 연결할 공간있는지 확인
    #                 #             # 1칸
    #                 #             break
    #
    #             if (i != 5) and (j != 6) and (map[i][j+1] != 0) and (map[i+1][j+1] == 0): # 오른쪽 대각선으로 하나 놓을수 있는지 확인
    #                 if (i != 0) and (j != 0) and (map[i-1][j-1] == -1): # 2개 연결됬는지 확인
    #                     if (i - 1 != 0) and (j - 1 != 0) and (map[i - 2][j - 2] == -1):  # 3개 연결 됬는지 확인
    #                         # 3칸짜리 점수
    #                         return i+1, j+1
    #                         break
    #                     else:
    #                         if (i + 1 != 5) and (j + 1 != 6) and (map[i+2][j+2] == 0): # 2개 연결할 공간있는지 확인
    #                             # 2칸
    #                             break
    #                 # else: # 1개 밖에 연결안된 경우
    #                 #     if (i + 1 != 5) and (j + 1 != 6) and (map[i+2][j+2] == 0): # 2개 연결할 공간있는지 확인
    #                 #         if (i +2 != 5) and (j +2 != 6) and (map[i+3][j+3] == 0):
    #                 #             # TODO 1칸짜리 점수
    #                 #             break;
    #
    #         if map[i][j] == 1:
    #             if (i != 5) and (j != 0) and (map[i][j-1] != 0) and (map[i+1][j-1] == 0): # 왼쪽 대각선으로 하나 놓을수있는지 확인
    #                 if (i != 0) and (j != 6) and (map[i-1][j+1] == 1): # 2개연결됬는지 확인
    #                     if (i - 1 != 0) and (j + 1 != 6) and (map[i - 2][j + 2] == 1):  # 3개 연결됬는지 확인
    #                         return i+1,j-1
    #                         break
    #                     else:
    #                         if (i + 1 != 5) and (j-1 != 0) and (map[i+2][j-2] == 0): # 2개 연결할 공간있는지 확인
    #                             #2칸
    #                             break
    #                 # else:
    #                 #     if (i + 1 != 5) and (j - 1 != 0) and (map[i + 2][j - 2] == 0):  # 2개 연결할 공간있는지 확인
    #                 #         if (i + 2 != 5) and (j - 2 != 0) and (map[i + 3][j - 3] == 0):  # 3개 연결할 공간있는지 확인
    #                 #             # 1칸
    #                 #             break
    #
    #             if (i != 5) and (j != 6) and (map[i][j+1] != 0) and (map[i+1][j+1] == 0): # 오른쪽 대각선으로 하나 놓을수 있는지 확인
    #                 if (i != 0) and (j != 0) and (map[i-1][j-1] == 1): # 2개 연결됬는지 확인
    #                     if (i - 1 != 0) and (j - 1 != 0) and (map[i - 2][j - 2] == 1):  # 3개 연결 됬는지 확인
    #                         # 3칸짜리 점수
    #                         return i+1, j+1
    #                         break
    #                     else:
    #                         if (i + 1 != 5) and (j + 1 != 6) and (map[i+2][j+2] == 0): # 2개 연결할 공간있는지 확인
    #                             # 2칸
    #                             break
    #                 # else: # 1개 밖에 연결안된 경우
    #                 #     if (i + 1 != 5) and (j + 1 != 6) and (map[i+2][j+2] == 0): # 2개 연결할 공간있는지 확인
    #                 #         if (i +2 != 5) and (j +2 != 6) and (map[i+3][j+3] == 0):
    #                 #             # TODO 1칸짜리 점수
    #                 #             break;