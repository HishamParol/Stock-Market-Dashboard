#functons are defined here
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import http.client
import requests
import time
import queue
import threading
import boto3
import json

def plotgraph(file):
    fig=plt.figure(figsize=[15,10])
    plt.grid(True)
    fig.suptitle('Moving average for window size:')
    plt.plot(file['Adj Close'],label='Price')
    plt.legend(loc=2)
    plt.xlabel('Number of Days')
    plt.ylabel('Price')
    plt.savefig(b)

def moving_avg(data,window):
    #Initialize signals Dataframe 
    signals = pd.DataFrame(index=data.index)
    signals['Date'] = data['Date']
    signals['Signal'] = 0.0
    signals['Close'] = data['Close']

    # Create a moving average over the window
    signals['Moving_avg'] = data['Close'].rolling(window=window).mean()
    signals['Volume'] = data['Volume']

    # Create signals
    signals['Signal'][:] = np.where(signals['Close'][:] 
                                            > signals['Moving_avg'][:], 1.0, 0.0)  
  
    # Generate trading orders
    signals['Positions'] = signals['Signal'].diff()
    signals['Profit/Loss']=signals['Close']*signals['Positions']*100
    signals['Cumulative Profit/Loss']=signals['Profit/Loss'].cumsum()

    return signals

def create_button(data):
    #Define a new column Buy/Sell to create Buy/Sell button
    data=data.reset_index(drop=True)
    for idx in range(0,len(data)):
        if data['Positions'].iloc[idx] == 1.0:
            data['Buy/Sell'].iloc[idx]='<button id="{}" type = "button" class="w3-button w3-teal" onClick="myFunction(this.id)">Buy</button>'.format(idx)
            
        elif data['Positions'].iloc[idx] == -1.0:
            data['Buy/Sell'].iloc[idx]='<button id="{}" type = "button" class="w3-button w3-red" onClick="myFunction(this.id)">Sell</button>'.format(idx)
        else: 
            data['Buy/Sell'].iloc[idx]= '--'

    return data

def call_lambda(v):
    c = http.client.HTTPSConnection("6lt6d4uus5.execute-api.eu-west-2.amazonaws.com") #Enter your Amazon lambda VaR CALCULATION API here
    json= '{ "key5":"'+v+'"}'
    c.request("POST", "/default/varcalculation", json)
    response = c.getresponse()
    data2 = response.read()
    data2=data2.decode("utf-8")
    data2=data2[1:-1]
    data2=data2.split(",")
    
    return data2

def call_ec2(DNS):
    r = requests.get(DNS,verify=False)
    result=[r.text]
    return result

def start_stop(v):
    c = http.client.HTTPSConnection("prh7qrnqye.execute-api.eu-west-2.amazonaws.com") #Enter your Amazon lambda startstop API here 
    v=str(v)
    json= '{ "key1":"'+v+'"}'
    c.request("POST", "/default/start_stop123", json)
    response = c.getresponse()
    data2 = response.read()
    data2=data2.decode("utf-8")
    return data2
    
def get_data(V):
#ENTER YOUR S3 BUCKET LINK TO FETCH DATA 
    if V==1:
        data='https://courseworkhisham.s3.eu-west-2.amazonaws.com/AMZN.csv'
        tag=1
        name='AMAZON FINANCE DATA'
    elif V==2:
        tag=2
        data='https://courseworkhisham.s3.eu-west-2.amazonaws.com/AAPL.csv'
        name='APPLE FINANCE DATA'
    elif V==3:
        tag=3
        data='https://courseworkhisham.s3.eu-west-2.amazonaws.com/BABA.csv'
        name='ALI BABA FINANCE DATA'
    elif V==4:
        tag=4
        data='https://courseworkhisham.s3.eu-west-2.amazonaws.com/BIT.csv'
        name='BITCOIN FINANCE DATA'
   
    AMZN = pd.read_csv(data)
    AMZN = AMZN.rename(columns = {'Adj Close':'Adj'})
    return AMZN,tag,name

def encode_date(date):
    dd, mm, yyyy = date.split('/')
    return (yyyy+'-'+mm+'-'+dd)

def encode_date1(date):
    dd, mm, yyyy = date.split('/')
    return (dd+'-'+mm+'-'+yyyy)

def tos3(name,VaR,v95,v99,Profit,simulations):
    store_data= {"Name":name,"VaR":VaR,"Var95":v95,"VaR99":v99,"Profit":Profit,"Simulations":simulations}
    s3=boto3.resource('s3')
    key = "results.csv"
    bucket_name='courseworkhisham'
    s3.Bucket(bucket_name).put_object(Key=key,Body=json.dumps(store_data).encode())




    
