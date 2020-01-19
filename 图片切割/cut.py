######################################################################
#                   cut.py用于将一张输入的图片切割为                   #
#                   所需要的尺寸，并将图片输出到文件夹                 #
#                   最终图片命名从1.jpg到n.jpg                        #
#####################################################################
from PIL import Image
img = Image.open("./699+7.5g+20170721A.jpg")
#将图片里的字符串更改为需要的文件名即可，这里给的是相对路径，实际路径也可以。
a = img.size
width = a[0]
height = a[1]
#得到原图的尺寸
rx = 64
ry = 64
#rx, ry代表希望将图片分割为 rx * ry 的图片
x = width // rx
y = height // ry
print("x is " + str(x))
print("y is " + str(y))
#x:横向切割的数量
#y:纵向切割的数量
num = 0
#num用来记录图片数量，用来给图片从小到大命名
for i in range(x):
    for j in range(y):
        left = i * rx
        bottom = j * ry
        #得到切割图像的基位置
        cropped = img.crop((left, bottom, left + rx, bottom + ry))
        cropped.save("./64_64/" + str(num) + ".jpg")
        #切割并保存图片
        num += 1
        #图片数+1
