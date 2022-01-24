#coding=utf-8
import operator
from tkinter.tix import Tree
from numpy import float64
import pandas as pd
import math
from random import random





class clean_data:
    clean_source=pd.DataFrame()
    def __init__(self,dataframe):
        self.clean_source=dataframe
    def export_result(self):
        pass


class raw_data:
    class_info = 0.0  #類別訊息獲取量
    attributes = {}  #建字典對到 effect attribute
    conclusions = [] #結論
    raw_source=pd.DataFrame()
    class_info=0.0  #類別訊息獲取量
    attributes={}  #建字典對到 effect attribute
    primary_key=[] #唯一分辨的key
    clean_subsets=[] #其他的clean subset 裡面存 clean_data class
    unclean_subsets=[]  #其他的unclean subset 裡面存raw_data class
    '''
    attributes['天氣']=effect_attribute('天氣')
    '''
    
    #建構子
    def __init__(self,file_path=None,dataframe=None,primary_key=None):
        '''
        先判定是否需要讀csv,若不用就直接用現有dataframe建立
        之後就先建立attri字典
        
        
        '''
        self.raw_source=dataframe
        self.primary_key.append(primary_key)
        self.fake_read_in_attributes(file_path=file_path) #先建立attri字典
        self.sort_attri_order() #排序gainA
        self.reorder_raw_source() #依照attribute的gainA去重新排列data
        self.extract_to_subsets()  #分離clean與unclean資料
        # self.export_result()    #地回地回
        
    #遞迴的部分
    def export_result(self):
        if(len(self.unclean_subsets)!=0):
            for unclean_subset in self.unclean_subsets:
                unclean_subset.export_result()
        else:
            for clean_subset in self.clean_subsets:
                clean_subset.export_result()
    
    #把東西丟到subset裡
    def extract_to_subsets(self):
        temp_dict_to_check={}
        temp_dict_to_cast={}
        temp_dict_series_dataframe_clean={}
        temp_dict_series_dataframe_unclean={}

        for index,row in self.raw_source.iterrows(): #先檢查
            if(row[0] not in temp_dict_to_check):#第一次被讀到
                temp_dict_to_check[row[0]]=True #True 代表是clean data, False代表是 unclean data
                temp_dict_to_cast[row[0]]=row[-1]
                continue
            if(row[-1]!=temp_dict_to_cast[row[0]]):#不等於
                temp_dict_to_check[row[0]]=False
        for index,row in self.raw_source.iterrows(): #分類
            if(temp_dict_to_check[row[0]]): #clean data 丟到clean data
                if(row[0] not in temp_dict_series_dataframe_clean):
                    temp_dict_series_dataframe_clean[row[0]]=row.to_frame(0).T
                else:
                    temp_dict_series_dataframe_clean[row[0]]=temp_dict_series_dataframe_clean[row[0]].append(row.to_frame(0).T,ignore_index=True)
            else: #unclean data 把unclean丟到unclean data
                if(row[0] not in temp_dict_series_dataframe_unclean):
                    temp_dict_series_dataframe_unclean[row[0]]=row.to_frame(0).T
                else:
                    temp_dict_series_dataframe_unclean[row[0]]=temp_dict_series_dataframe_unclean[row[0]].append(row.to_frame(0).T,ignore_index=True)
        '''
        下面是可以用來測試,分別看現在乾淨資料與不乾淨資料
        print('乾淨')
        for clean in temp_dict_series_dataframe_clean.values():
            print(clean)        
        print('不乾淨')
        for unclean in temp_dict_series_dataframe_unclean.values():
            print(unclean)        
        '''
        print('乾淨')
        for clean in temp_dict_series_dataframe_clean.values():
            print(clean)        
        print('不乾淨')
        for unclean in temp_dict_series_dataframe_unclean.values():
            print(unclean)        
        
        # for clean in temp_dict_series_dataframe_clean.values(): #匯出clean data
        #     self.clean_subsets.append(clean_data(clean))
        # for unclean in temp_dict_series_dataframe_unclean.values(): #匯出unclean data,記得刪除第一航並加primary key
        #     self.unclean_subsets.append(raw_data(dataframe=unclean.drop(columns=unclean.columns[0]),primary_key=unclean.columns[0]))
        
            
                
        pass
    
    #排序gainA
    def sort_attri_order(self):
        self.attributes=dict(sorted(self.attributes.items(), key=lambda item: item[1].gainA,reverse=True)) #照gainA升冪排序
        # for k,v in self.attributes.items(): #看gainA
        #     print(k,v.gainA)
    def reorder_raw_source(self):
        newOrder=list(self.attributes.keys())
        newOrder.append(self.raw_source.columns[-1]) #加上結論
        self.raw_source=self.raw_source[newOrder]
        self.raw_source=self.raw_source.sort_values(self.raw_source.columns[0],ascending=True)
        print('印reorder後的\n',self.raw_source.head(15)) #印reorder後的
    
    
    #測試用
    def fake_read_in_attributes(self,file_path=None):
        if(file_path!=None):    #要讀csv
            self.raw_source=pd.read_csv(file_path)
        #不用讀csv
        for col in self.raw_source.columns[:-1]: #結論不用讀
            self.attributes[col]=effect_attribute(name=col,con=list(),gainA=0)
        print('印reorder前的\n',self.raw_source.head()) #印reorder前的

    
    def read_in_csv(): #讀csv順便把attributes字典建立，記得用pandas讀csv
        df = pd.read_csv("./觀測天氣之資料表.csv") #讀檔

        con = df['結論'].sort_values()
        data_sum = con.count() #資料總數
        con_type = con.T.drop_duplicates() #結論有哪幾種
        for result in con_type: #把結論存起來
            raw_data.conclusions.append(result)
        con_type_num = len(raw_data.conclusions)
# 計算class_info
        for count in range(0,con_type_num):
            upper = con.value_counts()[count]
            raw_data.class_info -= (upper/data_sum)*math.log2(upper/data_sum)
        
        for col in df.columns: #取得全部屬性
            if col != "結論":
                raw_data.attributes[col] = effect_attribute(name = col, con = raw_data.conclusions, gainA = raw_data.class_info)

        print(raw_data.class_info) #印出類別資訊量for check check!
        return df, raw_data.attributes #回傳csv資料

#公式 >>> [-= type/all(log2(type/all))]
    
class effect_attribute:
    effect_attr_name = ""    #屬性名稱
    attr_info = 0.0  #屬性訊息量
    gainA = 0.0   #屬性訊息獲取量
    conclusions = []   #結論
    attr_subset = {}  #屬性對應結論
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
    def __init__(self, name, con, gainA):
        self.effect_attr_name = name
        self.conclusions = con
        self.gainA = gainA
        
    def caculate_attr(self, data):
        
        data_sum = len(data) #資料總筆數
        attr_data = data[self.effect_attr_name] #屬性資料
        data_type = attr_data.drop_duplicates() #取得屬性資料的種類
        attr_con = data.value_counts() #屬性+結論的個別總數
        
        data_type_num = data[self.effect_attr_name].value_counts() #屬性資料的個別總數 （有 9 無 0)
        
#這裡看起來會出大事>>>>就如果說 屬性資料用一樣的敘述好像會蓋掉資料ㄇ 還是其實沒啥差<<他反正我現在看起來是存在同一個dic裡面啦@_@
        for type in data_type: #初始化屬性結論
            temp_info = 0.0
            data_upper = data_type_num[type]
            con = self.conclusions
            #先假設只有兩ㄍ結論我之後再改QQ
            type_con0 = attr_con[type].get(con[0]) #該屬性的性質的結論結果
            type_con1 = attr_con[type].get(con[1])

            #修正無資料ㄉ東東
            if type_con0 == None:
                type_con0 = 0
            if type_con1 == None:
                type_con1 = 0

            type_sum = type_con0 + type_con1 #之後改之後改

            self.attr_subset[type] = [type_con0,type_con1]
            for result in self.attr_subset[type]:
                if result == 0:
                    break
                else:
                    temp_info -= (result/type_sum)*math.log2(result/type_sum)
            self.attr_info += (data_upper/data_sum)*temp_info

        # print(self.attr_subset)
        print(self.effect_attr_name)
        return self.attr_info

def main():
    # test=raw_data(file_path="D:/NUK/建新RA/NUK_James_RA/觀測天氣之資料表.csv") pan
    
    csv_df, attr = raw_data.read_in_csv()
    for sub_attr in raw_data.attributes:
        arrange_sub_attr_data = csv_df[[sub_attr, '結論']].sort_values(by = '結論').sort_values(by = sub_attr) #排序過後的資料 > 只取該屬性跟結論
        print(attr[sub_attr].caculate_attr(arrange_sub_attr_data))
        # print(arrange_sub_attr_data)
    # print(csv_df)
    pass


if __name__ == "__main__":
    main()