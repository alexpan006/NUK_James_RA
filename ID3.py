#coding=utf-8
from email import policy
from isort import file
import pandas as pd
import math
from random import random


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

'''
0124 TODO before 0130
>>修改read_in_csv()>>傳入值可能是filePath/dataFrame>>要做不同的事 //// DONE >> 我把它改叫load_data()ㄌ，阿但是我不確定他會不會出事
>>clean_data產出policy>>policy包含effect, deep, simplicity, reliability, support, class distribution
>>修改結論>>最後一行必為結論>>結論可能不止2種 ///// DONE >> 我覺得啦，感覺沒啥毛病但我沒有第3種結論可以試，就是邏輯上應該沒事沒事
>>建立effect_attributes即計算gainA ///// DONE
'''


class clean_data:
    '''
    只記錄primary keys，然後會丟conclusion，用來算class distribution
    阿conclusion你在自己用ㄍ
    '''
    original_header=list
    primary_keys=dict() #主key
    conclusions=list()  #結論
    support=0.0 #
    reliability=0.0
    class_distribution="" #ex: "4,0"
    simplicity=0.0
    deep=0.0
    clean_data=pd.DataFrame()
    result={} #最終輸出dict 藥用dict to 

    def __init__(self,primary_keys=None,clean_data=None,original_header=None,conclusions=None,support=None):
        self.primary_keys=primary_keys #傳入primary key會是dict
        self.original_header=original_header
        self.clean_data=clean_data #是pd.DataFrame()
        self.conclusions=conclusions
        self.support=support #Support
    def cal_all(self):
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
        '''
        勝這裡
        # for k,v in self.primary_keys.items():
        #     # print('-->',k)
        #     for header in self.original_header:
        #         print(header)
        #         if(k==header):
        #             self.result[k]=v
        #         else:
        #             self.result[header]=None
        '''

        self.result["Deep"]=self.deep
        self.result["Support"]=self.support
        self.result["Reliability"]=self.reliability
        self.result["Class Distribution"]=self.class_distribution
        self.result["Simpicity"]=self.simplicity
        
        print(self.result)
        
            
        
        
        
    def export_result(self):
        self.cal_all()
        # print('primary_keys====>',self.primary_keys)
        # r_num = len(self.policy) + 1
        # for subset in self.primary_keys:
        #     deep = len(subset)
        '''
        判斷是哪個effect的結果、結論(class)是哪一個、有幾筆資料支持(support)、reliability(這啥我忘ㄌ)
        class distribution(有前面ㄉ好像就能算ㄌ)、simplicity(support/deep)
        好像來不及惹我玩回來再寫或哥你來QQ
        '''
            # print(subset)
            # r_num += 1
            
        
        


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
    
    #建構子
    def __init__(self,file_path=None,dataframe=None,primary_keys=None):
        '''
        先判定是否需要讀csv,若不用就直接用現有dataframe建立
        之後就先建立attri字典
        '''
        self.attributes.clear() #清空attributes
        self.primary_keys.clear() #清空primary keys
        # self.unclean_subsets.clear() #清空unclean_subsets
        # self.clean_subsets.clear() #清空clean_subsets
        
        if(primary_keys!=None):
            self.primary_keys=primary_keys #傳入primary key會是dict
        # self.fake_read_in_attributes(file_path=file_path,dataframe=dataframe) #先建立attri字典
        self.load_data(file_path=file_path,data=dataframe)
        self.sort_attri_order() #排序gainA
        self.reorder_raw_source() #依照attribute的gainA去重新排列data
        
        # print(self.raw_source)
        self.extract_to_subsets()  #分離clean與unclean資料
        
    #遞迴的部分
    def export_result(self):
        for clean_subset in self.clean_subsets:
            #TEST!!
            # clean_data.primary_keys.append(clean_subset.primary_keys)
            # print('primary key===>',clean_subset.primary_keys,clean_subset.support) 
            clean_subset.export_result()
        print('乾淨有',len(self.clean_subsets),'筆,','不乾淨',len(self.unclean_subsets),'筆') #測試用
    
    #把東西丟到subset裡
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
    
    
    #測試用
    def fake_read_in_attributes(self,file_path=None,dataframe=None):
        if(file_path!=None):    #要讀csv
            self.raw_source=pd.read_csv(file_path)
        else:#不用讀csv
            self.raw_source=dataframe
        for col in self.raw_source.columns[:-1]: #結論不用讀
            self.attributes[col]=effect_attribute(name=col,con=list(),gainA=0)
            
        # for k,v in self.attributes.items():
        #     print(k,v.gainA)
        # print('印reorder前的\n',self.raw_source.head()) #印reorder前的

    
    '''
    2022.01.25 14:08
    下面記得要用self,這樣才抓的到self.attributes字典
    像raw_data.conclusions.append(result) 應該是 self.conclusions.append(result)
    所以可能你之前會怪怪ㄉ就是因為這ㄍ
    '''
    
    '''
    0130
    ㄟㄟ你要用self.raw_source=pd.read_csv不然其他地方要用raw_data會吃不到
    
    '''
    
    #載入df回傳effect_attributes
    def load_data(self, file_path = None, data = None):
        if file_path == None: #不用讀csv
            self.raw_source = data
        else:
            self.raw_source = pd.read_csv(file_path) #讀檔
            '''
            # 設定clean_data的data
            clean_data.data = self.raw_source
            # 初始化policy(export)的dataframe
            clean_data.policy['RID'] = []
            for effect in self.raw_source.columns[:-1]:
                clean_data.policy[effect] = []
            clean_data.policy['Class'] = []
            clean_data.policy['Deep'] = []
            clean_data.policy['Support'] = []
            clean_data.policy['Reliability'] = []
            clean_data.policy['Class Distribution'] = []
            clean_data.policy['Simplicity'] = []
            '''
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
        '''
        #讀結論的col name
        for col in self.raw_source.columns[-1:]:
            self.s_col = col #記錄結論的col name
            
        con = self.raw_source[self.s_col].sort_values()
        data_sum = con.count() #資料總數
        con_type = con.T.drop_duplicates() #結論有哪幾種
        for result in con_type: #把結論存起來
            self.conclusions.append(result)
        print(self.conclusions)
        
        # 設定clean_data裡的conclusions
        clean_data.conclusions = self.conclusions
        con_type_num = len(self.conclusions)
        # 計算class_info
        for count in range(0,con_type_num):
            upper = con.value_counts()[count]
            self.class_info -= (upper/data_sum)*math.log2(upper/data_sum)
        #建立effect_attribute並計算gainA
        for col in self.raw_source.columns[:-1]:
            #建立effect_attribute
            self.attributes[col] = effect_attribute(name = col, con = self.conclusions, gainA = self.class_info)
            #計算gainA和attr_info
            #先排序資料>>只取結論跟該屬性
            arrange_sub_attr_data = self.raw_source[[col, self.s_col]].sort_values(by = self.s_col).sort_values(by = col)
            #call function進行計算
            self.attributes[col].caculate_attr(data = arrange_sub_attr_data)
            # 用ㄌself之後print出來他們還是都存在同一個attr_subset裡ㄟ，在搞在搞
            # print(self.attributes[col].attr_subset)
        '''
        '''
            就那個attr_subset還是頑固
            這裡在搞但不影響結果標出來給你看ㄍ
        '''
        '''
        return self.attributes
        '''    
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
    def __init__(self, name, conclusion, gainA,dataframe):
        self.attr_subset.clear()
        self.effect_attr_name = name
        self.ss = conclusion
        self.parent_gainA = gainA
        self.con_num = len(conclusion)
        self.attr_data=dataframe
        self.caculate_attr()
        
    #測試用
    def fake_data(self):
        self.attr_info=random.random()
        self.gainA=random.random()
        
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
        
        '''
        data_sum = len(data) #資料總筆數
        attr_data = data[self.effect_attr_name] #屬性資料
        data_type = attr_data.drop_duplicates() #取得屬性資料的種類
        attr_con = data.value_counts() #屬性+結論的個別總數
        
        data_type_num = data[self.effect_attr_name].value_counts() #屬性資料的個別總數 （有 9 無 0)

        for type in data_type: #初始化屬性結論
            temp_info = 0.0
            data_upper = data_type_num[type]
            con = self.ss
            
            type_con =[]
            type_sum = 0
            for idx in range(0,self.con_num):
                type_con.append(attr_con[type].get(con[idx]))
                #修正
                if type_con[idx] == None:
                    type_con[idx] = 0
                type_sum += type_con[idx]

            self.attr_subset[type] = type_con
            for result in self.attr_subset[type]:
                if result == 0: #如果沒有那種結果就跳過，不然算出來會出事
                    pass
                else:
                    temp_info -= (result/type_sum)*math.log2(result/type_sum)
            self.attr_info += (data_upper/data_sum)*temp_info

        self.gainA -= self.attr_info
        '''
        
        

def main():
    panMain()
    # cccMain()
    

def panMain():
    test=raw_data(file_path='./觀測天氣之資料表.csv')# pan
    test.export_result()
        
    pass

def cccMain():
    data = raw_data(file_path = './觀測天氣之資料表.csv')
    # test = pd.read_csv('./觀測天氣之資料表.csv')
    # attr = data.load_data(file_path = './觀測天氣之資料表.csv')
    attr = data.load_data(file_path = './觀測天氣之資料表.csv')
    for sub_attr in attr:
        print(attr[sub_attr].effect_attr_name)
        print('attribute_info:')
        print(attr[sub_attr].attr_info)
        print('gainA')
        print(attr[sub_attr].gainA)
    gaga = clean_data()
    print(gaga.export_result())


if __name__ == "__main__":
    main()