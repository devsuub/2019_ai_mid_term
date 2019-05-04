def heuristic(map, last_betting_point):
    print("heuristic called", map);

    # 가로확인

    # 세로확인

    # 대각선 확인
    for i in range(6):
        for j in range(7):
            if map[i][j] == -1:
                if (i != 5) and (j != 0) and (map[i][j-1] != 0) and (map[i+1][j-1] == 0): # 왼쪽 대각선으로 하나 놓을수있는지 확인
                    if (i != 0) and (j != 6) and (map[i-1][j+1] == -1): # 2개연결됬는지 확인
                        if (i - 1 != 0) and (j + 1 != 6) and (map[i - 2][j + 2] == -1):  # 3개 연결됬는지 확인
                            # TODO 3칸짜리 점수
                            break;
                        else:
                            if (i + 1 != 5) and (j-1 != 0) and (map[i+2][j-2] == 0): # 2개 연결할 공간있는지 확인
                                # TODO 2칸짜리 점수
                                break;
                    else:
                        if (i + 1 != 5) and (j - 1 != 0) and (map[i + 2][j - 2] == 0):  # 2개 연결할 공간있는지 확인
                            if (i + 2 != 5) and (j - 2 != 0) and (map[i + 3][j - 3] == 0):  # 3개 연결할 공간있는지 확인
                                # TODO 1칸짜리 점수
                                break;

                if (i != 5) and (j != 6) and (map[i][j+1] != 0) and (map[i+1][j+1] == 0): # 오른쪽 대각선으로 하나 놓을수 있는지 확인
                    if (i != 0) and (j != 0) and (map[i-1][j-1] == -1): # 2개 연결됬는지 확인
                        if (i - 1 != 0) and (j - 1 != 0) and (map[i - 2][j - 2] == -1):  # 3개 연결 됬는지 확인
                            # TODO 3칸짜리 점수
                            break;
                        else:
                            if (i + 1 != 5) and (j + 1 != 6) and (map[i+2][j+2] == 0): # 2개 연결할 공간있는지 확인
                                # TODO 2칸짜리 점수
                                break;
                    else: # 1개 밖에 연결안된 경우
                        if (i + 1 != 5) and (j + 1 != 6) and (map[i+2][j+2] == 0): # 2개 연결할 공간있는지 확인
                            if (i +2 != 5) and (j +2 != 6) and (map[i+3][j+3] == 0):
                                # TODO 1칸짜리 점수
                                break;

    return 0