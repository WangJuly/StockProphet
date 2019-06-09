#完成预测一天功能
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

def stock_predection(train_data_source):
    time_step=60

    #data_source:csv文件路径
    dataset_train = pd.read_csv(train_data_source)
    dataset_train = dataset_train[~(dataset_train['Type'].isnull())]
    training_set = dataset_train.iloc[:,[5]].values

    sc = MinMaxScaler(feature_range = (0, 1))#数据集缩放到0-1间
    training_set_scaled = sc.fit_transform(training_set)

    #构建lstm，3层LSTM，1层Dense，利用Dropout避免过拟合
    X_train = []
    y_train = []
    for i in range(time_step, dataset_train.shape[0]):
        X_train.append(training_set_scaled[i-time_step:i, 0])
        y_train.append(training_set_scaled[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    #Dropout层20%,避免过拟合
    Model = Sequential()
    Model.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
    Model.add(Dropout(0.2))
    Model.add(LSTM(units = 50, return_sequences = True))
    Model.add(Dropout(0.2))
    Model.add(LSTM(units = 50))

    Model.add(Dense(units = 1))
    Model.compile(optimizer = 'adam', loss = 'mean_squared_error')
    Model.fit(X_train, y_train, epochs = 4, batch_size = 32,verbose=2)

    inputs = dataset_train['data.Close'].values
    inputs = inputs.reshape(-1,1)
    inputs = sc.transform(inputs)

    X_test = []
    X_test.append(inputs[inputs.shape[0]-1-time_step:inputs.shape[0]-1, 0])

    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_price = Model.predict(X_test)
    predicted_price = sc.inverse_transform(predicted_price)

    plt.figure(figsize=(20,10))
    plt.title('Stock Price Prediction --price:'+str(predicted_price))
    x1 = range(len(dataset_train))
    y1 = training_set
    plt.plot(x1,y1,color='black',label = 'Stock Price')
    x2 = len(dataset_train)
    y2 = predicted_price
    plt.scatter(x2,y2,color='blue',label = 'Predicted Stock Price')

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(200))
    plt.gcf().autofmt_xdate()# 自动旋转日期标记
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

    return (str(predicted_price))
