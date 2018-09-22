import numpy as np
import pylab as pl
import sys

sys.argv.append('pca_output.vec')
f = open(sys.argv[1], 'r', encoding='UTF-8')
C = list()
for line in f:
    args = line.split(' ')
    point = (float(args[1]), float(args[2]))
    C.append(point)


def draw(C):
    colValue = ['r', 'y', 'g', 'b', 'c', 'k', 'm']
    coo_X = []  # x坐标列表
    coo_Y = []  # y坐标列表
    for j in range(len(C)):
        coo_X.append(C[j][0])
        coo_Y.append(C[j][1])
    pl.scatter(coo_X, coo_Y, marker='x',
               color=colValue[0])

    pl.legend(loc='upper right')
    pl.show()


draw(C)
