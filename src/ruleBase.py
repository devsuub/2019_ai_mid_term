def ruleBase(map):
    # 첫번째 줄 3번칸이 비었을 경우 3에 넣는다
    if (map[0][2] == 0):
        return 2
    # 첫번째 줄 4번이 비었을경우 4에 넣는다
    elif (map[0][3] == 0):
        return 3
    else:
        return -1
