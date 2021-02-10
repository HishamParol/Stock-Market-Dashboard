import json
import os
import boto3
import csv
import random 
import statistics
from functions import varcal
from functions import index
from functions import subset
from collections import deque
from functions import ret
from functions import stringtofloat
from functions import get_key
import pickle
from functions import tos3

def lambda_handler(event, context):
    jsondata = (event['key5'])
 
    jsonlist=jsondata.split(",")
    startDate=jsonlist[4]
    jsonfloat = stringtofloat(jsonlist[:4])
    window=jsonfloat[0]
    window=int(window)
    SA=jsonfloat[1]
    SA=int(SA)
    CF=jsonfloat[3]
    CF=int(CF)
    which_data = jsonfloat[2]
    which_data=int(which_data)
    
    key=get_key(which_data)
   
    bucket = 'courseworkhisham'
    s3_resource = boto3.resource('s3')
    s3_object = s3_resource.Object(bucket, key)

   
    adjclose = []
    date = []
    data = s3_object.get()['Body'].read().decode('utf-8').splitlines()
    
    #endDate=varcal(startDate,window)
    
    
    for i in range(len(data)):
        x=data[i].split(',')
        y=x[5]
        z=x[0]
        adjclose.append(y)
        date.append(z)
    
    startindex1= index(startDate,date)
    endindex = startindex1 - (window+1)
    if endindex<0:
        transfer=[0,0,0,0,0,0]
    else:
        newdata = subset(data,startindex1,endindex)
        a = deque([newdata])
        b=a.rotate(2)
        #rets_1 = (newdata/newdata.shift(1))-1
        s = [newdata[-1]]+newdata[:-1]
        s[0]=0
        u = s[1]
        #ret = (newdata/s)-1
        endDate=date[endindex]
        
        x2=data[startindex1].split(',')
        price=round(float(x2[5]),2)
        con=stringtofloat(newdata)
        con2 = stringtofloat(s)
        
       
        y= ret(con,con2)
        y.pop(0)
        sigma=statistics.stdev(y)
        mu=statistics.mean(y)
        
       
        transfer=[mu,sigma,price,window]
        
        sale=sum(y)
        
        random_value=random.gauss(mu, sigma)
        
        
        new_series=[]
        
        for i in range(SA):
             random_value=random.gauss(mu, sigma)
             #newprice=(1+random_value)*float(price)
             new_series.append(random_value)
        
        new_series.sort(reverse=True)
        var=new_series[CF]
        var95=new_series[95]
        var99=new_series[99]
        average_var=(var95+var99)/2
        var=round(var,4)
  
        transfer=[var,var95,var99,average_var,startDate,which_data]
        #Storing results to s3
        tos3(var,var95,var99,average_var,SA)
    
    return transfer

