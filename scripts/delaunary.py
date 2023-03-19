import random
import numpy as np
from scipy.spatial import Delaunay
from matplotlib import pyplot as plt
from PIL import Image


def onclick(event):
    if event.button == 1:
        # クリックした座標を取得
        x, y = event.xdata, event.ydata
        print("Clicked at:", x, y)

        # 新しいポイントを追加
        global points
        if len(points) == 0:
            points.append([x, y])
            points = np.array(points)
        else:
            points = np.vstack([points, [x, y]])
            print(points)
        if len(points)>2:
        
            # Delaunay三角形化を行う
            global tri
            tri = Delaunay(points)

            # 図を再描画
            ax.clear()
            ax.triplot(points[:, 0], points[:, 1], tri.simplices)
            ax.plot(points[:, 0], points[:, 1], 'o')
            ax.set_xlim([voronoi_xmin, voronoi_xmax])
            ax.set_ylim([voronoi_ymin, voronoi_ymax])
            plt.gca().invert_yaxis()
            plt.draw()


# PNGファイルを読み込んでピクセルデータを取得する
image = Image.open("sh.png")
pixels = image.load()
width, height = image.size

# Voronoi図の領域をPNGファイルの幅と高さにする
voronoi_xmin, voronoi_ymin = 0, 0
voronoi_xmax, voronoi_ymax = width, height

# ランダムに4つの点を選ぶ
points = []

# 図を作成する
fig, ax = plt.subplots()
ax.imshow(image)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

# 図を表示する
plt.show(block=True)