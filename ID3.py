#coding=utf-8
import operator
from tkinter.tix import Tree
import pandas as pd
import random

# df=pd.read_csv("./觀測天氣之資料表.csv")
# df=df.sort_values("天氣",ascending=True)
# test=df[['氣溫','天氣','濕度','風','結論']]
# print(df.head(15))


# hello


class clean_data:
    clean_source=pd.DataFrame()
    def __init__(self,dataframe):
        self.clean_source=dataframe
        pass


class raw_data:
    conclusions=[] #結論
    raw_source=pd.DataFrame()  #把csv讀成pandas的dataFrame 
    
    class_info=0.0  #類別訊息獲取量
    attributes={}  #建字典對到 effect attribute
    primary_key=[] #唯一分辨的key
    clean_subsets=[] #其他的clean subset 裡面存 clean_data class
    unclean_subsets=[]  #其他的unclean subset 裡面存raw_data class
    '''
    attributes['天氣']=effect_attribute('天氣')
    '''
    
    #建構子
    def __init__(self,file_path=None,dataframe=None):
        '''
        先判定是否需要讀csv,若不用就直接用現有dataframe建立
        之後就先建立attri字典
        
        
        '''
        self.raw_source=dataframe
        self.fake_read_in_attributes(file_path=file_path) #先建立attri字典
        self.sort_attri_order() #依照attribute的gainA去重新排列data
        self.reorder_raw_source()
        self.extract_to_subsets()
        pass
    #遞迴的部分
    def testf():
        if(len(unclean_subsets)!=0):
            for unclean_subset in unclean_subsets:
                unclean_subset.testf()
        else:
            for clean_subset in clean_subsets:
                clean_subset.export_result()
    
    #把東西丟到subset裡
    def extract_to_subsets(self):
        temp_dict_to_check={}
        temp_dict_to_cast={}
        temp_dict_series_dataframe={}
        for index,row in self.raw_source.iterrows(): #先檢查
            # print(row)
            print(pd.DataFrame(row))
            break

        for index,row in self.raw_source.iterrows(): #先檢查
            if(row[0] not in temp_dict_to_check):#第一次被讀到
                temp_dict_to_check[row[0]]=True
                temp_dict_to_cast[row[0]]=row[-1]
                continue
            if(row[-1]!=temp_dict_to_cast[row[0]]):#不等於
                temp_dict_to_check[row[0]]=False
        # for index,row in self.raw_source.iterrows(): #分類
        #     if(temp_dict_to_check[row[0]]): #clean data 丟到clean data
                
        #         pass
        #     else: #unclean data
        #         pass
        
                
            
            
                
        # print(self.raw_source[[self.raw_source.columns[0],self.raw_source.columns[-1]]].head(15))
        
        
        # self.subsets.append(raw_data())
        pass
    
    #排序gainA
    def sort_attri_order(self):
        self.attributes=dict(sorted(self.attributes.items(), key=lambda item: item[1].gainA,reverse=True)) #照gainA升冪排序
        for k,v in self.attributes.items():
            print(k,v.gainA)

    
    def reorder_raw_source(self):
        newOrder=list(self.attributes.keys())
        newOrder.append(self.raw_source.columns[-1]) #加上結論
        self.raw_source=self.raw_source[newOrder]
        self.raw_source=self.raw_source.sort_values(self.raw_source.columns[0],ascending=True)
        print('印reorder後的\n',self.raw_source.head(15)) #印reorder後的

        pass
    
    
    #測試用
    def fake_read_in_attributes(self,file_path=None):
        if(file_path!=None):    #要讀csv
            self.raw_source=pd.read_csv(file_path)
        #不用讀csv
        for col in self.raw_source.columns[:-1]: #結論不用讀
            self.attributes[col]=effect_attribute(col)
        print('印reorder前的\n',self.raw_source.head()) #印reorder前的

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
    {"晴朗" : [1,0],
    "陰天" : [1,1],
    "雨天" : [0,2]}

    '''
    def __init__(self,name):
        self.effect_attr_name=name
        self.fake_data()
    
    #測試用
    def fake_data(self):
        self.attr_info=random.random()
        self.gainA=random.random()
        
        
def main():
    test=raw_data(file_path="./觀測天氣之資料表.csv")
    pass

if __name__ == "__main__":
    # pass
    main()
