#encoding=utf8
from os import error, stat
import tkinter as tk
from tkinter.constants import BOTTOM
from tkinter.filedialog import askopenfilename, test
from analysis_stage1 import csvValidCheck, exportUncleanDataNew
from analysis_stage1 import csvAnalyzeData
from analysis_stage1 import sortRuleRow

from tkinter import ttk 

class analyzeGui:
    filename=""
    def showChooseFile(self):
        self.rule.set('')
        self.filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        self.writeToMiniConsole("你選擇的檔案路徑為-->"+self.filename+"\n")
        
    def writeToMiniConsole(self,string):
        self.miniConsole.config(state='normal')
        self.miniConsole.insert('insert',string)
        self.miniConsole.config(state='disable')
        self.miniConsole.see(tk.END)
        
    def sortRule(self):
        self.rule.set('')
        if(self.filename==""):
            self.writeToMiniConsole('還沒有選擇欲排序欄位的csv檔\n')
            return
        self.isOkay=False
        while(not self.isOkay):
            if(self.rule.get() == 'quit' or self.rule.get() == 'q' or self.rule.get() == 'Quit'):
                self.writeToMiniConsole('結束排序欄位\n')
                self.rule.set('')
                return
            self.isOkay,state,newFileName,isNeedInput=sortRuleRow(self.filename,self.rule.get())
            if( self.isOkay ==False and isNeedInput == True): #要輸入新order
                self.writeToMiniConsole(state)
                self.miniConsole.config(state='normal')
                self.miniConsole.wait_variable(self.rule)
                continue
            if(self.isOkay == False):    #轉換時出bug
                self.writeToMiniConsole(state)
        if(self.isOkay!=True):
            return
        self.writeToMiniConsole('轉檔完成,新檔案名稱為'+newFileName+'\n')
        self.miniConsole.config(state='disable')
        self.rule.set('')
        return
    
    def exportUnclean(self):
        if(self.filename==""):
            self.writeToMiniConsole('還沒有選擇欲分離不相容資料的csv檔\n')
            return
        self.isOkay=False
        while(not self.isOkay):
            self.writeToMiniConsole('請輸入相容資料的接受等級(一定要大於0.51)，輸入完請按Enter\n')
            self.miniConsole.config(state='normal')
            self.miniConsole.wait_variable(self.rule)
            if(self.rule.get()==None or self.rule.get()==''):
                continue
            if(float(self.rule.get())<=0.5):
                continue
            clean,unclean,state,self.isOkay=exportUncleanDataNew(self.filename,float(self.rule.get()))
            if(not self.isOkay):
                self.writeToMiniConsole('出錯'+state+"\n")
        self.writeToMiniConsole('相容資料以輸出至==>'+clean+"\n"+'不相容資料以輸出至==>'+unclean+'\n')
        self.miniConsole.config(state='disable')
    
    def startAnalyze(self):
        self.rule.set('')
        if(self.filename==""):
            self.writeToMiniConsole('還沒有選擇欲分析的csv檔\n')
            return
        try:
            resultToken,result=csvValidCheck(self.filename)
        except :
            self.writeToMiniConsole('發生預期外的錯誤1\n')
            # self.writeToMiniConsole(stac)
        if(resultToken):
            try:
                result=csvAnalyzeData(self.filename)
                self.writeToMiniConsole('分析完成,輸出結果位於-->'+result+'\n')
            except Exception as err:
                self.writeToMiniConsole('發生預期外的錯誤2\n')
                self.writeToMiniConsole(err)

        else:
            self.writeToMiniConsole('原始csv不符合格式:\n'+result)
    def onChange(self,event):
        self.rule.set(event.widget.get("end-1c linestart", "end-1c"))   
    def on_closing(self): 
        self.isOkay=True
        self.window.destroy()
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('CSV分析')
        self.window.geometry('700x500')
        topFrame=tk.Frame(self.window)
        topFrame.pack()
        bottomFrame=tk.Frame(self.window)
        bottomFrame.pack(side=BOTTOM)
        #檔案路徑label
        lbl_1 = tk.Label(topFrame, text='Csv檔案路徑:', fg='#263238', font=('Arial', 12))
        lbl_1.grid(column=0, row=0,pady=10)

        #選擇button
        chooseCsvFile=tk.Button(topFrame,text='選擇Csv檔案',fg='Green',command=self.showChooseFile)
        chooseCsvFile.grid(column=0, row=1,pady=10)
        
        #分離不相容
        exportUnclean=tk.Button(topFrame,text='分離不相容資料',fg='Green',command=self.exportUnclean)
        exportUnclean.grid(column=0, row=2,pady=10)
        
        
        #規則欄位排序
        sortRule=tk.Button(topFrame,text='規則欄位排序',fg='Green',command=self.sortRule)
        sortRule.grid(column=0, row=3,pady=10)
        
        
        
        
        #開始分析button
        startButton=tk.Button(topFrame,text='產生決策規則',fg='Red',command=self.startAnalyze)
        startButton.grid(column=0, row=4,pady=20)
        
        
        #mini console
        self.miniConsole=tk.Text(bottomFrame,fg="Black",state='disable',width=80,height=10,relief='solid',borderwidth=2,font=('Arial', 13))
        self.miniConsole.grid(column=0, row=0)
        self.miniConsole.bind("<Return>",self.onChange)
        
        self.rule=tk.StringVar()
        
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

if __name__ == '__main__':
    gui=analyzeGui()
    
    


