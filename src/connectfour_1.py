# Import
import sqlite3
import update
from random import randint
from heuristic import heuristic
from init import init

con = sqlite3.connect(':memory:')

def select_all_table(con):
    cur = con.cursor()
    cur.execute("SELECT * FROM WINNING_LINE")
    for row in cur:
        print(row)

# 선택한 열에 착수하는 함수
def betting(turn, map):
    human_bet = 0
    last_betting_point = [-1] * 2
    if turn == 1:   # 사람 차례
        while human_bet != '1' and human_bet != '2' and human_bet != '3' and human_bet != '4' and human_bet != '5' and human_bet != '6' and human_bet != '7':
            human_bet = input("Where do you want to bet? (1~7) : ")

            # 테스트용 코드
            # human_bet = str(randint(1, 7))    # 사람 차례에도 랜덤하게 두기

            if human_bet != '1' and human_bet != '2' and human_bet != '3' and human_bet != '4' and human_bet != '5' and human_bet != '6' and human_bet != '7':
                print("Wrong Input. Please try it again.")
            else:
                for i in range(6):
                    if map[i][int(human_bet)-1] == 0:
                        map[i][int(human_bet)-1] = 1
                        last_betting_point[0] = i
                        last_betting_point[1] = int(human_bet)-1  #마지막 착수점 저장

                        # 테스트용 코드
                        # print(last_betting_point)   # 마지막 착수점 출력
                        return map, True, last_betting_point
                    else:
                        if i == 5:
                            print("Column "+human_bet+" is already full. Please select another column.")
                            return map, False, last_betting_point
    else:   # 컴퓨터 차례

        # 테스트용 코드
        heuristic(con, map)
        # cpu_bet = randint(0, 6) # 1~7열 사이에 랜덤하게 착수하기
        # cpu_bet = 6   # 6열에만 수 두기

        for i in range(6):
            if map[i][cpu_bet] == 0:
                map[i][cpu_bet] = -1
                last_betting_point[0] = i
                last_betting_point[1] = cpu_bet

                # 테스트용 코드
                # print(last_betting_point)   # 마지막 착수점 출력

                if i == 0:
                    alphabet = 'A'
                elif i == 1:
                    alphabet = 'B'
                elif i == 2:
                    alphabet = 'C'
                elif i == 3:
                    alphabet = 'D'
                elif i == 4:
                    alphabet = 'E'
                else:
                    alphabet = 'F'
                print("( CPU betted",alphabet+str(cpu_bet+1),")")
                return map, True, last_betting_point
            else:
                if i == 5:

                    # 테스트용 코드
                    # print("Column "+str(cpu_bet+1)+" is already full. Please select another column.")   # 컴퓨터가 두려는 열이 꽉찼음을 출력

                    return map, False, last_betting_point

# 착수할 열을 선택하고 착수 결과를 보여주는 함수
def gameProgressing(map, turn, state):
    success_betting = False
    dot = [['.'] * 7 for i in range(6)]
    print("---------------------------------------")
    while not success_betting:
        map, success_betting, last_betting_point = betting(turn, map)
    state.append(last_betting_point[1]+1)
    for i in range(6):
        for j in range(7):
            if map[i][j] == 1:
                dot[i][j] = '○'
            elif map[i][j] == -1:
                dot[i][j] = '●'
            else:
                dot[i][j] = '.'
    print()
    print("# 1 2 3 4 5 6 7 #")
    print('F', dot[5][0], dot[5][1], dot[5][2], dot[5][3], dot[5][4], dot[5][5], dot[5][6], '#')
    print('E', dot[4][0], dot[4][1], dot[4][2], dot[4][3], dot[4][4], dot[4][5], dot[4][6], '#')
    print('D', dot[3][0], dot[3][1], dot[3][2], dot[3][3], dot[3][4], dot[3][5], dot[3][6], '#')
    print('C', dot[2][0], dot[2][1], dot[2][2], dot[2][3], dot[2][4], dot[2][5], dot[2][6], '#')
    print('B', dot[1][0], dot[1][1], dot[1][2], dot[1][3], dot[1][4], dot[1][5], dot[1][6], '#')
    print('A', dot[0][0], dot[0][1], dot[0][2], dot[0][3], dot[0][4], dot[0][5], dot[0][6], '#')
    print("# # # # # # # # #")
    print()
    print("You: ○ , CPU: ●")

    # 테스트용 코드
    print("State: "+''.join(str(i) for i in state))    # 현재 state 보여주기

    turn *= -1  # 턴 바꾸기
    return map, turn, last_betting_point, state    # 맵, 누구턴인지, 마지막 착수점, state 리턴

# 특정 방향에 같은 수가 연속으로 몇개 존재하는지 찾아내는 함수
def continuousBetting(map, last_betting_point, column_direction, row_direction, count):
    column_address = last_betting_point[0]
    row_address = last_betting_point[1]
    next_column_address = column_address + column_direction
    next_row_address = row_address + row_direction
    if next_column_address < 0 or next_column_address > 5 or next_row_address < 0 or next_row_address > 6:
        return count
    elif map[next_column_address][next_row_address] != map[column_address][row_address]:
        return count
    else:
        next_checking_point = [next_column_address, next_row_address]
        return continuousBetting(map, next_checking_point, column_direction, row_direction, count+1)

# 게임판이 꽉 찼는지 확인하는 함수
def checkMapIsFull(map):
    for i in range(6):
        for j in range(7):
            if map[i][j] == 0:
                return False
    return True

# 게임오버 인지 확인하는 함수
def gameOver(map, last_betting_point, turn):
    winner = None
    if continuousBetting(map,last_betting_point,-1,0,0) + continuousBetting(map,last_betting_point,1,0,0) >= 3:
        winner = turn * -1
        return True, winner
    elif continuousBetting(map,last_betting_point,0,-1,0) + continuousBetting(map,last_betting_point,0,1,0) >= 3:
        winner = turn * -1
        return True, winner
    elif continuousBetting(map,last_betting_point,-1,1,0) + continuousBetting(map,last_betting_point,1,-1,0) >= 3:
        winner = turn * -1
        return True, winner
    elif continuousBetting(map,last_betting_point,-1,-1,0) + continuousBetting(map,last_betting_point,1,1,0) >= 3:
        winner = turn * -1
        return True, winner
    elif checkMapIsFull(map):
        winner = 0
        return True, winner
    else:
        return False, winner

# 게임 실행 함수
def startGame():
    # update.update_people_play(con, position='1A')
    # update.update_ai_play(con, position='1A')
    #select_all_table(con)

    text_input = ''
    turn = 0
    map = [[0] * 7 for i in range(6)]
    state = []
    while text_input != 'F' and text_input != 'f' and text_input != 'S' and text_input != 's':
        text_input = input("Will you go First or Second? (F/S) : ")

        # 테스트용 코드
        # text_input = 'f'    # 무조건 선공하기

        if text_input == 'F' or text_input == 'f':
            print()
            print("# 1 2 3 4 5 6 7 #")
            print('F . . . . . . . #')
            print('E . . . . . . . #')
            print('D . . . . . . . #')
            print('C . . . . . . . #')
            print('B . . . . . . . #')
            print('A . . . . . . . #')
            print("# # # # # # # # #")
            print()
            print("You go First.")
            turn = 1
            break
        elif text_input == 'S' or text_input == 's':
            print("CPU go First.")
            turn = -1
            break
        else:
            print("Wrong Input. Please try it again.")
    while True: # 게임 진행 함수
        map, turn, last_betting_point, state = gameProgressing(map, turn, state)
        game_over, winner = gameOver(map, last_betting_point, turn)
        if game_over:   # 게임이 끝나면 누가 이겼는지 출력
            print()
            print("---------------------------------------")
            print("-------------- Game Over --------------")
            if winner == 1:
                print("--------------- You Win ---------------")
            elif winner == -1:
                print("--------------- CPU Win ---------------")
            else:
                print("---------------- Draw! ----------------")
            print("---------------------------------------")
            print()
            break

# 메인 함수
game_continue = ''
init(con)
print()
print("----------------------------------------")
print("---- Artificial Intellgence Project ----")
print("------------- Connect Four -------------")
print("------------- Human vs CPU -------------")
print("----------------------------------------")
print()
startGame()

while game_continue != 'Y' and game_continue != 'y' and game_continue != 'N' and game_continue != 'n':
    game_continue = input("Do you want to restart the game? (Y/N) : ")

    # 테스트용 코드
    # game_continue = 'y' # 게임 무한 재실행

    if game_continue == 'Y' or game_continue == 'y':
        print()
        print("----------------------------------------")
        print("------------- Game Restart -------------")
        print("----------------------------------------")
        print()
        game_continue = ''
        startGame()
    elif game_continue == 'N' or game_continue == 'n':
        print()
        print("----------------------------------------")
        print("-------- Game Engine Terminated --------")
        print("----------------------------------------")
        print()
        break
    else:
        print("Wrong Input. Please try it again.")