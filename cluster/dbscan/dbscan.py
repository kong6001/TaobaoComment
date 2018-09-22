# -*- coding:utf-8 -*-

import math
import numpy as np
import pylab as pl
from sklearn.decomposition import PCA
import os

file = open('pca_output.vec', encoding='UTF-8')
lines = file.readlines()
file.close()

dataset = set()
dic = dict()
for item in lines:
    data = item.replace(' \n', '')
    data = data.replace('\n', '')
    data = data.split(' ')
    if len(data) < 3:
        continue

    tup = tuple(data[1:])
    dic[tup] = data[0]
    dataset.add(tup)


# 计算欧几里得距离,a,b分别为两个元组
def dist(a, b):
    dim = max(len(a), len(b))
    distance = 0
    for i in range(0, dim):
        distance += math.pow(float(a[i]) - float(b[i]), 2)
    return math.sqrt(distance)


# 算法模型
def DBSCAN(D, e, Minpts):
    # 初始化核心对象集合T,聚类个数k,聚类集合C, 未访问集合P,
    T = set()
    k = 0
    C = []
    P = set(D)
    for d in D:
        if len([i for i in D if dist(d, i) <= e]) >= Minpts:
            T.add(d)
    # 开始聚类
    while len(T):
        P_old = P
        o = list(T)[np.random.randint(0, len(T))]
        P = P - set(o)
        Q = []
        Q.append(o)
        while len(Q):
            q = Q[0]
            Nq = [i for i in D if dist(q, i) <= e]
            if len(Nq) >= Minpts:
                S = P & set(Nq)
                Q += (list(S))
                P = P - S
            Q.remove(q)
        k += 1
        Ck = list(P_old - P)
        T = T - set(Ck)
        C.append(Ck)
    return C


# 画图
def draw(C):
    colValue = ['r', 'y', 'g', 'b', 'c', 'k', 'm']
    for i in range(len(C)):
        coo_X = []  # x坐标列表
        coo_Y = []  # y坐标列表
        for j in range(len(C[i])):
            coo_X.append(float(C[i][j][0]))
            coo_Y.append(float(C[i][j][1]))
        pl.scatter(coo_X, coo_Y, marker='x',
                   color=colValue[i % len(colValue)], label=i)

    pl.legend(loc='upper right')
    pl.show()


e = 0.0025
Minpts = 3
C = DBSCAN(dataset, e, Minpts)

path = str(e) + str(Minpts)
if not os.path.exists(path):
    os.mkdir(path)

for i in range(0, len(C)):
    f = open(path+'/output' +
             str(i) + '.txt', 'w', encoding='UTF-8')
    for item in C[i]:
        f.write(dic[item] + '\n')
    f.close()

draw(C)
