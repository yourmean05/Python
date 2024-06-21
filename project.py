import turtle
import random

# 창 설정
turtle.setup(1075, 1075)
turtle.title("내 땅 밟으면, 넌 나가라.")
turtle.bgcolor("black")

# 초기값 설정
end = 0
num = 0
player_num = 2
player_xy = [[(-10, 10)], [(10, -10)], [(10, 10)], [(-10, -10)]]
player_alive = [1, 1, 0, 0]
player_color = ("red", "royalblue2", "seagreen3", "violet")
xy = [()]
turn = 0
distance = 0
min_distance = random.randint(3, 5)
max_distance = random.randint(10, 15)
turtle.shape("square")
turtle.speed(0)
screen = turtle.Screen()

# 시작 화면 출력
title_screen = turtle.Turtle()
title_screen.penup()
title_screen.hideturtle()
title_screen.goto(0, 100)
title_screen.pencolor("white")
title_screen.write("내 땅 밟으면, 넌 나가라", align="center", font=("Arial", 24, "bold"))

# 게임 설명
def explain():
    message = """
    게임 설명:
    '↑', '↓', '←', '→' 화살표 키를 사용하여 이동합니다.
    'space bar'를 눌러 이동을 멈추고 차례를 넘깁니다.
    
    알 수 없는 '이동거리'를 고려하며,
    다른 플레이어의 영역을 밟지 않고 최대한 많은 공간을 확보하세요!
    """
    turtle.hideturtle()
    check = turtle.textinput("게임 설명", message)
    return check

# 출력 되돌리는 함수
def undo(undo_num = 1):
    for _ in range(undo_num*16):
        turtle.undo()

# 사각형 출력 및 이동 함수
def draw_square(x, y, color):
    turtle.color(player_color[color], player_color[color])
    turtle.pu()
    turtle.goto(50*x-25, 50*y+25)
    turtle.pd()
    turtle.begin_fill( )
    turtle.setheading(0)
    turtle.forward(50)
    turtle.setheading(270)
    turtle.forward(50)
    turtle.setheading(180)
    turtle.forward(50)
    turtle.setheading(90)
    turtle.forward(50)
    turtle.end_fill( )
    turtle.pu()
    turtle.color("white")
    turtle.goto(50*x, 50*y)

# 경계선 출력 함수
def print_screen():
    turtle.clear()
    turtle.color("white")
    turtle.pu()
    turtle.goto(-525, -525)
    turtle.pd()
    turtle.goto(-525, 525)
    turtle.goto(525, 525)
    turtle.goto(525, -525)
    turtle.goto(-525, -525)
    global player_xy
    global num
    for i in player_xy:
        for x, y in i:
            draw_square(x, y, num)
        num += 1
    num = 0

# 위로 이동 함수
def go_up():
    global turn
    global distance
    global xy
    if xy[-1][1] < 10:
        a = [0, 1, 2, 3]
        a.remove(turn)
        if (xy[-1][0], xy[-1][1]+1) in (player_xy[a[0]] + player_xy[a[1]] + player_xy[a[2]]): # 탈락 판단
            distance = set(xy) - set(player_xy[turn])
            distance = len(distance)
            undo(distance)
            player_alive[turn] = 0
            turn += 1
            if turn == player_num:
                turn = 0
            xy = [()]
            play()
        else:
            draw_square(xy[-1][0], xy[-1][1]+1, turn)
            xy += [(xy[-1][0], xy[-1][1]+1)]

# 밑으로 이동 함수
def go_down():
    global turn
    global distance
    global xy
    if xy[-1][1] > -10:
        a = [0, 1, 2, 3]
        a.remove(turn)
        if (xy[-1][0], xy[-1][1]-1) in (player_xy[a[0]] + player_xy[a[1]] + player_xy[a[2]]): # 탈락 판단
            distance = set(xy) - set(player_xy[turn])
            distance = len(distance)
            undo(distance)
            player_alive[turn] = 0
            turn += 1
            if turn == player_num:
                turn = 0
            xy = [()]
            play()
        else:
            draw_square(xy[-1][0], xy[-1][1]-1, turn)
            xy += [(xy[-1][0], xy[-1][1]-1)]

# 좌로 이동 함수
def go_left():
    global turn
    global distance
    global xy
    if xy[-1][0] > -10:
        a = [0, 1, 2, 3]
        a.remove(turn)
        if (xy[-1][0]-1, xy[-1][1]) in (player_xy[a[0]] + player_xy[a[1]] + player_xy[a[2]]): # 탈락 판단
            distance = set(xy) - set(player_xy[turn])
            distance = len(distance)
            undo(distance)
            distance = 0
            player_alive[turn] = 0
            turn += 1
            if turn == player_num:
                turn = 0
            xy = [()]
            play()
        else:
            draw_square(xy[-1][0]-1, xy[-1][1], turn)
            xy += [(xy[-1][0]-1, xy[-1][1])]

# 우로 이동 함수
def go_right():
    global turn
    global distance
    global xy
    if xy[-1][0] < 10:
        a = [0, 1, 2, 3]
        a.remove(turn)
        if (xy[-1][0]+1, xy[-1][1]) in (player_xy[a[0]] + player_xy[a[1]] + player_xy[a[2]]): # 탈락 판단
            distance = set(xy) - set(player_xy[turn])
            distance = len(distance)
            undo(distance)
            player_alive[turn] = 0
            turn += 1
            if turn == player_num:
                turn = 0
            xy = [()]
            play()
        else:
            draw_square(xy[-1][0]+1, xy[-1][1], turn)
            xy += [(xy[-1][0]+1, xy[-1][1])]

# 턴 종료 함수
def stop():
    global turn
    global distance
    global xy
    distance = set(xy) - set(player_xy[turn])
    distance = len(distance)
    if distance < min_distance:
        undo(distance)
        distance = 0
        xy = [()]
        play()

    elif distance > max_distance:
        undo(distance)
        distance = 0
        turn += 1
        if turn == player_num:
            turn = 0
        xy = [()]
        play()

    else:
        distance = 0
        for i in xy:
            if i not in player_xy[turn]:
                player_xy[turn] += [i]
        turn += 1
        if turn == player_num:
            turn = 0
        xy = [()]
        play()

# 게임 진행 함수
def play():
    global end
    global turn
    global xy
    global player_alive
    turtle.showturtle()
    if player_alive.count(1) == 1: # 승리 판단
        if end == 0:
            turtle.reset()
            turtle.color("white")
            turtle.write(f'{player_alive.index(1)+1}번 플레이어 승리', align="center", font=("Arial", 50))
            draw_square(player_xy[player_alive.index(1)][-1][0], player_xy[player_alive.index(1)][-1][1], player_alive.index(1))
            end += 1
    if player_alive[turn] != 1: # 탈락자 판단
        turn += 1
        if turn == player_num:
            turn = 0
        play()
    turtle.pu()
    turtle.goto(player_xy[turn][-1][0]*50, player_xy[turn][-1][1]*50)
    xy[0] = player_xy[turn][-1]
    screen.onkey(stop, 'space')
    screen.onkey(go_up, 'Up')
    screen.onkey(go_down, 'Down')
    screen.onkey(go_left, 'Left')
    screen.onkey(go_right, 'Right')

player_num = turtle.numinput("플레이어 수 (2~4)", "플레이어 수를 입력하시오", 2, 2, 4)
title_screen.clear() # 맵 출력 전 제목 지우기
check = explain()
while check is None: # 설명문 출력했는지 체크
    check = explain()

if player_num == 3:
    player_alive[2] = 1

if player_num == 4:
    player_alive[2] = 1
    player_alive[3] = 1

print_screen()
play()

screen.listen()
turtle.done()