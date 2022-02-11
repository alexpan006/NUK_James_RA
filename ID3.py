# -*- coding: utf-8 -*-
from email import policy
from operator import index
import re
from isort import file
import pandas as pd
import math
from random import random

'''
0209 -- CCC 各種暴力解orz
>RID解決完了
>中繼資料要去掉要能讀到-分析後.csv那個file_path line73-75那邊
>subset輸出解決了，但是出來之後有中括號跟引號，我暫時去不掉，寫在analyze-qui-stage2.py line42-47
'''

'''
2022.02.07--Pan 開工大吉
1.我在每一個class的建構子都加了重設所有參數的method,如果後來你有加新的class variable,
  記得要加到resest_all函示裡.
2.解決了之前怪怪ㄉ部分惹,現在要用遞迴的方式才能取出所有的priamry_keys了,拿gain也是用遞迴去
unclean_subsets裡面拿raw_data class 的東東.
3.阿你要用的部分就是:   
    (1)RID處理一下
    (2)中繼資料.csv看可不可以用掉
    (3)等建興說每個分離前的gainA要以啥樣子的csv匯出,你再用個ㄅㄟ

'''

'''
2022.01.25--Pan
1.read_in_csv那個函數要用self去拿class級別的variable,這樣才其他地方才吃的到
2.阿然後你先改read_in_csv好惹
3.clean data 可以用 raw_data().export_result()拿到所有的primary_key.你可以看一夏#遞迴的部分
  現在變成最一開始的raw_data裡面有所有的clean跟unclean資料,分別在clean_subsets跟unclean_subsets李
Noted:
-->然後我發現最好在建構子的地方都把會出錯的variable都clear一下,這樣好像才不會出事,我也不知為啥
-->上面那件事好像又有機會出事,我也不知道為啥
-->然後我有加一個三種結論ㄉcsv,你可以試試看      >> test過了基本上是對的我沒發現啥錯啦
-->阿png那個有分類的過程,attribute排序的部分我都是預設的,紅線部分是分出來clean,藍線分出來是unclean
-->阿你可以直接run,看個結果
'''
class attr_gaiaA():
    gainA_list = pd.DataFrame()

    def export(self, file_path):
        self.gainA_list.to_csv(file_path, mode = 'a',encoding='utf-8')
        self.gainA_list = pd.DataFrame() #reset


class clean_data:
    '''
    只記錄primary keys，然後會丟conclusion，用來算class distribution
    阿conclusion你在自己用ㄍ
    '''
    original_header=list()
    primary_keys=dict() #主key
    conclusions=list()  #結論
    support=0.0 #
    reliability=0.0
    class_distribution="" #ex: "4,0"
    simplicity=0.0
    deep=0.0
    clean_data=pd.DataFrame()
    result={} #最終輸出dict 藥用dict to 
    policy = pd.DataFrame()

    def __init__(self,primary_keys=None,clean_data=None,original_header=None,conclusions=None,support=None):
        self.reset_all()
        self.policy= pd.DataFrame()
        self.clean_data=pd.DataFrame()
        self.primary_keys=primary_keys #傳入primary key會是dict
        self.original_header=original_header
        self.clean_data=clean_data #是pd.DataFrame()
        self.conclusions=conclusions
        self.support=support #Support
        
        '''
        要去掉中繼資料ㄉ話這裡可以讀到-分析後.csv那個file_path就行ㄌ，直接弄掉就好
        '''    
        for col in pd.read_csv('中繼資料.csv',encoding='utf-8').columns: 
            self.policy[col] = [""]
    
    #Reset所有參數
    def reset_all(self):
        self.original_header=list()
        self.primary_keys=dict() #主key
        self.conclusions=list()  #結論
        self.support=0.0 #
        self.reliability=0.0
        self.class_distribution="" #ex: "4,0"
        self.simplicity=0.0
        self.deep=0.0
        self.clean_data=pd.DataFrame()
        self.result={} #最終輸出dict 藥用dict to 
        self.policy = pd.DataFrame()
        

    def cal_all(self,result_filepath):
        #處理最後輸出位置
        new_path=result_filepath.replace('.csv','-分析後.csv')
        
        self.deep=len(self.primary_keys)-1 #Deep
        self.simplicity=self.support/self.deep #Simplicity
        
        #處理class distribution的部分
        class_d=list()
        for one_conclusion in self.conclusions: #初始化class_d
            class_d.append(0)
        for index,v in self.clean_data.iterrows():
            temp_a=list()
            for one_conclusion in self.conclusions:
                if(one_conclusion == v[-1]):
                    temp_a.append(1)
                else:
                    temp_a.append(0)
            class_d=[a+b for a,b in zip(class_d,temp_a)]
        # print('class_d',class_d) #class_d [0, 4]
        self.class_distribution=",".join(list([str(class_d_str) for class_d_str in class_d]))
        
        
        self.reliability=self.support/sum(class_d)#Reliability的部分
        for k,v in self.primary_keys.items():
            self.result[k]=v
        
        # 全部加到 result dict李
        self.result["Deep"]=self.deep
        self.result["Support"]=self.support
        self.result["Reliability"]=self.reliability
        self.result["Class Distribution"]=self.class_distribution
        self.result["Simplicity"]=self.simplicity
        self.result["RID"] = len(pd.read_csv(new_path,encoding='utf-8')) + 1
        for key in self.result.keys():
            if key == '結論':
                self.policy['Class'] = self.result[key]
            else:
                self.policy[key] = self.result[key]
        
        self.policy.to_csv(new_path, mode = 'a', header = False, index = False,encoding='utf-8') #輸出用append的方式家道csv

        
    def export_result(self,result_filepath):
        #處理最後輸出位置
        new_path = result_filepath.replace('.csv','-分析後.csv')
        self.cal_all(result_filepath)

class raw_data:
    class_info = 0.0  #類別訊息獲取量
    conclusions = {} #結論 ex: {好:2,不好:5}
    conclusion_col = ""
    raw_source=pd.DataFrame()
    class_info=0.0  #類別訊息獲取量
    attributes={}  #建字典對到 effect attribute
    original_header=list()
    '''
    attributes['天氣']=effect_attribute('天氣')
    '''
    primary_keys=dict() #唯一分辨的key
    clean_subsets=[] #其他的clean subset 裡面存 clean_data class
    unclean_subsets=[]  #其他的unclean subset 裡面存raw_data class
    
    export_gainA = attr_gaiaA()
    #建構子
    def __init__(self,file_path=None,dataframe=None,primary_keys=None):
        '''
        先判定是否需要讀csv,若不用就直接用現有dataframe建立
        之後就先建立attri字典
        '''
        self.reset_all()
        #直接相等會讓primary_keys的型態變成None
        if(primary_keys!=None):
            self.primary_keys=primary_keys #傳入primary key會是dict
        self.load_data(file_path=file_path,data=dataframe)
        self.sort_attri_order() #排序gainA
        self.reorder_raw_source() #依照attribute的gainA去重新排列data
        self.extract_to_subsets()  #分離clean與unclean資料
        
    #Reset所有參數
    def reset_all(self):
        self.class_info = 0.0  #類別訊息獲取量
        self.conclusions = {} #結論 ex: {好:2,不好:5}
        self.conclusion_col = ""
        self.raw_source=pd.DataFrame()
        self.class_info=0.0  #類別訊息獲取量
        self.attributes={}  #建字典對到 effect attribute
        self.original_header=list()
        self.primary_keys=dict() #唯一分辨的key
        self.clean_subsets=[] #其他的clean subset 裡面存 clean_data class
        self.unclean_subsets=[]  #其他的unclean subset 裡面存raw_data class
        
    #遞迴的部分
    def export_result(self,result_filepath):
        print('乾淨節點數:',len(self.clean_subsets),"不乾淨節點數:",len(self.unclean_subsets))
        for unclean_subset in self.unclean_subsets:
            unclean_subset.export_result(result_filepath)
        for clean_subset in self.clean_subsets:
            clean_subset.export_result(result_filepath)
        result_filepath=result_filepath.replace('.csv','-分析後.csv')
        
        self.get_all_gainA(export_gainA = self.export_gainA)
        print('--------------------------')
        print(self.export_gainA.gainA_list)
        print('--------------------------')
        export_gainA_path = result_filepath.replace('-分析後.csv','-分析過程子集.csv')
        self.export_gainA.export(file_path = export_gainA_path)
        return result_filepath
    
    #分離unclean跟clean資料
    def extract_to_subsets(self):
        '''
        分離unclean跟clean資料
        '''
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
        
        if(len(temp_dict_series_dataframe_clean) != 0):
            for clean in dict(temp_dict_series_dataframe_clean).values():
                temp_primary_k_clean=dict(self.primary_keys)    #處理primary key
                temp_primary_k_clean[clean.columns[0]]=(clean[clean.columns[0]][0])
                temp_primary_k_clean[clean.columns[-1]]=(clean[clean.columns[-1]][0])
                self.clean_subsets.append(clean_data(primary_keys=temp_primary_k_clean,original_header=self.original_header,clean_data=clean,conclusions=list(self.conclusions.keys()),support=clean.shape[0]))
                
                    
        if(len(temp_dict_series_dataframe_unclean) != 0):
            for unclean in dict(temp_dict_series_dataframe_unclean).values(): #匯出unclean data,記得刪除第一航並加primary key(一個list)
                temp_primary_k_unclean=dict(self.primary_keys)  #處理primary key
                temp_primary_k_unclean[unclean.columns[0]]=(unclean[unclean.columns[0]][0])
                self.unclean_subsets.append(raw_data(file_path=None,dataframe=(unclean.drop(columns=unclean.columns[0])),primary_keys=temp_primary_k_unclean))
        
    #排序gainA
    def sort_attri_order(self):
        self.attributes=dict(sorted(self.attributes.items(), key=lambda item: item[1].gainA,reverse=True)) #照gainA升冪排序
        
    def reorder_raw_source(self):
        newOrder=list(self.attributes.keys())
        newOrder.append(self.raw_source.columns[-1]) #加上結論
        self.raw_source=self.raw_source[newOrder]
        self.raw_source=self.raw_source.sort_values(self.raw_source.columns[0],ascending=True)
    
    #載入df回傳effect_attributes
    def load_data(self, file_path = None, data = None):
        if file_path == None: #不用讀csv
            self.raw_source = data
        else:
            self.raw_source = pd.read_csv(file_path,encoding='utf-8') #讀檔
            policy = pd.DataFrame()
            # 設定clean_data的data
            # clean_data.data = self.raw_source
            # 初始化policy(export)的dataframe
            policy['RID'] = []
            for effect in self.raw_source.columns[:-1]:
                policy[effect] = []
            policy['Class'] = []
            policy['Deep'] = []
            policy['Support'] = []
            policy['Reliability'] = []
            policy['Class Distribution'] = []
            policy['Simplicity'] = []
            
            output_filename = file_path.replace('.csv','-分析後.csv')
            policy.to_csv(output_filename, index = False,encoding='utf-8')
            policy.to_csv('中繼資料.csv', index = False,encoding='utf-8')

        self.original_header=self.raw_source.columns
        self.s_col = self.raw_source.columns[-1] #直接這樣就好惹  記錄結論的欄位名
        counter=0 #用來算資料總數
        for index,one in self.raw_source[self.s_col].iteritems():
            if(one not in self.conclusions):
                self.conclusions[one]=1
            else:
                self.conclusions[one]+=1
            counter+=1
        data_sum=counter #資料總數
        # print(list(self.conclusions.values()))
        self.class_info=self.cal_i(list(self.conclusions.values())) #算類別訊息輛
        for col in self.raw_source.columns[:-1]:
            self.attributes[col]=effect_attribute(name=col,conclusion=list(self.conclusions.keys()),gainA=self.class_info,dataframe=self.raw_source[[col,self.raw_source.columns[-1]]])
        
    def cal_i(self,x):
        '''
        用來算 I( X , Y )
        x=[5,9],x是list 
        '''
        total_count=0
        for one in x:
            total_count+=one
        sum=0.0
        for one in x:
            if(one==0):
                continue
            temp=(-one/total_count)*math.log2((one/total_count))
            sum+=temp
        return sum
    def get_all_gainA(self, export_gainA):
        export_gainA.gainA_list['subset'] = []
        export_gainA.gainA_list['attributes'] = []
        export_gainA.gainA_list[''] = []
        export_gainA.gainA_list['GainA'] = []
        for unclean_subset in self.unclean_subsets:
            
            export_gainA.gainA_list = export_gainA.gainA_list.append({'subset':unclean_subset.primary_keys}, ignore_index = True)
            export_gainA.gainA_list = export_gainA.gainA_list.append({'attributes':'結論','':unclean_subset.class_info}, ignore_index = True)
            for attr in unclean_subset.attributes.values():
                export_gainA.gainA_list = export_gainA.gainA_list.append({'attributes':attr.effect_attr_name,'':attr.attr_info,'GainA':attr.gainA}, ignore_index = True)
                
    
class effect_attribute:
    con_num = 0 #存結論數量
    ss = []   #結論
    attr_subset = {}  #屬性對應結論
    parent_gainA = 0.0   #上層屬性訊息獲取量
    attr_info = 0.0  #屬性訊息量
    effect_attr_name = ""    #屬性名稱
    attr_data=pd.DataFrame() 
    gainA=0.0
    
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
    def __init__(self, name, conclusion, gainA, dataframe):
        
        self.attr_subset.clear() #0207
        
        self.reset_all() 
        
        
        self.effect_attr_name = name
        self.ss = conclusion
        self.parent_gainA = gainA
        self.con_num = len(conclusion)
        self.attr_data=dataframe

        self.caculate_attr()
    
    def reset_all(self):
        self.con_num = 0 #存結論數量
        self.ss = []   #結論
        self.attr_subset = {}  #屬性對應結論
        self.parent_gainA = 0.0   #上層屬性訊息獲取量
        self.attr_info = 0.0  #屬性訊息量
        self.effect_attr_name = ""    #屬性名稱
        self.attr_data=pd.DataFrame() 
        self.gainA=0.0
    
        
    def cal_i(self,x):
        '''
        用來算 I( X , Y )
        x=[5,9],x是list 
        '''
        total_count=0
        for one in x:
            total_count+=one
        sum=0.0
        for one in x:
            if(one==0):
                continue
            temp=(-one/total_count)*math.log2((one/total_count))
            sum+=temp
        return sum
    def caculate_attr(self):
        for index,raw in self.attr_data.iterrows(): #設定attr_subset
            if(raw[0] not in self.attr_subset): #第一次讀到
                temp_list=list()
                for one_conclusion in self.ss:
                    if(raw[1] == one_conclusion):
                        temp_list.append(1)
                    else:
                        temp_list.append(0)
                self.attr_subset[raw[0]]=temp_list
            else: #不是第一次讀到
                temp_list=list()
                for one_conclusion in self.ss:
                    if(raw[1] == one_conclusion):
                        temp_list.append(1)
                    else:
                        temp_list.append(0)
                self.attr_subset[raw[0]]=[a+b for a,b in zip(list(self.attr_subset[raw[0]]),temp_list)] 
        #算gain A
        for one in self.attr_subset.values():
            self.attr_info+=(sum(one)/self.attr_data.shape[0])*self.cal_i(one)
        self.gainA=self.parent_gainA-self.attr_info #結論-自己的屬性訊息量=GainA    

def main():
    panMain()
    # cccMain()
    

def panMain():
    test=raw_data(file_path='./觀測天氣之資料表.csv')# pan
    test.export_result("./觀測天氣之資料表---測試匯出.csv")
    
    pass

# def cccMain():
#     data = raw_data(file_path = './觀測天氣之資料表.csv')
#     # test = pd.read_csv('./觀測天氣之資料表.csv')
#     # attr = data.load_data(file_path = './觀測天氣之資料表.csv')
#     attr = data.load_data(file_path = './觀測天氣之資料表.csv')
#     for sub_attr in attr:
#         print(attr[sub_attr].effect_attr_name)
#         print('attribute_info:')
#         print(attr[sub_attr].attr_info)
#         print('gainA')
#         print(attr[sub_attr].gainA)
#     clean_data = clean_data()
#     print(clean_data.export_result())


if __name__ == "__main__":
    main()



#檢查CSV是否符合規則
def csvValidCheck(filename):
    rowSize=0
    standardRowSize=0
    with open(filename,'r',encoding="utf-8-sig") as f1:
        index=1
        lines=f1.readlines()
        for line in lines:
            temp=line.strip().split(',')
            if(index==1):
                rowSize=len(temp)
            else:
                standardRowSize=len(temp)
                if(rowSize!=standardRowSize):
                    return False,"csv檔第  "+str(index)+"  行的欄位數與其他行不一致\n"
                if(re.fullmatch(r'(\D*)+(\d*)',temp[-1],flags=0)== None):
                    return False,"csv檔第  "+str(index)+"  行的歸納結果不符合命名規則\n歸納結果的命名規則為:任意字元(不可以穿插數字)+數字\n"
                for item in temp:
                    if(item=="" or item==None):
                        return False,"csv檔第  "+str(index)+"  行有欄位為空\n"
            index+=1
        return True,"csv檔檢查通過,符合格式\n"
