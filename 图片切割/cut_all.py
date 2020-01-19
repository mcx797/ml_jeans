#################################################################
#            cut_all.py将一个文件夹内的所有图片                   #
#            全部切割为需要尺寸的图片，并将所有                   #
#            图片按照0.jpg, 1.jpg, ...全部保存                   #
#            到目标文件夹                                        #
#################################################################
from PIL import Image as image
import os
import numpy as np

directory = "train/zeros/"
x_size = 64
y_size = 64
#directory为要切割的图片所在的地址，我这里是文件夹里专门存的图片，如果文件夹里有别的类型的文件不知道会不会出问题。
#x_size, y_size为最终要切割图片的横纵坐标
#除了这三个参数外，保存文件夹参数在cut函数内修改。

#load_data用于加载filepath下的文件并返回结果。
def load_data(filePath):
    # 读文件
    f = open(filePath,'rb')
    data = []
    # 得到图像的像素值
    img = image.open(f)
    # 得到图像尺寸
    width, height = img.size
    return img, width, height
# 加载图像，得到规范化的结果 imgData，以及图像尺寸




#cut用于将需要切割的每一张图片切割成 rx, ry图片并保存到相应的文件夹, num同样用来记录总图片数量和命名
def cut(img, width, height, rx, ry, num):
    #rx, ry代表希望将图片分割为 rx * ry 的图片
    x = width // rx
    y = height // ry
    for i in range(x):
        for j in range(y):
            left = i * rx
            bottom = j * ry
            cropped = img.crop((left, bottom, left + rx, bottom + ry))
            cropped.save("./train_64/zeros/" + str(num) + ".jpg")
            #我这里把图片保存在了"./train_64/zeros/"， 修改这个字符串修改保存地址。
            num += 1
    return num


num = 0
#num用来记录总图片数量和命名
for imgname in os.listdir(directory):
    img, width, height = load_data(directory + imgname)
    num = cut(img, width, height, x_size, y_size, num)
#遍历文件夹里所有的文件并切割，因为我没有对文件名进行判断就直接切割了，所以如果文件夹里有其他文件会出问题。
#可以对imgname加一个判断：
#if(".jgp" in directory)应该可以解决问题。但我没试过...  ~(^~^)~
