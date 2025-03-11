import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 屏幕设置
screen_width = 480
screen_height = 240
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("I love VEX 数字雨")

# 颜色定义
BLACK = (0, 0, 0)

# 字体设置
font_size = 20
font = pygame.font.SysFont('couriernew', font_size, bold=True)
char_width = font.size("I")[0]
char_height = font.size("I")[1]

# 列计算
columns = screen_width // char_width

# 显示文本
text = "I love VEX"
text_chars = list(text)
text_len = len(text_chars)

# 初始化列数据（每列存储多个字符串）
columns_data = [[] for _ in range(columns)]

# 控制帧率
clock = pygame.time.Clock()

def draw_text():
    # 生成新字符串（从屏幕顶部生成）
    for col in range(columns):
        if random.random() < 0.02:  # 控制生成频率
            new_string = {
                "start_y": -len(text_chars) * char_height,  # 初始在屏幕顶部上方
                "color": 255,
                "chars": text_chars.copy()
            }
            columns_data[col].append(new_string)

    # 更新并绘制字符串
    for col in range(columns):
        x = col * char_width
        new_strings = []
        
        for string in columns_data[col]:
            # 更新位置和颜色
            string["start_y"] += 3  # 下落速度
            string["color"] = max(string["color"] - 6, 0)
            
            # 只要字符串还有可见部分或颜色未消失就保留
            if string["color"] > 0 and string["start_y"] < screen_height:
                # 绘制所有字符
                for i, char in enumerate(string["chars"]):
                    y = string["start_y"] + i * char_height
                    # 只绘制屏幕内的字符
                    if -char_height < y < screen_height:
                        color = (0, string["color"], 0)
                        text_surface = font.render(char, True, color)
                        screen.blit(text_surface, (x, y))
                new_strings.append(string)
        
        columns_data[col] = new_strings

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)
    draw_text()
    pygame.display.update()
    clock.tick(30)