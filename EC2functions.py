from datetime import date,timedelta,datetime
import boto3
import json

def varcal(date,window):
    startdate=date
    startdate_object = datetime.strptime(date, '%d/%m/%Y')
    enddate1 = startdate_object - timedelta(window)
    enddate=enddate1.strftime('%d/%m/%Y')
    print(enddate)
    return enddate
  
def index(vdate,date):
    for i in range(len(date)):
        if date[i]==vdate:
            index = i
            break
    return i    

def subset(data,startindex,endindex):
    close = []
    for i in range(endindex,startindex):
        x1=data[i].split(',')
        y1=x1[5]
        close.append(y1)
            
    return close 
    
def ret(data1,data2):
    retn=[]
    for i in range(len(data1)):
        r=(data2[i]/data1[i])-1
        retn.append(r)
        
    return retn
    
def stringtofloat(data):
    convertdata=[]
    for item in data:
        sf=float(item)
        convertdata.append(sf)
        
    return convertdata

def get_key(which_data):
    if which_data==1:
        key='AMZN.csv'
    elif which_data==2:
        key='AAPL.csv'
    elif which_data==3:
        key='BABA.csv'
    elif which_data==4:
        key='BIT.csv'
    
    return key
    
def tos3(var,var95,var99,average_var,SA):
    store_data= {"VaR":var,"Var95":var95,"VaR99":var99,"Average_Var":average_var,"Simulations":SA}
    s3=boto3.resource('s3')
    key = "results.csv"
    bucket_name='your s3 bucket name'
    s3.Bucket(bucket_name).put_object(Key=key,Body=json.dumps(store_data).encode())

