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



a="fsdf"
b= "fasdfsadfsdaf"
blank=" "
for i in range(30-len(a)):
    blank+=" "

print(a+blank+'{1}')
blank=" "
for i in range(30-len(b)):
    blank+=" "

print(b+blank+'{1}')
