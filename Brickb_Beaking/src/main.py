from vex import *

brain = Brain()
screen = brain.screen

# 屏幕尺寸
WIDTH = 480
HEIGHT = 240

# 游戏参数
BALL_RADIUS = 6
PADDLE_WIDTH = 60
PADDLE_HEIGHT = 8
BRICK_ROWS = 4
BRICK_COLS = 8
BRICK_WIDTH = (WIDTH - (BRICK_COLS + 1) * 4) // BRICK_COLS
BRICK_HEIGHT = 16
PADDLE_SPEED = 6
BALL_SPEED = 3

# 球的初始速度
ball_dx = BALL_SPEED
ball_dy = -BALL_SPEED

# 初始位置
paddle_x = (WIDTH - PADDLE_WIDTH) / 2
paddle_y = HEIGHT - 20

ball_x = WIDTH / 2
ball_y = HEIGHT / 2

# 分数
score = 0

# 创建砖块矩阵
bricks = [[True for _ in range(BRICK_COLS)] for _ in range(BRICK_ROWS)]

# 颜色主题
BG_COLOR = Color.BLACK
BALL_COLOR = Color.YELLOW
PADDLE_COLOR = Color.WHITE
BRICK_COLORS = [Color.RED, Color.ORANGE, Color.GREEN, Color.BLUE]

# 触控状态
touching = False
touch_x = 0


def draw_bricks():
    """绘制所有未被击碎的砖块"""
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            if bricks[row][col]:
                x = col * (BRICK_WIDTH + 4) + 4
                y = row * (BRICK_HEIGHT + 4) + 20
                screen.set_fill_color(BRICK_COLORS[row % len(BRICK_COLORS)])
                screen.draw_rectangle(x, y, BRICK_WIDTH, BRICK_HEIGHT)


def draw_paddle(x):
    """绘制底板"""
    screen.set_fill_color(PADDLE_COLOR)
    screen.draw_rectangle(x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)


def draw_ball(x, y):
    """绘制球体"""
    screen.set_fill_color(BALL_COLOR)
    screen.draw_circle(int(x), int(y), BALL_RADIUS)


def check_collision():
    """检测球与墙壁、底板、砖块的碰撞"""
    global ball_dx, ball_dy, score,ball_y

    # 墙壁反弹
    if ball_x <= BALL_RADIUS or ball_x >= WIDTH - BALL_RADIUS:
        ball_dx *= -1
    if ball_y <= BALL_RADIUS:
        ball_dy *= -1

    # 底板反弹
    if (paddle_y <= ball_y + BALL_RADIUS <= paddle_y + PADDLE_HEIGHT and
        paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH):
        ball_dy *= -1
        ball_y = paddle_y - BALL_RADIUS  # 避免重复触发

    # 砖块碰撞
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            if bricks[row][col]:
                brick_x = col * (BRICK_WIDTH + 4) + 4
                brick_y = row * (BRICK_HEIGHT + 4) + 20
                if (brick_x <= ball_x <= brick_x + BRICK_WIDTH and
                    brick_y <= ball_y <= brick_y + BRICK_HEIGHT):
                    bricks[row][col] = False
                    ball_dy *= -1
                    score += 10
                    return


def touch_event():
    """持续跟踪手指位置控制底板"""
    global touching, touch_x
    if screen.pressing():
        x = screen.x_position()
        touch_x = x
        touching = True
    else:
        touching = False


def game_over():
    """显示游戏结束画面"""
    screen.clear_screen()
    screen.set_cursor(10, 15)
    screen.print("Game Over")
    screen.set_cursor(12, 15)
    screen.print("Score: %d"%score)
    while True:
        wait(100)


def win_game():
    """显示胜利画面"""
    screen.clear_screen()
    screen.set_cursor(10, 15)
    screen.print("You Win!")
    screen.set_cursor(12, 15)
    screen.print("Score: %d"%score)
    while True:
        wait(100)


# 主循环
while True:
    screen.clear_screen()

    # 处理触控输入
    touch_event()

    # 控制底板移动
    if touching:
        target_x = touch_x - PADDLE_WIDTH // 2
        target_x = max(0, min(target_x, WIDTH - PADDLE_WIDTH))
        paddle_x = target_x

    # 更新球的位置
    ball_x += ball_dx
    ball_y += ball_dy

    # 边界检查：球掉出底部 -> 游戏结束
    if ball_y > HEIGHT:
        game_over()
        break

    # 检查是否全部砖块已清除 -> 胜利
    all_clear = all(not any(row) for row in bricks)
    if all_clear:
        win_game()
        break

    # 绘图
    draw_bricks()
    draw_paddle(paddle_x)
    draw_ball(ball_x, ball_y)

    # 显示分数
    screen.set_pen_color(Color.WHITE)
    screen.set_cursor(1, 1)
    screen.print("Score: %d"%(score))

    # 碰撞检测
    check_collision()

    screen.render()
    wait(20, MSEC)