import pygame
import random
import math
from pygame.locals import *

# 初始化Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 颜色配置（德国包豪斯风格冷色调）
COLORS = [
    (8, 76, 97),  # 深海蓝
    (18, 147, 145),  # 青金石
    (238, 238, 238),  # 机械白
    (45, 64, 89),  # 钢灰
    (127, 199, 175)  # 氧化绿
]


class BioOrganism:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(20, 60)
        self.color = random.choice(COLORS)
        self.speed = random.uniform(0.5, 2.0)
        self.angle = random.uniform(0, 2 * math.pi)
        self.geometry_type = random.choice(["polygon", "spiral", "crystal"])
        self.lifespan = 600  # 自动消失时间

    def update(self):
        # 机械流体运动算法
        self.angle += random.uniform(-0.05, 0.05)
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifespan -= 1

        # 边界反弹
        if self.x < 0 or self.x > WIDTH: self.angle = math.pi - self.angle
        if self.y < 0 or self.y > HEIGHT: self.angle = -self.angle

    def draw(self):
        # 生成包豪斯风格几何图形
        if self.geometry_type == "polygon":
            points = []
            sides = random.randint(5, 8)
            for i in range(sides):
                radius = self.size * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 500 + i))
                px = self.x + radius * math.cos(2 * math.pi * i / sides)
                py = self.y + radius * math.sin(2 * math.pi * i / sides)
                points.append((px, py))
            pygame.draw.polygon(screen, self.color, points, 2)

        elif self.geometry_type == "spiral":
            for i in range(1, 6):
                radius = i * self.size / 5
                pygame.draw.arc(screen, self.color,
                                (self.x - radius, self.y - radius, 2 * radius, 2 * radius),
                                pygame.time.get_ticks() / 1000, pygame.time.get_ticks() / 1000 + math.pi / 2,
                                2)

        elif self.geometry_type == "crystal":
            for j in range(3):
                angle = pygame.time.get_ticks() / 1000 + j * math.pi / 3
                length = self.size * (0.8 + 0.2 * math.sin(pygame.time.get_ticks() / 300))
                end_x = self.x + length * math.cos(angle)
                end_y = self.y + length * math.sin(angle)
                pygame.draw.line(screen, self.color, (self.x, self.y), (end_x, end_y), 3)


# 生物管理器
class BioManager:
    def __init__(self):
        self.organisms = []

    def create_new(self, x, y):
        self.organisms.append(BioOrganism(x, y))

    def remove_oldest(self):
        if self.organisms:
            self.organisms.pop(0)

    def update_all(self):
        for org in self.organisms[:]:
            org.update()
            if org.lifespan <= 0:
                self.organisms.remove(org)

    def draw_all(self):
        for org in self.organisms:
            org.draw()


# 主程序循环
manager = BioManager()
running = True

while running:
    screen.fill((15, 25, 35))  # 深海背景色

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键创建
                manager.create_new(*event.pos)
            elif event.button == 3:  # 右键删除最旧
                manager.remove_oldest()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:  # 空格清空
                manager.organisms.clear()

    manager.update_all()
    manager.draw_all()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
