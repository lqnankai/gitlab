'''
Created on 2016.8.30

@author: liangqian
'''
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.engine.training import Model

def readData():
    x_train = []
    y_train = []
    f = open('data.txt')
    while(True):
        line = f.readline()
        if(len(line) == 0):break
        else:
            strs = line.split(':')
            y_train.append(int(strs[0]))
            data = strs[1].split(',')
            x_train.append(data)
            
    print(x_train.shape)        
        

def buildingModel():
    model = Sequential()
    layers = [1,50,100,1]
    model.add(LSTM(input_dim=layers[0],output_dim=layers[1],return_sequences = True))
    model.add(Dropout(0.2))
    
    model.add(LSTM(layers[2],return_sequences=False))
    model.add(Dropout(0.2))
    
    model.add(Dense(output_dim=layers[3]))
    model.add(Activation("linear"))
    
    model.compile(loss="mse", optimizer="rmsprop")
    return Model

readData()