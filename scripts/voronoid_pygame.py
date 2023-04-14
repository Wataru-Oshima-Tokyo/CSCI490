# import pygame
# import random

# # Pygame初期化
# pygame.init()
# screen = pygame.display.set_mode((400, 400))

# # 入力点の集合を生成する
# points = [(random.randint(0, 400), random.randint(0, 400)) for i in range(15)]

# # 画面を塗りつぶす
# screen.fill((255, 255, 255))

# # 入力点を描画する
# for point in points:
#     pygame.draw.circle(screen, (0, 0, 0), point, 2)

# # # Voronoi図を描画する
# for x in range(400):
#     for y in range(400):
#         closest_distance = float("inf")
#         closest_point = None
#         for point in points:
#             distance = (x - point[0]) ** 2 + (y - point[1]) ** 2
#             if distance < closest_distance:
#                 closest_distance = distance
#                 closest_point = point
#         pygame.draw.circle(screen, (255, 0, 0), closest_point, 1)

# # 画面を更新する
# pygame.display.update()

# # イベントループ
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

# # Pygameの終了
# pygame.quit()


import numpy as np
import pygame
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi,voronoi_plot_2d

# Pygame初期化
pygame.init()
screen = pygame.display.set_mode((400, 400))

# 入力点の集合
points = np.random.rand(15, 2) * 400

# Voronoi図を計算する
vor = Voronoi(points)

# Voronoi図を描画する
for region in vor.regions:
    if not -1 in region:
        vertices = [vor.vertices[i] for i in region]
        vertices = [(int(x), int(y)) for x, y in vertices]
        print(vertices)
        if len(vertices) != 0:
            pygame.draw.polygon(screen, (255, 255, 255), vertices)

# Pygameイベントループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    voronoi_plot_2d(vor)

    # プロットを表示する
    plt.show()

# Pygameの終了
pygame.quit()