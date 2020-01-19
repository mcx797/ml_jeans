# -*- coding: utf-8 -*-
# 使用 K-means 对图像进行聚类，并显示聚类压缩后的图像
import numpy as np
import PIL.Image as image
import sys
from sklearn.cluster import KMeans
from sklearn import preprocessing
import matplotlib.image as mpimg
import os
# 加载图像，并对数据进行规范化
def load_data(filePath):
    # 读文件
    f = open(filePath,'rb')
    data = []
    # 得到图像的像素值
    img = image.open(f)
    # 得到图像尺寸
    width, height = img.size
    for x in range(width):
        for y in range(height):
            # 得到点 (x,y) 的三个通道值
            c1, c2, c3 = img.getpixel((x, y))
            data.append([(c1+1)/256.0, (c2+1)/256.0, (c3+1)/256.0])
    f.close()
    return np.mat(data), width, height, data, img

def kmeans(Path, num):
    # 加载图像，得到规范化的结果 imgData，以及图像尺寸
    img, width, height, data, img1 = load_data(Path)
    # 用 K-Means 对图像进行 16 聚类
    kmeans =KMeans(n_clusters=2)
    label = kmeans.fit_predict(img)
    # 将图像聚类结果，转化成图像尺寸的矩阵
    label = label.reshape([width, height])
    sum1 = 0
    sum2 = 0
    sum3 = 0
    for x in range(width * height):
        sum1 += data[x][0]
        sum2 += data[x][1]
        sum3 += data[x][2]
    sum1 = sum1 / (width * height)
    sum2 = sum2 / (width * height)
    sum3 = sum3 / (width * height)
    sum1 = int(sum1 * 256) - 1
    sum2 = int(sum2 * 256) - 1
    sum3 = int(sum3 * 256) - 1
    # 创建个新图像 img，用来保存图像聚类压缩后的结果
    img=image.new('RGB', (width, height))
    sum = 0
    max = kmeans.cluster_centers_[label[0, 0], 0] + kmeans.cluster_centers_[label[0, 0], 1] + kmeans.cluster_centers_[label[0, 0], 2]
    isss = 0
    for x in range(width):
        for y in range(height):
            c1 = kmeans.cluster_centers_[label[x, y], 0]
            c2 = kmeans.cluster_centers_[label[x, y], 1]
            c3 = kmeans.cluster_centers_[label[x, y], 2]
            if (c1 + c2 + c3 > max):
                max = c1 + c2 + c3
                isss = 1
                break
            elif(c1 + c2 + c3 < max):
                isss = 1
                break
        if (isss == 1):
            break
    for x in range(width):
        for y in range(height):
            c1 = kmeans.cluster_centers_[label[x, y], 0]
            c2 = kmeans.cluster_centers_[label[x, y], 1]
            c3 = kmeans.cluster_centers_[label[x, y], 2]
            if (c1 + c2 + c3 == max):
                sum += 1
            img.putpixel((x, y), (int(c1*256)-1, int(c2*256)-1, int(c3*256)-1))
    img.save('./kmeansPic1/' + str(num) + '.jpg')
    img1.save('./kmeansPic2/' + str(num) + '.jpg')
    num += 1
    return num, sum / (width * height), sum1, sum2, sum3


directory = "./PreventPic/"
num = 0
result = []
Out = open("prevent.csv", "wt")
sys.stdout = Out
print("Proportion, R, G, B")
for imgname in os.listdir(directory):
    #print(imgname)
    num, resulti, sum1, sum2, sum3 = kmeans(directory + imgname, num)
    print(str(resulti) + ", " + str(sum1) + ", " + str(sum2) + ", " + str(sum3))