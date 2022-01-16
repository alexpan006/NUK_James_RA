#coding=utf-8
import pandas as pd

df=pd.read_csv("./觀測天氣之資料表.csv")
df=df.sort_values("天氣",ascending=True)
print(df.head())



class raw_data:
    class_info=0.0  #類別訊息獲取量
    attributes={}  #建字典對到 effect attribute
    conclusions=[] #結論
    
    '''
    attributes['晴朗']=effect_attribute('晴朗')
    '''
    def read_in_csv(): #讀csv順便把attributes字典建立，記得用pandas讀csv
        pass
    
    

class effect_attribute:
    effect_attr_name=""    #屬性名稱
    attr_info=0.0  #屬性訊息量
    gainA=0.0   #屬性訊息獲取量
    conclusions=[]   #結論
    attr_subset={}  #屬性對應結論
    '''
    attr_subset={}
    conclusions=["不好","好"]

    ====>晴朗,炎熱,高,無,不好
    讀一行原始資料，讀到一個結論(當作 a="不好")

    for one_conclusion in conclusions:
        if(a == one_conclusion):
            attr_subset[ one_conclusion ] += 1
        else:
            pass

    attr_subset=>
    {"晴朗" : [2,0],
    "陰天" : [1,1],
    "雨天" : [0,2]}

    '''
    def __init__(self,name):
        self.effect_attr_name=name
        pass