import numpy as np
import re
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
import time
# PGM形式のファイルから地図を読み取る
def read_pgm(filename, byteorder='>'):
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    return np.frombuffer(buffer,
                         dtype='u1' if int(maxval) < 256 else byteorder+'u2',
                         count=int(width)*int(height),
                         offset=len(header)
                         ).reshape((int(height), int(width)))


    with open(filename, 'rb') as f:
        # ファイルヘッダーの読み飛ばし
        f.readline()
        # 画像サイズの読み込み
        size = f.readline().decode().split()
        print(size)
        width, height = int(size[0]), int(size[1])
        # 最大輝度値の読み込み
        max_val = int(f.readline().decode())
        # バイナリデータの読み込み
        data = np.fromfile(f, dtype=np.uint8).reshape(height, width)
    return data

# 地図を読み取る
original_map = read_pgm("map.pgm")
map = original_map.copy()
for row in map:
    for col in row:
        if col != 0:
            col= 0
# for row in map:
#     print(row)
# plt.plot(map)
# plt.show()

plt.imshow(map, cmap='gray')
plt.colorbar()
plt.show()
# 地図からインタレストポイントを抽出する
points = np.argwhere(map > 0)
print(points)
# # Voronoi図を計算する
vor = Voronoi(points)
print(vor)
# # Voronoi図を描画する
# plt.plot(points[:,0], points[:,1], '.')
# for simplex in vor.ridge_vertices:
#     if -1 not in simplex:
#         plt.plot(vor.vertices[simplex, 0], vor.vertices[simplex, 1], 'k-')

# plt.xlim(vor.min_bound[0] - 1, vor.max_bound[0] + 1)
# plt.ylim(vor.min_bound[1] - 1, vor.max_bound[1] + 1)
# plt.show()


