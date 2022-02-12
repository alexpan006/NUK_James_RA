import math


# class a:
#     a_sum=0
#     name=''
#     def __init__(self,name):
#         self.name=name
#         # self.haha()
#     def pp(self):
#         print(self.name)
#     def haha(self):
#         self.a_sum=100
# print('1111',a('b').haha())
# lala=a("a")
# print(lala.a_sum)
# print('3333',a("test").a_sum) #100




def cal_i(a):
    print('在a李:',a)
    total_count=0
    for one in a:
        total_count+=one
    sum=0
    for one in a:
        if(one!=0):
            temp=(-one/total_count)*math.log2((one/total_count))
            print('temp=',temp)
            sum+=temp
    return sum
parent=0.9709505944546686
child=(2/5)*cal_i([0,2]) + (3/5)*cal_i([3,0]) 
print('child:',child)
print(parent - child  )

