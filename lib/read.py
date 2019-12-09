import numpy as np
import tensorflow as tf

#
# dataset=np.zeros([100,1],dtype=int)
# for i in range(100):
#     dataset[i][0]=i
# print(dataset)

dataset=np.load("dataset.npy")
print(dataset.shape)
data=tf.data.Dataset.from_tensor_slices((dataset))
data=data.shuffle(20).repeat(1).batch(1)
k=data.take(5)
it=iter(data.take(5))
# it=iter(data)
# print(len(data))



count=0



# while True:
#     try:
#         # 获得下一个值:
#         x = next(it)
#         y = tf.keras.utils.to_categorical(x,num_classes=85)
#         print(x.shape)
#         print(y.shape)
#         print(x)
#         print(y[0])
#         break
#         count+=1
#         # print(x)
#         # print(x.shape)
#     except StopIteration:
#         # 遇到StopIteration就退出循环
#         break


print(count)



