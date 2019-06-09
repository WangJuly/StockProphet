#方差 预测的时间范围内的最大值 获得的利润
#stock_predection("D:\\learning1.csv","D:\\learning2.csv",60)
#
#training & test, camparation of prediction and price
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from math import *
import time
from datetime import datetime
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

register_matplotlib_converters()

#iloc取值根据csv文件更改
#time_step为60，即用59天的数据预测第六十天，可以改变timestep

def prepare_train(time_step,train_data_source):
    #导入训练集，train_data_source:csv文件路径
    dataset_train = pd.read_csv(train_data_source)
    dataset_train = dataset_train[~(dataset_train['Type'].isnull())] #去除csv文件空行
    #r = map(lambda x : time.strftime('%Y-%m-%d',time.localtime(x)),dataset_train['data.Date']) 如time为时间戳，改为%Y-%m-%d
    #dataset_train['data.Date'] = list(r)

    training_set = dataset_train.iloc[:, [5]].values #取close一列
    #将数据集缩放到0-1间
    sc = MinMaxScaler(feature_range = (0, 1))
    training_set_scaled = sc.fit_transform(training_set)

    #训练
    X_train = []
    y_train = []
    for i in range(time_step, dataset_train.shape[0]):
        X_train.append(training_set_scaled[i-time_step:i, 0])
        y_train.append(training_set_scaled[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    return X_train,y_train,dataset_train,sc,training_set

def train(X_train,y_train):
    #构建lstm，3层LSTM+1层Dense，每层利用Dropout（0.2）避免过拟合，epochs=20为迭代轮次，可更改
    #Dropout值、LSTM的层次为调参项
    Model = Sequential()
    Model.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
    Model.add(Dropout(0.2))
    Model.add(LSTM(units = 50, return_sequences = True))
    Model.add(Dropout(0.2))
    Model.add(LSTM(units = 50))
    Model.add(Dense(units = 1))
    Model.compile(optimizer = 'adam', loss = 'mean_squared_error')
    Model.fit(X_train, y_train, epochs = 20, batch_size = 32,verbose=2)
    return Model

def prediction(dataset_train,time_step,test_data_source,sc,model):
    #导入测试集，test_data_source:csv文件路径
    dataset_test = pd.read_csv(test_data_source)
    dataset_test = dataset_test[~(dataset_test['Type'].isnull())]

    test_set = dataset_test.iloc[:, [5]].values #取close列
    dataset_total = pd.concat((dataset_train['data.Close'], dataset_test['data.Close']), axis = 0) #合并训练集测试集
    inputs = dataset_total[len(dataset_total) - len(dataset_test) - time_step:].values
    inputs = inputs.reshape(-1,1)
    inputs = sc.transform(inputs)
    X_test = []
    for i in range(time_step, inputs.shape[0]):
        X_test.append(inputs[i-time_step:i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_price = model.predict(X_test)
    predicted_price = sc.inverse_transform(predicted_price)
    return predicted_price,X_test,dataset_test,test_set

def plot(dataset_train,dataset_test,predicted_price,training_set,test_set,variance,lost):
    #作图
    plt.figure(figsize=(20,10))
    plt.title('Stock Price Prediction --variance:'+variance+' --lost:'+lost)

    x1 = np.array(dataset_train['data.Date'])
    y1 = training_set
    plt.plot(x1,y1,color='black',label = 'Stock Price') #训练集历史数据
    x2 = np.array(dataset_test['data.Date'])
    y2 = test_set
    plt.plot(x2,y2,color='orange',label = 'True Stock Price')   #测试集真实数据
    x3 = np.array(dataset_test['data.Date'])
    y3 = predicted_price
    plt.plot(x3,y3,color='blue',label = 'Predicted Stock Price')    #预测股价

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(200))  #设置x坐标间隔
    plt.gcf().autofmt_xdate()#自动旋转日期标记
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend() #放label
    plt.show()


def stock_predection_test(train_data_source,test_data_source,time_step):
    time_step = int(time_step)

    X_train,y_train,dataset_train,scaler,training_set = prepare_train(time_step,train_data_source)
    model = train(X_train,y_train)
    predicted_price,X_test,dataset_test,test_set = prediction(dataset_train,time_step,test_data_source,scaler,model)
    
    true_price = scaler.inverse_transform(test_set)
    true_price = np.array(test_set)
    variance = np.sqrt(np.mean(np.power((true_price-predicted_price),2))) #计算预测误差
    lost = np.mean(abs(predicted_price - true_price)/true_price)*100
    max_price = np.max(predicted_price)
    #max_earn = max_price-predicted_price[0]
    #max_index = np.argmax(predicted_price)
    #print ("预测结果方差为",variance)
    print ("预测平均相对误差为%.3f " %(lost))
    plot(dataset_train,dataset_test,predicted_price,training_set,test_set,str(variance),str(lost))

    return variance,lost

