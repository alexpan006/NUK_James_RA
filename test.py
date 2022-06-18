import math
import re
import csv
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
# def cal_i(a):
#     print('在a李:',a)
#     total_count=0
#     for one in a:
#         total_count+=one
#     sum=0
#     for one in a:
#         if(one!=0):
#             temp=(-one/total_count)*math.log2((one/total_count))
#             print('temp=',temp)
#             sum+=temp
#     return sum

# ha={"1":1,"2":2}

# print(type(json.dumps(ha)))




test=['安安','哈哈']
tempList=list(test)
tempList.append('123')
print(tempList)
print(test)



# ha=[ [1,2,3,4,5] , [6,7,8,9,10] ]
# la=[]


# with open('test.csv','w',encoding='utf-8-sig',newline='') as f:
#     writer=csv.writer(f)
#     writer.writerows(ha)
#     writer.writerows(la)