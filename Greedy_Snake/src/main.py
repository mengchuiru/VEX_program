# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       mengc                                                        #
# 	Created:      2025/2/17 14:24:29                                           #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import random


brain = Brain()
controller = Controller()



# VEX V5屏幕参数
SCREEN_WIDTH = 480  # 屏幕宽
SCREEN_HEIGHT = 240 # 屏幕高
CELL_SIZE = 20      # 蛇身大小
COLOR_BG = Color(0, 0, 0)
COLOR_SNAKE = Color(255, 255, 255)
COLOR_FOOD = Color(255, 0, 0)
COLOR_TEXT = Color(0, 255, 0)


class Game:
    def __init__(self):
        
        # 按键事件注册
        controller.buttonUp.pressed(self.dir_up)
        controller.buttonDown.pressed(self.dir_down)
        controller.buttonLeft.pressed(self.dir_left)
        controller.buttonRight.pressed(self.dir_right)
        # 初始化游戏状态
        self.reset_game()

    def reset_game(self):
        """重置游戏状态"""
        brain.screen.clear_screen()  # 清空屏幕
        self.snake = [(5, 5), (4, 5), (3, 5)]  # 初始蛇身坐标
        self.direction = (1, 0)  # 初始向右移动
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.loop_time = 150
        self.last_update = brain.timer.time()

    def generate_food(self):
        """生成食物位置"""
        while True:
            x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1)
            y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def dir_up(self):
        if self.direction != (0, 1):
            self.direction = (0, -1)

    def dir_down(self):
        if self.direction != (0, -1):
            self.direction = (0, 1)

    def dir_left(self):
        if self.direction != (1, 0):
            self.direction = (-1, 0)

    def dir_right(self):
        if self.direction != (-1, 0):
            self.direction = (1, 0)


    def update_game(self):
        """更新游戏逻辑"""
        if self.game_over:
            return

        # 计算新蛇头位置
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # 碰撞检测
        if (
            new_head in self.snake
            or new_head[0] < 0
            or new_head[0] >= SCREEN_WIDTH // CELL_SIZE
            or new_head[1] < 0
            or new_head[1] >= SCREEN_HEIGHT // CELL_SIZE
        ):
            self.game_over = True
            return

        # 移动蛇身
        self.snake.insert(0, new_head)

        # 吃食物检测
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def draw_elements(self):
        """绘制游戏元素"""
        # 游戏结束显示
        if self.game_over:
            brain.screen.set_font(FontType.MONO40)
            brain.screen.set_pen_color(COLOR_TEXT)
            brain.screen.set_fill_color(COLOR_BG)
            brain.screen.print_at(
                "Game Over!",
                x=SCREEN_WIDTH // 2 - 140 + 40,
                y=SCREEN_HEIGHT // 2 - 15,
            )
            brain.screen.print_at(
                "Press A to restart",
                x=SCREEN_WIDTH // 2 - 140 - 40,
                y=SCREEN_HEIGHT // 2 - 15 + 40,
            )
            return

        # 绘制分数
        brain.screen.set_font(FontType.MONO12)
        brain.screen.set_pen_color(COLOR_TEXT)
        brain.screen.set_fill_color(COLOR_BG)
        brain.screen.print_at("Score:%d" % (self.score), x=1, y=12)

        # 绘制蛇身
        for segment in self.snake:
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE
            if segment == self.snake[-1]:
                col = COLOR_BG
            else:
                col = COLOR_SNAKE
            brain.screen.set_pen_color(col)
            brain.screen.set_fill_color(col)
            brain.screen.draw_rectangle(x, y, CELL_SIZE - 1, CELL_SIZE - 1)

        # 绘制食物
        food_x = self.food[0] * CELL_SIZE
        food_y = self.food[1] * CELL_SIZE
        brain.screen.set_pen_color(COLOR_FOOD)
        brain.screen.set_fill_color(COLOR_FOOD)
        brain.screen.draw_rectangle(food_x, food_y, CELL_SIZE - 1, CELL_SIZE - 1)

    def run(self):
        """主游戏循环"""
        running = True
        while running:
            if controller.buttonA.pressing() and self.game_over:
                self.reset_game()

            self.update_game()
            self.draw_elements()
            wait(self.loop_time, MSEC)


game = Game()
game.run()
