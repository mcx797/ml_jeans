############################################################
#            get the data of the picture and               #
#            try to get some kind of sort                  #
#            and finally get some rank                     #
############################################################

import pandas as pd
import csv
import PIL.Image as Image
import os
import sys

#getweight函数用于计算每张图片用于排序的权值，可以通过修改getweight函数调参。
#proportion代表白色部分占比，R, G, B则为三种颜色归一化（/255）后的值。这里直接相加，感觉用（R, G, B）到（1，1，1）的距离会更加合适？
def getweight(Proportion, R, G, B):
    return  Proportion + 3 * (R + G + B)

savedirectory = "./result1/"

#get all of the label
'''
data = []
data1 = pd.read_csv("prevent.csv")
print(data1)

'''
with open("prevent.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        data.append(line)
data.pop(0)
Len = len(data)
#得到所有的数据并将数据保存到data，第一行是label,所以用pop删除掉


for i in range(Len):
    data[i][0] = float(data[i][0])
    data[i][1] = (int(data[i][1]) - 1)/256
    data[i][2] = (int(data[i][2]) - 1)/256
    data[i][3] = (int(data[i][3]) - 1)/256 
#归一化处理
print(data)

#save all the picture
images = []
for i in range(len(data)):
    img = Image.open("./preventB/" + str(i) + ".jpg")
    images.append(img)

number = 0
Out = open("result1.csv", "wt")
sys.stdout = Out
print("Proportion, R, G, B, weight, label")
for i in range(Len):
    num = 0
    label = -1
    for j in range(Len):
        num1 = getweight(data[j][0], data[j][1], data[j][2], data[j][3])  
        if(num1 > num):
            num = num1
            label = j
    print(str(data[label][0]) + ", " + str(data[label][1]) + ", " + str(data[label][2]) + ", " + str(data[label][3]) + ", " + str(num1) + ", " + str(label))
    images[label].save(savedirectory + str(number) + ".jpg")
    number += 1
    data[label][0] = data[label][1] = data[label][2] = data[label][3] = 0 
    #不断找到值最大的那个图片，将图片输出，并将该图片对应的所有数据记为0
