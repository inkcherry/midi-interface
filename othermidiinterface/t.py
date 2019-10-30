# a="fsdf"
# b= "fasdfsadfsdaf"
# blank=30
# print(a,end='')
# for i in range(blank-len(a)):
#     print(" ",end='')
# print("3")
# print(b,end='')
# for i in range(blank-len(b)):
#     print(" ",end='')
# print("3")
#


#1
# a="fsdf"
# b= "fasdfsadfsdaf"
# blank=" "
# for i in range(30-len(a)):
#     blank+=" "
#
# print(a+blank+'{1}')
# blank=" "
# for i in range(30-len(b)):
#     blank+=" "
#
# print(b+blank+'{1}')



#2
# class a:
#     def __init__(self,t):
#         self.num=t
#         return
#     def printnum(self):
#         print(self.num)
# aass = []
#
# for i in range(3):
#     aass.append(a(i))
#
# # print(aass)
# print(len(aass))
# for key in aass:
#     print(step)
#     # key.printnum()
#     print(key.num)

#3
import numpy as np

a=np.array([[2,3],[4,5]])
b=np.array([[6,7],[8,9]])
c=np.array([[10,11],[11,12]])


t=a.reshape(1,a.shape[0],a.shape[1])
m=b.reshape(1,b.shape[0],b.shape[1])

print(t.shape)

print(m.shape)

w=np.concatenate((t,m),axis=0)
print(w)
print(w.shape)

T=np.concatenate((w,t),axis=0)
print(T.shape)
# print(a)

# c=np.zeros([a.shape[0],a.shape[1]])

# def merge(a,b):
#     a= a.reshape(1,a.shape[0],a.sha)

# c=np.array(a.shape[0],a.shape[1])

# c=np.append(c,a)
# c=np.append(c,b)
# d=c.reshape(3,2,2)
#
#
# print(d)