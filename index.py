#Import libraries
import os
import logging
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from matplotlib import style
from flask import Flask, request, render_template,redirect
import ast
from scipy import stats
import scipy as sp
from pandas import DataFrame
import seaborn as sns
import json
import queue
import threading
import multiprocessing
import time

from functions import plotgraph
from functions import moving_avg
from functions import create_button
from datetime import datetime
from functions import call_lambda
from functions import call_ec2
from functions import get_data
from functions import tos3
from functions import encode_date



app = Flask(__name__)


    

def doRender(tname, values={}):
	if not os.path.isfile( os.path.join(os.getcwd(), 'templates/'+tname) ): 
		return render_template('index.htm')
	return render_template(tname, **values) 



@app.route('/graph', methods=['GET','POST'])

def calculate():
    #moving average window
    size= request.form.get('key1')
    size=int(size)

    #Choose data
    V= request.form.get('data') 
    V=int(V)
    DATA,tag,name=get_data(V)
    
    #Calculate Moving Average and generate signals
    signals=moving_avg(DATA,size)
    signals=signals[size:]
    signals['Buy/Sell'] = 0
    signals = create_button(signals)
   
    #Date conversion and processing for plotjs
    label1=[]
   
    for ind in range(0,len(signals)):
        row=[]
        date_row=signals['Date'].iloc[ind]
        date_row1=encode_date(date_row)
        row.append(date_row1)
        moving=float(signals["Moving_avg"].iloc[ind])
        row.append(moving)
        price=float(signals["Close"].iloc[ind])
        row.append(price)
        label1.append(row)
    
    headers=["Date","Price","Moving_avg"]
    dataframe=pd.DataFrame(label1, columns=headers)

    #Define dictionary for plotting Graph
    buydic={"Signal":dataframe.Price.to_list(),"Moving_Avg":dataframe.Moving_avg.to_list(),"labels":dataframe.Date.to_list()}

    #Return for table data,Graph and tag
    return render_template('graph.html',posts=[signals.to_html(classes='data',escape=False)],titles=signals.columns.values,dictionary=buydic,which_data=tag,window_size=size)


@app.route('/results', methods=['POST'])
def RandomHandler():
    import http.client
    if request.method == 'POST':
        
        #Get form details
        W= request.form.get('key4') #Window
        S= request.form.get('key5') #Simulations
        R= request.form.get('key6') #R
        k4= request.form.get('key7') #Date
        CF= request.form.get('key8') #Confidence Interval
        ec2= request.form.get('ec2') #EC2 Clicked?
        lmd= request.form.get('lambda') #Lambda clicked?
        ind=int(k4)
        simulations=int(S)
        R=int(R)
        count=round(simulations/R) #No of run in single api call

        #Chosen Data windowsize
        which_data= request.form.get('dataidentifier')
        size= request.form.get('windowsize') 
        size=int(size) 
      
        V=int(which_data)
        DATA,tag,name=get_data(V)
      
        #Get Date
        signals=moving_avg(DATA,size)
        signals=signals[size:]
        signals['Buy/Sell'] = 0
        signals = create_button(signals)
        Datenew=signals['Date'].iloc[ind]
        Profit=signals['Profit/Loss'].iloc[ind]
        Cumulative =signals['Cumulative Profit/Loss'].iloc[ind]
        Cumulative=round(Cumulative,4)
        if (Profit<0):
            trade='SELL'
        else:
            trade='BUY'
       
        v=str(W)+","+str(count)+","+str(V)+","+str(CF)+","+Datenew

        #redirecting to different Services

        #This is Amazon EC2 Cloud
        #Enable EC2 Button from graph.html in templates folder
        if ec2 is not None:
            #START THE SERVICE
            start_stop(1)
            #Get Public DNS
            DNS="ENTER YOUR EC2 PUBLIC DNS.amazonaws.com/?Window={}&Count={}&Data={}&CF={}&Date={}".format(W,count,V,CF,Datenew)
            
            start = time.time()
            #Multi threading process
            pool = multiprocessing.Pool(processes = R)
            arguments=[]
            for i in range(R):
                arguments.append(DNS)
            LIST=pool.map(call_ec2,arguments)
            tt=time.time() - start
            tt=float(tt)
            #STOP THE SERVICE
            start_stop(2)
             
        #This is AMAZON Lambda Cloud
        elif lmd is not None:
            start = time.time()
            #Multi threading process
            pool = multiprocessing.Pool(processes = R)
            arguments=[]
            for i in range(R):
                arguments.append(v)
            LIST=pool.map(call_lambda,arguments)
            tt=time.time() - start
            tt=float(tt)
            print(LIST)
        #Processing received data
        columns=['VaR','VaR95','VaR99','Average_Var','Date','Data']
        LIST=pd.DataFrame(LIST,columns=columns)
        mov=LIST["VaR"]
        summ=0
        for u in range(len(mov)):
            y=mov[0]
            y=float(y)
            summ=summ+y
        VaR=summ/R
        VaR=round(VaR,4)
        v95=LIST['VaR95'].values[0]
        v99=LIST['VaR99'].values[0]
        Average_Var=LIST['Average_Var'].values[0]
        Date=LIST['Date'].values[0]
        Data=LIST['Data'].values[0]
        v95=v95[0:7]
        v99=v99[0:7]
        Average_Var=Average_Var[0:7]
        
        #Error handling
        #If the user selects window size > dates available
        error=''
        if VaR==0:
            trade='N/A'
            VaR='N/A'
            v95='N/A'
            v99='N/A'
            Profit='N/A'
            Average_Var='N/A'
            error="SELECT A DIFFERENT WINDOW SIZE"

        #Store the results in S3
        #tos3(name,VaR,v95,v99,Profit,simulations)
            
        return render_template('results.html',trade=trade,error=error,name=name,R=R,VaR=VaR,v95=v95,v99=v99,Average_Var=Average_Var,Date=Date,Data=Data,Datenew=Datenew,Profit=Profit,Cumulative=Cumulative,V=V,tt=tt)

#*********************************************************************************************************************************************

@app.route('/', defaults={'path': ''})

@app.route('/<path:path>')

def mainPage(path):

   return doRender(path)


@app.errorhandler(500)



def server_error(e):

   logging.exception('ERROR!')

   return """

An error occurred: <pre>{}</pre>

""".format(e), 500


if __name__ == '__main__':


   app.run(host='0.0.0.0',port=8081,debug=True)
