import os
import warnings
import sys
from PIL import Image
import matplotlib.pylab as plt
import numpy as np
import random
warnings.filterwarnings('ignore')
from keras.utils import to_categorical

#数据预处理
directory_test_ones = "./test_64/ones/"
directory_test_zeros = "./test_64/zeros/"
directory_train_ones = "./train_64/ones/"
directory_train_zeros = "./train_64/zeros/"

test_image = []
test_label = []
train_image = []
train_label = []

Len = len(os.listdir(directory_test_ones))
#得到test集且label为1的图片个数。
for i in range(Len):
    img = Image.open(directory_test_ones + str(i) + ".jpg")
    arr = np.asarray(img, dtype = np.float32)
    test_image.append(arr)
    test_label.append(1)
#提取test集且label为1的所有图片，把图片信息转化为nparray数组并储存在test_image中， 把相应的label（结果为1）储存在test_label中

#与上方同理，将test_zeros里所有图片的信息储存。
Len = len(os.listdir(directory_test_zeros))
for i in range(Len):
    img = Image.open(directory_test_zeros + str(i) + ".jpg")
    arr = np.asarray(img, dtype = np.float32)
    test_image.append(arr)
    test_label.append(0)


#进行顺序的随机化处理，由于image， label需要有对应关系，先用zip合并，后再分离。
#（其实测试集貌似不需要进行随机处理？如果不随机处理的话，就可以直接根据out.csv的结果和图片进行对比处理了，感觉下面三行代码可以删掉）
test = list(zip(test_image, test_label))
random.shuffle(test)
test_image[:], test_label[:] = zip(*test)



test_image = np.asarray(test_image, dtype = np.float32)
#为了符合keras模型的输入数据要求，将test_img转化为test_image图片

test_image /= 255
#归一化处理


#处理train集的数据，和上面处理test集的数据完全相同。
Len = len(os.listdir(directory_train_ones))
for i in range(Len):
    img = Image.open(directory_train_ones + str(i) + ".jpg")
    arr = np.asarray(img, dtype = np.float32)
    train_image.append(arr)
    train_label.append(1)
Len = len(os.listdir(directory_train_zeros))
for i in range(Len):
    img = Image.open(directory_train_zeros + str(i) + ".jpg")
    arr = np.asarray(img, dtype = np.float32)
    train_image.append(arr)
    train_label.append(0)
train = list(zip(train_image, train_label))
random.shuffle(train)
train_image[:], train_label[:] = zip(*train)
train_image = np.asarray(train_image, dtype = np.float32)
train_image /= 255
train_label = to_categorical(train_label, 2)
#print(train_label)

'''
print(train_image.shape)
print(train_label.shape)
print(test_image.shape)
print(test_label.shape)
print(type(train_image))
print(train_image)
'''
#打印各种数组的形状，开始debug用的。


from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dropout, Dense
from keras.losses import categorical_crossentropy
from keras.optimizers import Adadelta
model = Sequential()#建立网络模型的框架
model.add(Conv2D(32, (5,5), activation='relu', input_shape=[64, 64, 3]))
#添加第一层2D层，第一层需要指定输入数据的input_shape, 这里由于是64 * 64尺寸的彩色图像，给入[64, 64, 3]
model.add(Conv2D(64, (5,5), activation='relu'))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))
#所有model.add均为添加卷积层。

model.compile(loss=categorical_crossentropy,
             optimizer=Adadelta(),
             metrics=['accuracy'])
#至此网络搭建完成，损失函数 loss直接用的keras的库函数。至此神经网络搭建完成（反正也都是掉包。。。）

batch_size = 64
epochs = 30
#网络的参数opochs为训练轮数，30轮这里的训练结果为85%准确率

model.fit(train_image, train_label,
         batch_size=batch_size,
         epochs=epochs)
#拟合训练的过程（这个分类实际上是吧分类问题转换为了回归问题。。。）

test_y = model.predict(test_image, batch_size = batch_size, verbose = 0, steps = None)
#根据模型预测（model可以把模型保存的，这里只是测试效果没有保存）



#输出结果到out.csv
savedStdout = sys.stdout
Out = open("out.csv", "wt")
sys.stdout = Out
#将python标准输出流替换为文件out.csv,后文print将内容输出到out.csv
print("id,label,read")
sum = 0
#sum为预测正确的数据个数
for i in range(700):
    if abs(test_y[i][1]) > abs(test_y[i][0]):
        ntemp = 1
    else:
        ntemp = 0
    #ntemp为预测的结果，因为这里是二分类，如果[0] > [1]认为结果为0， 否则认为结果为1
    print("%d,%d,%d" % (i, ntemp, test_label[i]))
    if(ntemp == test_label[i]):
        sum += 1
    #如果预测正确，则sum += 1
    #print(test_y[i])
Out = open("accuracy.txt", "wt")
sys.stdout = Out
print(sum / 700)
#将最终的测试集准确率输出到arruracy.txt.