import cv2
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

# 地図画像を読み込む
map_image = cv2.imread('turtlebot.png')

# 画像を白黒反転し、地図上の障害物を白色、通行可能な領域を黒色にする
gray_map = cv2.cvtColor(map_image, cv2.COLOR_BGR2GRAY)
inverted_map = cv2.bitwise_not(gray_map)
(thresh, map_bw) = cv2.threshold(inverted_map, 127, 255, cv2.THRESH_BINARY)

# 黒色のピクセルの中心点を取得して、ポイントを生成する
points = []
for y in range(map_bw.shape[0]):
    for x in range(map_bw.shape[1]):
        if map_bw[y][x] == 0:
            points.append([x, y])

# Voronoiダイアグラムを生成する
vor = Voronoi(points)

# 各領域の半径を計算する
radii = []
for i, region in enumerate(vor.regions):
    if not region:
        radii.append(0)
    else:
        indices = region + [region[0]]
        vertices = vor.vertices[indices]
        center = vertices.mean(axis=0)
        distances = np.linalg.norm(vertices - center, axis=1)
        radii.append(distances.min())

# Voronoiダイアグラムをプロットする
fig = voronoi_plot_2d(vor)

# 各領域の半径をプロットする
for i, region in enumerate(vor.regions):
    if not region:
        continue
    if -1 in region:
        continue
    plt.annotate("{:.2f}".format(radii[i]), xy=vor.vertices[region].mean(axis=0),
                 horizontalalignment='center', verticalalignment='center')

# プロットを表示する
plt.savefig('voronoi.png')