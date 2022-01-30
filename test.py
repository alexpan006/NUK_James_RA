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
    total_count=0
    for one in a:
        total_count+=one
    sum=0
    for one in a:
        if(one==0):
            continue
        temp=(-one/total_count)*math.log2((one/total_count))
        sum+=temp
    return sum
# print(cal_i([0,4]))

la=["1"]
ha={"1":12,"2":22,"3":33}

print( x for x in la if x not in ha)

for k in sorted(ha):
    print(k)

