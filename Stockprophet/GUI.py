#author：王莉莉
#date:2019-06-01
#图形界面
#-*-coding:utf-8-*-
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
import datetime
import time
import sys
from math import *
from threading import Thread
from stockholm import Stockholm
import learningtest
import learning
import os
#获取偏移指定天数的时间表达式
def get_date_str(offset):
    if(offset is None):
        offset = 0
    date_str = (datetime.datetime.today() + datetime.timedelta(days=offset)).strftime("%Y%m%d")
    return date_str

class stockGUI:
    def __init__(self):
        self.root=Tk()
        self.root.title('股票预言家')
        self.root.geometry('400x300')
        self.canvas=Canvas(self.root,width=400,height=300,bg='white')
        self.root_pic=ImageTk.PhotoImage(file='stock.jpg')
        self.canvas.create_image(280, 150, image=self.root_pic)
        self.canvas.create_text(100,40,font=('Times',15,'bold'),text='股票预言家')
        self.canvas.create_text(95,65,font=('Times',15,'bold'),text='stock prophet')
        self.link1=Button(self.canvas,text='股票数据', font=('等线',11),command=self.callback1,width=15,height=1,bg='white')
        self.link2=Button(self.canvas,text='股票预测', font=('等线',11),command=self.callback2,width=15,height=1,bg='white')
        self.canvas.pack()
        self.link1.place(x=170,y=180,anchor=CENTER)
        self.link2.place(x=170,y=230,anchor=CENTER) 
        self.reload_data = 'Y'
        self.gen_portfolio = 'Y'
        self.output_type = 'csv'
        self.charset = 'utf-8'
        self.start_date = '20190101'
        self.end_date = '20190102'
        self.target_date = get_date_str(None)
        self.test_date_range = 30
        self.store_path = 'USER_HOME/tmp/stockholm_export'

        self.thread = 10
        self.testfile_path = './portfolio_test.txt'
        self.db_name = 'stockholm'
        self.methods = ''
        self.export_file_name='stockholm_export'
        self.num_stock = 'sh600771'
        self.stock_symbol='sh600771'
        self.end_date_db='20190102'
        self.target_date_db='2019-01-02'
    #数据存储
    def get_stockholm_run1(self):
        self.store_path=self.store_pathv.get()
        if(self.v_num.get()==1):
            self.num_stock='all'
        else:
            self.num_stock=self.num.get()

        if(self.v.get()==1):
            self.output_type='json'
        elif(self.v.get()==2):
            self.output_type='csv'
        else:
            self.output_type='all'
        
        if(self.v2.get()==1):
            self.charset='utf-8'
        else:
            self.charset='gbk'
        self.start_date = self.start_date1.get()+self.start_date2.get()+self.start_date3.get()
        self.end_date = self.end_date1.get()+self.end_date2.get()+self.end_date3.get()
        self.export_file_name = self.export_en.get()
        self.stock_en.set('正在获取数据')
        stockh = Stockholm(self)
        stockh.run1() 
        self.stock_en.set('获取数据完成')
    #选股测试
    def get_stockholm_run2(self):
        self.target_date=self.target_date1.get()+self.target_date2.get()+self.target_date3.get()
        self.test_date_range=int(self.target_length.get())
        self.pick_en.set('正在获取选股结果')
        stockh = Stockholm(self)
        stockh.run2() 
        self.pick_en.set('获取选股结果完成')
    #获取单支股票的详细数据
    def get_stockholm_detail(self):
        reader_list=['1','2','3','4','5','6','7','8','9','10']
        win2=Toplevel()
        win2.title('股票预言家')
        win2.geometry('500x600')
        canvas2=Canvas(win2,width=500,height=600,bg='white')
        canvas2.pack()
        self.date1=StringVar()
        self.date2=StringVar()
        self.date3=StringVar()
        self.end_date1_db=StringVar()
        self.end_date2_db=StringVar()
        self.end_date3_db=StringVar()
        self.open_v=StringVar()
        self.close_v=StringVar()
        self.high_v=StringVar()
        self.low_v=StringVar()
        self.change_v=StringVar()
        self.volume_v=StringVar()
        self.vol_change_v=StringVar()
        self.Turnover_v=StringVar()
        self.TurnoverRate_v=StringVar()
        self.Chg_v=StringVar()
        self.KDJ_K_v=StringVar()
        self.KDJ_D_v=StringVar()
        self.KDJ_J_v=StringVar()
        self.pic_v=IntVar()
        self.end_date1_db.set('2019')
        self.end_date2_db.set('01')
        self.end_date3_db.set('02')
        self.pic_v.set(1)
        self.symbol=StringVar()
        self.symbol.set('sh600771')
        frame2 = Frame(win2,width=476,height=530,bd=4,relief='groove',bg='white')
        frame2.place(x=12,y=60,anchor=N+W)
        
        symbol_label=Label(win2,bg='white',font=('Times',15,'bold'),text='股票名：')
        symbol_label.place(x=30,y=30)
        en2 = Entry(win2,textvariable=self.symbol)
        en2.place(x=185,y=38,width=150,height=30,anchor=CENTER)
        pic_label=Label(frame2,bg='white',font=('Times',15,'bold'),text='股票走势图表')
        pic_label.place(x=15,y=20)

        end_date_label=Label(frame2,bg='white',text='目标日期：')
        end_date_label.place(x=15,y=70)
        en8 = Entry(frame2,textvariable=self.end_date1_db)
        en8.place(x=120,y=78,width=50,height=20,anchor=CENTER)
        en9 = Entry(frame2,textvariable=self.end_date2_db)
        en9.place(x=220,y=78,width=50,height=20,anchor=CENTER)
        en10 = Entry(frame2,textvariable=self.end_date3_db)
        en10.place(x=320,y=78,width=50,height=20,anchor=CENTER)
        end_date_label1=Label(frame2,bg='white',text='年')
        end_date_label2=Label(frame2,bg='white',text='月')
        end_date_label3=Label(frame2,bg='white',text='日')
        end_date_label1.place(x=165,y=70)  
        end_date_label2.place(x=265,y=70)
        end_date_label3.place(x=365,y=70)
        pic_rb1=Radiobutton(frame2,bg='white',text='KDJ_K',variable=self.pic_v,value=1)
        pic_rb2=Radiobutton(frame2,bg='white',text='KDJ_D',variable=self.pic_v,value=2)
        pic_rb3=Radiobutton(frame2,bg='white',text='KDJ_J',variable=self.pic_v,value=3)
        pic_rb4=Radiobutton(frame2,bg='white',text='Close',variable=self.pic_v,value=4)
        pic_rb1.place(x=15,y=115)
        pic_rb2.place(x=85,y=115)
        pic_rb3.place(x=155,y=115)
        pic_rb4.place(x=225,y=115)

        con_bt = Button(frame2,bg='white',text = "显示图表",width=9,height=1,
                    command =self.get_plot)
        con_bt.place(x=390,y=115)
        stock_date_label=Label(frame2,bg='white',font=('Times',15,'bold'),text='具体股票信息')
        stock_date_label.place(x=15,y=175)
        date_label=Label(frame2,bg='white',text='日期：')
        date_label.place(x=15,y=210)
        date_label1=Label(frame2,bg='white',text='年')
        date_label2=Label(frame2,bg='white',text='月')
        date_label3=Label(frame2,bg='white',text='日')
        date_label1.place(x=150,y=210)  
        date_label2.place(x=250,y=210)
        date_label3.place(x=350,y=210)
        en2 = Entry(frame2,textvariable=self.date1)
        en2.place(x=100,y=218,width=50,height=20,anchor=CENTER)
        en3 = Entry(frame2,textvariable=self.date2)
        en3.place(x=200,y=218,width=50,height=20,anchor=CENTER)
        en4 = Entry(frame2,textvariable=self.date3)
        en4.place(x=300,y=218,width=50,height=20,anchor=CENTER)
        open_label=Label(frame2,bg='white',font=('等线',10,'bold'),text='Open(开盘价):')
        close_label=Label(frame2,bg='white',font=('等线',10,'bold'),text='Close(收盘价):')
        high_label=Label(frame2,bg='white',font=('等线',10,'bold'),text='High(当日最高):')
        low_label=Label(frame2,bg='white',font=('等线',10,'bold'),text='Low(当日最低):')
        change_label=Label(frame2,bg='white',font=('等线',10,'bold'),text='Change(价格变化%):')
        volume_label=Label(frame2,bg='white',font=('等线',10,'bold'),text='Volume(成交量):')
        vol_change_label=Label(frame2,bg='white',font=('等线',10,'bold'),text='Vol_Change(成交量较前日变化):')
        Turnover_label=Label(frame2,bg='white',font=('等线',10,'bold'),text='Turnover(成交额):')
        TurnoverRate_label=Label(frame2,bg='white',font=('等线',10,'bold'),text='TurnoverRate(换手率):')
        Chg_label=Label(frame2,bg='white',font=('等线',10,'bold'),text='Chg(涨幅):')
        KDJ_K_label=Label(frame2,bg='white',font=('等线',10,'bold'),text='KDJ_K(KDJ指标K):')
        KDJ_D_label=Label(frame2,bg='white',font=('等线',10,'bold'),text='KDJ_D(KDJ指标D):')
        KDJ_J_label=Label(frame2,bg='white',font=('等线',10,'bold'),text='KDJ_J(KDJ指标J):')
        open_label.place(x=15,y=240)
        close_label.place(x=215,y=240)
        high_label.place(x=15,y=270)
        low_label.place(x=215,y=270)
        change_label.place(x=15,y=300)
        volume_label.place(x=215,y=300)
        vol_change_label.place(x=15,y=330)
        Turnover_label.place(x=15,y=360)
        TurnoverRate_label.place(x=215,y=360)
        Chg_label.place(x=15,y=390)
        KDJ_K_label.place(x=215,y=390)
        KDJ_D_label.place(x=15,y=420)
        KDJ_J_label.place(x=215,y=420)
        open_en = Entry(frame2,textvariable=self.open_v)
        open_en.place(x=180,y=248,width=50,height=20,anchor=CENTER)
        close_en = Entry(frame2,textvariable=self.close_v)
        close_en.place(x=380,y=248,width=50,height=20,anchor=CENTER)
        high_en = Entry(frame2,textvariable=self.high_v)
        high_en.place(x=180,y=278,width=50,height=20,anchor=CENTER)
        low_en = Entry(frame2,textvariable=self.low_v)
        low_en.place(x=380,y=278,width=50,height=20,anchor=CENTER)
        change_en = Entry(frame2,textvariable=self.change_v)
        change_en.place(x=180,y=308,width=50,height=20,anchor=CENTER)
        volume_en = Entry(frame2,textvariable=self.volume_v)
        volume_en.place(x=380,y=308,width=50,height=20,anchor=CENTER)
        vol_change_en = Entry(frame2,textvariable=self.vol_change_v)
        vol_change_en.place(x=250,y=338,width=50,height=20,anchor=CENTER)
        Turnover_en = Entry(frame2,textvariable=self.Turnover_v)
        Turnover_en.place(x=180,y=368,width=50,height=20,anchor=CENTER)
        TurnoverRate_en = Entry(frame2,textvariable=self.Turnover_v)
        TurnoverRate_en.place(x=380,y=368,width=50,height=20,anchor=CENTER)
        Chg_en = Entry(frame2,textvariable=self.Chg_v)
        Chg_en.place(x=180,y=398,width=50,height=20,anchor=CENTER)
        KDJ_K_en = Entry(frame2,textvariable=self.Chg_v)
        KDJ_K_en.place(x=380,y=398,width=50,height=20,anchor=CENTER)
        KDJ_D_en = Entry(frame2,textvariable=self.Chg_v)
        KDJ_D_en.place(x=180,y=428,width=50,height=20,anchor=CENTER)
        KDJ_J_en = Entry(frame2,textvariable=self.Chg_v)
        KDJ_J_en.place(x=380,y=428,width=50,height=20,anchor=CENTER)
        inf_bt = Button(frame2,bg='white',text = "显示数据",width=9,height=2,
                    command =self.get_inf)
        inf_bt.place(x=390,y=470)
    #为指定的股票作图  
    def get_plot(self):
        self.stock_symbol=self.symbol.get()
        self.end_date_db=self.end_date1_db.get()+'-'+self.end_date2_db.get()+'-'+self.end_date3_db.get()
        self.num_stock = 'all'   ######################################
        if(self.pic_v.get()==1):
            self.pic_name='KDJ_K'
        elif(self.pic_v.get()==2):
            self.pic_name='KDJ_D'
        elif(self.pic_v.get()==3):    
            self.pic_name='KDJ_J'
        else:
            self.pic_name='Close'
        stockh = Stockholm(self)
        stockh.draw_choice(self.num_stock,self.pic_name,self.end_date_db)
    #获取股票的详细信息
    def get_inf(self):
        self.stock_symbol=self.symbol.get()
        self.target_date_db=self.date1.get()+'-'+self.date2.get()+'-'+self.date3.get()
        self.num_stock = 'all' #########################################
        stockh = Stockholm(self)
        inf_dict=stockh.select_mongo(self.stock_symbol,self.target_date_db)
        if(inf_dict==0):
            self.open_v.set("")
            self.close_v.set("")
            self.high_v.set("")
            self.low_v.set("")
            self.change_v.set("")
            self.volume_v.set("")
            self.vol_change_v.set("")
            self.Turnover_v.set("")
            self.TurnoverRate_v.set("")
            self.Chg_v.set("")
            self.KDJ_K_v.set("")
            self.KDJ_D_v.set("")
            self.KDJ_J_v.set("")
        else:
            self.open_v.set(inf_dict['Open'])
            self.close_v.set(inf_dict['Close'])
            self.high_v.set(inf_dict['High'])
            self.low_v.set(inf_dict['Low'])
            self.change_v.set(inf_dict['Change'])
            self.volume_v.set(inf_dict['Volume'])
            self.vol_change_v.set(inf_dict['Vol_Change'])
            self.Turnover_v.set(inf_dict['Turnover'])
            self.TurnoverRate_v.set(inf_dict['TurnoverRate'])
            self.Chg_v.set(inf_dict['Chg'])
            self.KDJ_K_v.set(inf_dict['KDJ_K'])
            self.KDJ_D_v.set(inf_dict['KDJ_D'])
            self.KDJ_J_v.set(inf_dict['KDJ_J'])
    #股票预测机器学习（数据对比）
    def get_learning_test(self):
        if(self.store_path == 'USER_HOME/tmp/stockholm_export'):
            self.export_folder = os.path.expanduser('~') + '/tmp/stockholm_export'
        else:
            self.export_folder = self.store_path
        self.learning_date=self.learning_date1.get()+self.learning_date2.get()+self.learning_date3.get()
        self.num_stock=self.learning_symbol.get()
        #print(self.num_stock)
        self.export_file_name='learning1'
        self.start_date = '20110101'
        self.end_date = self.learning_date
        stockh = Stockholm(self)
        stockh.run1() 
        self.export_file_name='learning2'
        ld=datetime.datetime(int(self.learning_date1.get()),int(self.learning_date2.get()),int(self.learning_date3.get()))
        self.start_date = (ld + datetime.timedelta(days=1)).strftime("%Y%m%d")
        self.end_date = get_date_str(None)
        stockh2 = Stockholm(self)
        stockh2.run1()
        self.variance=learningtest.stock_predection_test(self.export_folder+'/'+"learning1.csv",self.export_folder+'/'+"learning2.csv",60)
    #股票预测机器学习（预测下一天）
    def get_learning(self):
        if(self.store_path == 'USER_HOME/tmp/stockholm_export'):
            self.export_folder = os.path.expanduser('~') + '/tmp/stockholm_export'
        else:
            self.export_folder = self.store_path
        self.learning_date=self.learning_date1.get()+self.learning_date2.get()+self.learning_date3.get()
        self.num_stock=self.learning_symbol.get()
        #print(self.num_stock)
        self.export_file_name='learning'
        self.start_date = '20120101'
        self.end_date = get_date_str(None)
        stockh3 = Stockholm(self)  
        stockh3.run1() 
        self.predicted_price=learning.stock_predection(self.export_folder+'/'+"learning.csv")
        
    def get_date_str(self,offset):
        if(offset is None):
            offset = 0
        date_str = (datetime.datetime.today() + datetime.timedelta(days=offset)).strftime("%Y-%m-%d")
        return date_str
    #数据获取和选股界面           
    def callback1(self):            
        # build main win1        
        self.win1=Toplevel()
        self.win1.title('股票预言家')
        self.win1.geometry('500x500')
        self.canvas=Canvas(self.win1,width=500,height=700,bg='white')
        self.canvas.pack()

        self.frame1=Frame(self.win1,width=500,height=500,bd=4,bg='white')
        self.frame1.place(x=0,y=20,anchor=N+W)
        self.v_num=IntVar()
        self.v_num.set(1)
        self.v=IntVar()
        self.v.set(1)
        self.v2=IntVar()
        self.v2.set(1)
        self.num=StringVar()
        self.num.set('sh600771')
        self.store_pathv=StringVar()
        self.store_pathv.set('USER_HOME/tmp/stockholm_export')
        self.start_date1=StringVar()
        self.start_date2=StringVar()
        self.start_date3=StringVar()
        self.end_date1=StringVar()
        self.end_date2=StringVar()
        self.end_date3=StringVar()
        self.target_date1=StringVar()
        self.target_date2=StringVar()
        self.target_date3=StringVar()
        self.start_date1.set('2019')
        self.start_date2.set('01')
        self.start_date3.set('01')
        self.end_date1.set('2019')
        self.end_date2.set('01')
        self.end_date3.set('02')
        self.target=get_date_str(None)
        self.target_date1.set(self.target[0:4])
        self.target_date2.set(self.target[4:6])
        self.target_date3.set(self.target[6:8])
        self.export_en=StringVar()
        self.export_en.set('stockholm_export')    
        self.stock_en=StringVar()
        self.pick_en=StringVar()
        self.target_length=StringVar()
        self.stock_num_label=Label(self.frame1,bg='white',text='选取股票数量：')
        self.stock_file_label=Label(self.frame1,bg='white',text='输出文件格式：')
        self.file_directory_label=Label(self.frame1,bg='white',text='输出文件路径：')
        self.export_file_label=Label(self.frame1,bg='white',text='输出文件名：')
        self.file_code_label=Label(self.frame1,bg='white',text='文件编码格式：')

        self.stock_num_rb1=Radiobutton(self.frame1,bg='white',text='all',variable=self.v_num,value=1)
        self.stock_num_rb2=Radiobutton(self.frame1,bg='white',text='one',variable=self.v_num,value=2)
        self.stock_file_rb1=Radiobutton(self.frame1,bg='white',text='json',variable=self.v,value=1)
        self.stock_file_rb2=Radiobutton(self.frame1,bg='white',text='csv',variable=self.v,value=2)
        self.stock_file_rb3=Radiobutton(self.frame1,bg='white',text='all',variable=self.v,value=3)
        self.file_code_rb1=Radiobutton(self.frame1,bg='white',text='utf-8',variable=self.v2,value=1)
        self.file_code_rb2=Radiobutton(self.frame1,bg='white',text='gbk',variable=self.v2,value=2)
        self.en_num = Entry(self.frame1,textvariable=self.num)
        self.stock_num_label.place(x=10,y=20)
        self.stock_file_label.place(x=10,y=50)
        self.file_directory_label.place(x=10,y=80)
        self.export_file_label.place(x=10,y=110)
        self.file_code_label.place(x=10,y=140)

        self.stock_num_rb1.place(x=110,y=20)
        self.stock_num_rb2.place(x=160,y=20)
        self.stock_file_rb1.place(x=110,y=50)
        self.stock_file_rb2.place(x=160,y=50)
        self.stock_file_rb3.place(x=200,y=50)
        self.file_code_rb1.place(x=110,y=140)
        self.file_code_rb2.place(x=160,y=140)
        self.en_num.place(x=230,y=20)

        self.begin_date_label=Label(self.frame1,bg='white',text='开始日期：')
        self.end_date_label=Label(self.frame1,bg='white',text='结束日期：')
        self.begin_date_label.place(x=10,y=170)
        self.end_date_label.place(x=10,y=200)
        self.en5 = Entry(self.frame1,textvariable=self.start_date1)
        self.en5.place(x=120,y=178,width=50,height=20,anchor=CENTER)
        self.en6 = Entry(self.frame1,textvariable=self.start_date2)
        self.en6.place(x=220,y=178,width=50,height=20,anchor=CENTER)
        self.en7 = Entry(self.frame1,textvariable=self.start_date3)
        self.en7.place(x=320,y=178,width=50,height=20,anchor=CENTER)
        self.en8 = Entry(self.frame1,textvariable=self.end_date1)
        self.en8.place(x=120,y=208,width=50,height=20,anchor=CENTER)
        self.en9 = Entry(self.frame1,textvariable=self.end_date2)
        self.en9.place(x=220,y=208,width=50,height=20,anchor=CENTER)
        self.en10 = Entry(self.frame1,textvariable=self.end_date3)
        self.en10.place(x=320,y=208,width=50,height=20,anchor=CENTER)
        self.start_date_label1=Label(self.frame1,bg='white',text='年')
        self.start_date_label2=Label(self.frame1,bg='white',text='月')
        self.start_date_label3=Label(self.frame1,bg='white',text='日')
        self.end_date_label1=Label(self.frame1,bg='white',text='年')
        self.end_date_label2=Label(self.frame1,bg='white',text='月')
        self.end_date_label3=Label(self.frame1,bg='white',text='日')
        self.start_date_label1.place(x=165,y=170)  
        self.start_date_label2.place(x=265,y=170)
        self.start_date_label3.place(x=365,y=170) 
        self.end_date_label1.place(x=165,y=200)  
        self.end_date_label2.place(x=265,y=200)
        self.end_date_label3.place(x=365,y=200)

        self.en1 = Entry(self.frame1,textvariable=self.store_pathv)
        self.en1.place(x=255,y=90,width=300,height=20,anchor=CENTER)
        self.en2 = Entry(self.frame1,textvariable=self.export_en)
        self.en2.place(x=255,y=120,width=300,height=20,anchor=CENTER)
        self.en3 = Entry(self.frame1,textvariable=self.stock_en)
        self.en3.place(x=255,y=240,width=100,height=20,anchor=CENTER)
        self.stock_bt = Button(self.frame1,bg='white', text = "获取数据",width=9,height=1,
                    command =self.get_stockholm_run1)
        self.stock_bt.place(x=100,y=230)

        self.target_date_label=Label(self.frame1,bg='white',text='选股日期:')
        self.target_date_label.place(x=10,y=290) 
        self.target_date_label1=Label(self.frame1,bg='white',text='年')
        self.target_date_label2=Label(self.frame1,bg='white',text='月')
        self.target_date_label3=Label(self.frame1,bg='white',text='日')
        self.target_date_label1.place(x=165,y=290)  
        self.target_date_label2.place(x=265,y=290)
        self.target_date_label3.place(x=365,y=290)
        self.target_length_label=Label(self.frame1,bg='white',text='时间跨度:')
        self.target_length_label.place(x=10,y=320)
        
        self.target_en1 = Entry(self.frame1,textvariable=self.target_date1)
        self.target_en1.place(x=120,y=298,width=50,height=20,anchor=CENTER)
        self.target_en2 = Entry(self.frame1,textvariable=self.target_date2)
        self.target_en2.place(x=220,y=298,width=50,height=20,anchor=CENTER)
        self.target_en3 = Entry(self.frame1,textvariable=self.target_date3)
        self.target_en3.place(x=320,y=298,width=50,height=20,anchor=CENTER)
        self.target_en4 = Entry(self.frame1,textvariable=self.target_length)
        self.target_en4.place(x=150,y=328,width=100,height=20,anchor=CENTER)
        
        self.pickh_bt = Button(self.frame1,bg='white',text = "选股测试",width=9,height=1,
                    command =self.get_stockholm_run2)
        self.pickh_bt.place(x=100,y=350)  
        self.pickh_en = Entry(self.frame1,textvariable=self.pick_en)
        self.pickh_en.place(x=255,y=360,width=100,height=20,anchor=CENTER)
        self.detail_bt = Button(self.frame1,bg='white',text = "获取详细数据",width=12,height=1,
                    command =self.get_stockholm_detail)
        self.detail_bt.place(x=150,y=400)
    #股票预测界面
    def callback2(self):
        self.win2=Toplevel()
        self.win2.title('股票预言家')
        self.win2.geometry('500x300')
        self.canvas2=Canvas(self.win2,width=500,height=300,bg='white')
        self.canvas2.pack()

        self.frame2=Frame(self.win2,width=500,height=300,bd=4,bg='white')
        self.frame2.place(x=0,y=20,anchor=N+W)
        self.learning_symbol=StringVar()
        self.learning_symbol.set('sh600771')
        self.learning_date1=StringVar()
        self.learning_date1.set('2019')
        self.learning_date2=StringVar()
        self.learning_date2.set('01')
        self.learning_date3=StringVar()
        self.learning_date3.set('01')
        self.symbol_label=Label(self.win2,bg='white',font=('Times',15,'bold'),text='股票名：')
        self.symbol_label.place(x=30,y=30)
        self.ls_en = Entry(self.win2,font=('等线',11,'bold'),textvariable=self.learning_symbol)
        self.ls_en.place(x=185,y=40,width=150,height=28,anchor=CENTER)
        self.learing_date_label=Label(self.frame2,bg='white',font=('等线',11,'bold'),text='测试日期:')
        self.learing_date_label.place(x=30,y=82) 
        self.learing_date_label1=Label(self.frame2,bg='white',font=('等线',11,'bold'),text='年')
        self.learing_date_label2=Label(self.frame2,bg='white',font=('等线',11,'bold'),text='月')
        self.learing_date_label3=Label(self.frame2,bg='white',font=('等线',11,'bold'),text='日')
        self.learing_date_label1.place(x=165,y=86)  
        self.learing_date_label2.place(x=265,y=86)
        self.learing_date_label3.place(x=365,y=86)
        self.learning_en1 = Entry(self.frame2,textvariable=self.learning_date1)
        self.learning_en1.place(x=128,y=95,width=50,height=20,anchor=CENTER)
        self.learning_en2 = Entry(self.frame2,textvariable=self.learning_date2)
        self.learning_en2.place(x=228,y=95,width=50,height=20,anchor=CENTER)
        self.learning_en3 = Entry(self.frame2,textvariable=self.learning_date3)
        self.learning_en3.place(x=328,y=95,width=50,height=20,anchor=CENTER)
        self.learning_test_bt = Button(self.frame2,bg='white',text = "预测对比",font=('等线',11,'bold'),width=10,height=1,
                    command =self.get_learning_test)
        self.learning_test_bt.place(x=100,y=140)
        self.learning_bt = Button(self.frame2,bg='white',text = "股票预测",font=('等线',11,'bold'),width=10,height=1,
                    command =self.get_learning)
        self.learning_bt.place(x=240,y=140)

    def running(self):
        #self.thread_clock()
        self.root.mainloop()

def main():
    m=stockGUI()
    m.running()
    
if __name__=="__main__":
    main()
    
