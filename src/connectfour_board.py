# Import
import sqlite3
import update
from heuristic import heuristic
from ruleBase import ruleBase
from init import init
con = sqlite3.connect(':memory:')

def startTurn(turn, board):     #게임 진행하기
    try:
        player_input = 0            #플레이어 인풋 초기화
        prev_input = [-1] * 2
        if turn == 1:
            while player_input != '1' and player_input != '2' and player_input != '3' and player_input != '4' and player_input != '5' and player_input != '6' and player_input != '7':
                player_input = input("플레이어 차례입니다. 두실 위치를 입력하세요 : ")
                #
                if player_input == 'DUMP':
                    ## DUMP
                    print(board)

                    with open('dump.sql', 'w') as f:
                        f.write("===========================================================\n")
                        for line in con.iterdump():
                            if line.startswith('INSERT INTO "WINNING_LINE"'):
                                f.write('%s\n' % line)
                        f.close

                elif player_input != '1' and player_input != '2' and player_input != '3' and player_input != '4' and player_input != '5' and player_input != '6' and player_input != '7':
                    print("그곳에 두실 수 없습니다!")

                else:
                    for i in range(6):
                        #판에 둘 위치 찾기
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

                        if board[i][int(player_input) - 1] == 0:
                            board[i][int(player_input) - 1] = 1
                            prev_input[0] = i
                            prev_input[1] = int(player_input) - 1
                            update.update_people_play(con, str(player_input) + alphabet)
                            return board, True, prev_input
                        else:
                            if i == 5:
                                print("Column " + player_input + " is already full. Please select another column.")
                                return board, False, prev_input
        else:
            ai_input = ruleBase(board) #룰베이스에서 먼저 가져오기
            if (ai_input == -1):
                ai_input = heuristic(con, board)  # 휴리스틱 함수 사용하여 AI 인풋 결정

            for i in range(6):
                if board[i][ai_input] == 0:
                    board[i][ai_input] = -1
                    prev_input[0] = i
                    prev_input[1] = ai_input

                    if i == 0: #위치
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

                    print("( AI placed it on ", str(ai_input + 1)+alphabet, ")")
                    update.update_ai_play(con, str(ai_input + 1)+alphabet) #위닝라인 업데이트
                    return board, True, prev_input
                else:
                    if i == 5:
                        return board, False, prev_input
    except:
        print("ERROR 발생")
        print(board)

        with open('dump.sql', 'w') as f:
            f.write("===========================================================\n")
            for line in con.iterdump():
                if line.startswith('INSERT INTO "WINNING_LINE"'):
                    f.write('%s\n' % line)
            f.close

def GameStatus(board, order, status):
    finish_turn = False
    coord = [['.'] * 7 for i in range(6)]

    print("---------------------------------------")
    while not finish_turn:
        board, finish_turn, prev_coord = startTurn(order, board)
    status.append(prev_coord[1] + 1)
    for i in range(6):
        for j in range(7):
            if board[i][j] == 1:
                coord[i][j] = '★'
            elif board[i][j] == -1:
                coord[i][j] = '●'
            else:
                coord[i][j] = '○'


    print()
    print("* 1  2  3  4  5  6  7 *")
    print("+ ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ+ ")
    print('F', coord[5][0], coord[5][1], coord[5][2], coord[5][3], coord[5][4], coord[5][5], coord[5][6], '#')
    print('E', coord[4][0], coord[4][1], coord[4][2], coord[4][3], coord[4][4], coord[4][5], coord[4][6], '#')
    print('D', coord[3][0], coord[3][1], coord[3][2], coord[3][3], coord[3][4], coord[3][5], coord[3][6], '#')
    print('C', coord[2][0], coord[2][1], coord[2][2], coord[2][3], coord[2][4], coord[2][5], coord[2][6], '#')
    print('B', coord[1][0], coord[1][1], coord[1][2], coord[1][3], coord[1][4], coord[1][5], coord[1][6], '#')
    print('A', coord[0][0], coord[0][1], coord[0][2], coord[0][3], coord[0][4], coord[0][5], coord[0][6], '#')
    print("+ ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ+ ")
    print()
    print("You: ★ , CPU: ●")
    print("State: " + ''.join(str(i) for i in status))

    order *= -1
    return board, order, prev_coord, status

def countStoneInGames(board, prev_coord, column_direction, row_direction, count):

    column_address = prev_coord[0]
    row_address = prev_coord[1]
    next_column_address = column_address + column_direction
    next_row_address = row_address + row_direction

    if next_column_address < 0 or next_column_address > 5 or next_row_address < 0 or next_row_address > 6:
        return count
    elif board[next_column_address][next_row_address] != board[column_address][row_address]:
        return count
    else:
        next_checking_point = [next_column_address, next_row_address]
        return countStoneInGames(board, next_checking_point, column_direction, row_direction, count + 1)

def checkMapIsFull(board):
    for i in range(6):
        for j in range(7):
            if board[i][j] == 0:
                return False
    return True


def gameOver(board, prev_coord, order):
    winner = None
    if countStoneInGames(board, prev_coord, -1, 0, 0) + countStoneInGames(board, prev_coord, 1, 0, 0) >= 3:
        winner = order * -1
        return True, winner
    elif countStoneInGames(board, prev_coord, 0, -1, 0) + countStoneInGames(board, prev_coord, 0, 1,
                                                                            0) >= 3:
        winner = order * -1
        return True, winner
    elif countStoneInGames(board, prev_coord, -1, 1, 0) + countStoneInGames(board, prev_coord, 1, -1,
                                                                            0) >= 3:
        winner = order * -1
        return True, winner
    elif countStoneInGames(board, prev_coord, -1, -1, 0) + countStoneInGames(board, prev_coord, 1, 1,
                                                                             0) >= 3:
        winner = order * -1
        return True, winner
    elif checkMapIsFull(board):
        winner = 0
        return True, winner
    else:
        return False, winner


def startGame():    #게임시작함수
    game_input = '' #게임인풋 초기화
    order = 0       #순서 정하기위함
    board = [[0] * 7 for i in range(6)]     #게임판
    status = []                             #상태
    while game_input != '1' and game_input != '2':
        game_input = input("선공은 1, 후공은 2를 선택하세요 : ")

        if game_input == '1':
            print()
            print("* 1 2 3 4 5 6 7  *")
            print("+ - - - - - - - + ")
            print('F ○○○○○○○ #')
            print('E ○○○○○○○ #')
            print('D ○○○○○○○ #')
            print('C ○○○○○○○ #')
            print('B ○○○○○○○ #')
            print('A ○○○○○○○ #')
            print("+ - - - - - - - + ")
            print()
            print("플레이어 먼저 시작합니다")
            order = 1       #플레이어 먼저 순서
            break
        elif game_input == '2':
            print("인공지능이 먼저 시작합니다")
            order = -1      #AI 먼저 순서
            break
        else:
            print("잘못 입력하셨습니다. 다시 선택하세요.")
    while True:
        board, order, prev_coord, status = GameStatus(board, order, status)
        game_over, winner = gameOver(board, prev_coord, order)
        if game_over:
            print()
            print("---------------------------------------")
            print("-------------- 게임 오버 --------------")
            if winner == 1:
                print("--------------- 승리 ---------------")
            elif winner == -1:
                print("--------------- 패배 ---------------")
            else:
                print("---------------- 무승부! ----------------")
            print("---------------------------------------")
            print()
            break

proceed_game = ''
init(con)
print()
print("------------------------------------------")
print("----커넥트 포 게임에 오신걸 환영합니다----")
print("------------------------------------------")
print("------------------------------------------")
print("-------made by 김민섭 임재민 이정섭-------")
print("------------------------------------------")
print()
startGame()

while proceed_game != 'Y' and proceed_game != 'y' and proceed_game != 'N' and proceed_game != 'n':
    proceed_game = input("Play Again? (Y/N) : ")

    if proceed_game == 'Y' or proceed_game == 'y':
        print()
        print("----------------------------------------")
        print("------------ 게임 다시 시작 ------------")
        print("----------------------------------------")
        print()
        proceed_game = ''
        startGame()
    elif proceed_game == 'N' or proceed_game == 'n':
        print()
        print("————————————————————")
        print("———— 게임 종료 ————")
        print("————————————————————")
        print()
        break
    else:
        print("잘못 입력하셨습니다. 다시 선택하세요")