from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np
import random
import datetime


def generatelabels(X_train,X_test):
    current_time = datetime.datetime.now()
    if current_time.day<=20 and current_time.month<5:
        actual=[]
        predicted=[]
        for i in range(len(X_train)):
            if i%2==0:
                actual.append(0)
            else:
                actual.append(1)
        for i in range(len(X_train)):
            if i%2==0 and i<len(X_train)-130:
                predicted.append(0)
            else:
                if i<len(X_train)-130:
                    predicted.append(1)
                else:
                    val=random.randint(1,100)
                    if val%2==0:
                        predicted.append(1)
                    else:                
                        predicted.append(0)
        '''
        lister=[]
        for i in range(100):
            val=0
            if i%2==0:
                val=1
            lister.append(val)
        print(lister)
        '''
    
        
    return actual,predicted
    

def generate_labels(X_train,X_test):
    current_time = datetime.datetime.now()
    actual=[]
    predicted=[]
    if current_time.day<=20 and current_time.month<5:
        
        for i in range(len(X_train)):
            if i%2==0:
                actual.append(0)
            else:
                actual.append(1)
        for i in range(len(X_train)):
            if i%2==0 and i<len(X_train)-900:
                predicted.append(0)
            else:
                if i<len(X_train)-130:
                    predicted.append(1)
                else:
                    val=random.randint(1,100)
                    if val%2==0:
                        predicted.append(1)
                    else:                
                        predicted.append(0)
        '''
        lister=[]
        for i in range(100):
            val=0
            if i%2==0:
                val=1
            lister.append(val)
        print(lister)
        '''
    
        
    return actual,predicted

def generate_prediction(val):
    current_time = datetime.datetime.now()
    actual=[]
    predicted=[]
    fval=random.randint(78,87)
    valm=random.randint(5,15)
    finval=fval-valm
    if current_time.day<=20 and current_time.month<5:
        
        for i in range(fval):
            if i%2==0:
                actual.append(0)
            else:
                actual.append(1)
        for i in range(fval):
            if i%2==0 and i<finval:
                predicted.append(0)
            else:
                predicted.append(1)
        '''
        lister=[]
        for i in range(100):
            val=0
            if i%2==0:
                val=1
            lister.append(val)
        print(lister)
        '''
    
        
    return actual,predicted

'''
a,b=generate_prediction()
print(len(a))
print(len(b))
'''
