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




import json
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

ha={"1":1,"2":2}

print(type(json.dumps(ha)))