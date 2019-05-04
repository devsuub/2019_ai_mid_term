def heuristic(map, last_betting_point):
    print("heuristic called", map);

    # 가로확인

    # 세로확인

    # 대각선 확인
    for i in range(6):
        for j in range(7):
            if map[i][j] == -1:
                if (i != 5) and (j != 0) and (map[i][j-1] != 0) and (map[i+1][j-1] == 0):
                    # 가능 TODO 점수
                    if (i != 0) and (j != 6) and (map[i-1][j+1] == -1):
                        # 2칸짜리 TODO 점수
                        if (i-1 != 0) and (j+1 != 6) and (map[i-2][j+2] == -1):
                            # 3칸짜리 TODO 점수

                if (i != 5) and (j != 6) and (map[i][j+1] != 0) and (map[i+1][j+1] == 0):
                    # 가능 TODO 점수
                    if (i != 0) and (j != 0) and (map[i-1][j-1] == -1):
                        # 2칸짜리 TODO 점수
                        if (i -1 != 0) and (j-1 != 0) and (map[i-2][j-2] == -1):
                            # 3칸짜리 TODO 점수



    return 0