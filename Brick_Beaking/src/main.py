# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       mengc                                                        #
# 	Created:      2025/5/24 19:04:16                                           #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #


from vex import *

brain = Brain()  # 创建主控

# 设置屏幕分辨率
WIDTH = 480
HEIGHT = 240

# 设置常量
BALL_RADIUS = 12  # 球半径
PABBLE_WIDTH = 100  # 球拍宽度
PABBLE_HEIGHT = 20  # 球拍高度
BRICK_ROW = 5  # 磁砖行数
BRICK_COL = 10  # 磁砖列数
BRICK_WIDTH = WIDTH//BRICK_COL  # 磁砖宽度
BRICK_HEIGHT = HEIGHT / 3//BRICK_ROW  # 磁砖高度


bricks = []  # 磁砖列表
# 初始化磁砖
for i in range(BRICK_ROW):
    bricks.append([True] * BRICK_COL)

# 设置变量
ball_x = WIDTH // 2
ball_y = HEIGHT // 2

ball_speed_x = 2
ball_speed_y = -2

pabble_x = (WIDTH - PABBLE_WIDTH) // 2

# 球的位置函数


def ball_position():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    if ball_y-BALL_RADIUS < 0 or ball_y + BALL_RADIUS > HEIGHT:
        ball_speed_y = -ball_speed_y
    if ball_x-BALL_RADIUS < 0 or ball_x + BALL_RADIUS > WIDTH:
        ball_speed_x = -ball_speed_x

# 球拍的位置函数


def pabble_position():
    global pabble_x
    if brain.screen.pressing():
        if brain.screen.x_position() < WIDTH//2:
            pabble_x -= 5
        if brain.screen.x_position() > WIDTH//2:
            pabble_x += 5
        if pabble_x < 0:
            pabble_x = 0
        if pabble_x > WIDTH - PABBLE_WIDTH:
            pabble_x = WIDTH - PABBLE_WIDTH


# 碰撞检测函数
def collision():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, pabble_x
    if (ball_x + BALL_RADIUS > pabble_x and ball_x - BALL_RADIUS < pabble_x + PABBLE_WIDTH) and (ball_y + BALL_RADIUS > HEIGHT - PABBLE_HEIGHT):
        ball_speed_y = -ball_speed_y


# 绘制小球函数
def draw_ball(x, y):
    brain.screen.set_pen_color(Color.RED)  # 设置画笔颜色为红色
    brain.screen.set_fill_color(Color.RED)
    brain.screen.draw_circle(x, y, BALL_RADIUS)

# 绘制球拍函数


def draw_pabble(x):
    brain.screen.set_pen_color(Color.BLUE)  # 设置画笔颜色为蓝色
    brain.screen.set_fill_color(Color.BLUE)
    brain.screen.draw_rectangle(
        x, HEIGHT - PABBLE_HEIGHT, PABBLE_WIDTH, PABBLE_HEIGHT)

# 绘制磁砖函数


def draw_brick():
    for i in range(BRICK_ROW):
        for j in range(BRICK_COL):
            if bricks[i][j]:
                brain.screen.set_pen_color(Color.GREEN)  # 设置画笔颜色为绿色
                brain.screen.set_fill_color(Color.GREEN)
                brain.screen.draw_rectangle(
                    j * BRICK_WIDTH+1, i * BRICK_HEIGHT+1, BRICK_WIDTH-2, BRICK_HEIGHT-2)


while True:
    brain.screen.clear_screen()  # 清屏

    ball_position()  # 更新小球位置
    pabble_position()  # 更新球拍位置

    collision()  # 碰撞检测

    draw_brick()  # 绘制磁砖
    draw_pabble(pabble_x)  # 绘制球拍
    draw_ball(ball_x, ball_y)  # 绘制小球

    brain.screen.render()  # 刷新屏幕
    wait(20)
