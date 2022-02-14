# Stock Market dashboard (Multi cloud flask app)
---

Design and development of Python Flask web application to calculate the Risk value for various Stock Markets and deployed in Multi-Cloud (Google App
Engine, AWS ec2, AWS lambda, s3).</br>

**Key Tools: Flask framework, Numpy, Plotly,boto3, AWS ec2, AWS Lambda, AWS S3 Storage, Google Cloud Platform**</br>
**Languages: Python, HTML, CSS, JavaScript**<br>

# How to run this project 
---
* Download project files to your local machine.
* Go to project directory in terminal. 
* Create an isolated Python environment and activate it:
    - virtualenv -p python3 “your environment name”
    - source “your environment name”/bin/activate
    
 * Run the requirements.txt file:
    - pip install -r requirements.txt
    
 * Run index.py file and project starts running on your localhost http://0.0.0.0:8081/
    - python index.py

# Introduction
---
Cloud Computing which is based on internet is the on-demand delivery of IT resources and powerful computations on the basis of pay as you go scheme. In this project, I have given a brief of exploring different cloud services in two powerful giants – Amazon Web Services (AWS) and Google Cloud Platform (GCP) to development a web application. This service helps user to calculate Value at Risk, profit/loss and other parameters for four different companies. The outcome of this 
project is to understand and utilize on-demand cloud services and compare the costs of scalable resources.
</br>
The term ‘Cloud’ which means collection of networks in computing world is a distributed, on-demand and convenient service that has easy access to IT resources at a reasonable 
cost. According to NIST SP Cloud computing is characterized as a profound economic and technical shift which has a great potential to reduce the cost of IT systems .Instead of setting up one’s own infrastructure, which adds money, the users have to pay for the services they had used. In this experiment I have hosted my web application on Google Cloud Platform that provides Platform as a Service (PaaS) ,Amazon S3, which is a scalable storage infrastructure to store data and Amazon Lambda and EC2 resources for computation processes. **This cloud system is compatible with the NIST’s service model – Software as a Service(SaaS), Platform as a Service( PaaS) and Infrastructure as a Service(IaaS).**

# Key development insights using cloud?
---
- Within the context of developer, The use of multi-threading and parallel processing has changed the area of development and helped to gain performance speeds and scalability. - With easy access to cloud servers has helped me to build and test instantly.
- Amazon Lambda, a serverless computing platform manages smaller applications with fast response along with Amazon S3, a cloud storage system helped the development process much easier just by an API call. 
- AWS Lambda’s Function as a Service (FaaS) model provides instant testing of the application at low cost.
- I deployed onto the cloud infrastructure using programming languages, libraries,services, and tools.
- Google’s Cloud Shell is used to write the program and deploy instantly.
- I do not manage or control the underlying cloud infrastructure including network, servers, operating systems, or storage, but has control over the deployed applications and possibly configuration settings for the application-hosting environment

# How can an end-user access this platform?
---
The applications are accessible from various web browsers. The overall service model is hidden from the user. User can easily access the service by opening a URL and can select the company to get its corresponding graph and values. All these processes are implemented in an interactive front end and user can select buttons to redirect the process. The variables selected by user are automatically passed to the results page to display an overall summary. </br>
**Please note: Currently the application running on GCP is shutdown to reduce the cost, However you can access in the local system. Process for complete deployment using your own account is available here**

# Architecture
---
![Architecture](https://github.com/HishamParol/Stock-Market-Dashboard/blob/master/static/Screenshot%202022-02-13%20220300.png)
## Major System Components

This web application is built to calculate the Value at Risk for different companies, namely – Amazon, Apple, Ali Baba and Bitcoin. The application is build using Python’s Flask framework. The main server is Google Cloud Platform (GCP) and other scalable resources such as Amazon Lambda and EC2 are used for scalability. Data is stored in Amazon’s S3 bucket. S3 is free to join and pay-as-you-go service and provides backup. It is fully scalable, fast and reliable. S3 is easily accessible from EC2 and Lambda using boto3 library. This helps to avoid transferring data from Google Cloud Platform to scalable resources and reducing the strain on the server hosting the website. Since the data is being accessed from different resources, there is no need to store data in every resource.
</br>
The main application is hosted on Google App Engine not only because of its low cost but also the reliable services and flexibility in working with any framework. Cloud shell and Google Colaboratory helps to debug scripts instantaneously in cloud platform without any need of installing libraries. 
</br>
- In the index page user can select the window size for calculating moving average and data. Once the data is selected, it is fetched from S3 and loaded to GCP.
- For the VaR calculation, user clicks buy or sell button and enter other parameters. 
- I have implemented an option to choose between lambda or EC2 and to select the number of parallel processes.
- After this, user input is sent to lambda or EC2 to calculate VaR.
- Both uses S3 to process data. 
- Amazon Lambda is a serverless computing system which provides Function as a Service (FaaS). Here the code is executed based on event trigger and can be called by an API.
- The principle benefit of serverless model is that we pay only for exactly what we use, and the unused server time doesn’t not add to the bill. 
- Lambda is quite useful for running low end functions. Automatic scalability accommodates multiple requests and is very useful for parallel processing. 
- Lambda is also used to automatically turn on and turn off EC2 instances to avoid cost.

</br>
Amazon Elastic Compute Cloud(ec2) is other optional resource for calculating VaR. It is a web-based service that allows applications to run programs. I have deployed python Flask script to calculate VaR in ec2 instance and this function is called from GCP. An ec2 instance is launched in AWS console and an AMI (Amazon Machine Image ) is created that 
contains Ubuntu operating system. Unlike Lambda, ec2 is server-based resource and provides flexibility options to host applications onto more than one platform. For higher computation requirements ec2 is a better option however to reduce the cost I have implemented auto start-stop instances using boto3 library. Since the instance take few secs to turn on it adds another extra time for computation. The calculated VaR values are stored back to S3 bucket.

## System Component interaction

- In the first page, which is hosted in GCP, user can select any company and the window size for calculating moving average. 
- Once the form is submitted, data is loaded from S3 to GCP. And then loaded to Plotly to plot timeseries graph The page renders to graph page, where I plotted a time series of Adjusted Close price and Moving average.
- The graph is plotted using Plotly – a JavaScript based library function for plotting charts and graphs. In the backend, with the help of moving average, Buy and Sell signals are generated. 
- Profit or Loss and Cumulative profit or loss are calculated using close price and signal signs.These values are shown in a HTML table with buttons enabled for each buy and sell signals.
- User can see and select any date corresponding to buy/sell signals from the table to calculate Value at Risk at that position.
- After clicking the buy or sell button a pop-up window is displayed. Here user can give input values for calculating VaR such as number of parallel resources, return series size, number of simulations and choice of scalable resources.
- Based on selected scalable resource, these input variables along with date are transferred to EC2 or Lambda through an API call.
- After reaching variables in these resources, it interacts with S3 to fetch data and calculate VaR in scalable resources.
- The returns variables include VaR, mean, standard deviation and Average Var. The results are shown in results page and the value of VaR is automatically stored in S3 bucket.

## Implementation
---
In this experiment, I have used S3 bucket to store the datasets. S3 provides flexibility in storing the data and thus reducing the cost. Moreover, it also helped me to reduce the data transmission volumes from GAE to Lambda or EC2. I considered using scalable resources for doing computational tasks such as calculating return values, VaR at 95th
, 99th percentile and total VaR.
</br>
In order to cut down the cost in ec2, I have implemented auto start and stop functionality for ec2 instances. This will reduce the idle run time and instances are started only once user selects ec2 resource to calculate VaR. Once it turns ON, function will check the status of state. And if the status is running, variables are passed to remote flask application running on ec2 Ubuntu server. The computations are done there and return values are sent back to GAE. 
</br>
After receiving the values, ec2 changes its status from running to stopped. This functionality is tested by logging into the AWS ec2 console and observing the instance status. However, ec2 takes around 10 secs to start, which delays the total computation time.The variables are transferred to EC2 server as URL arguments.
</br>
In the flask app, these parameters are read using flask’s request function. After completing the calculations, computed values are sent back to GCP. For the parallel processing, I have used python’s multithreading function, that sends the request to scalable resources simultaneously. The average VaR from R parallel resources are calculated. This value is updated in S3. The computation time is reduced significantly in this process. However, GCP requires more memory and GPU power to handle multiple requests in parallel operation. The total computation time taken to run parallel process is displayed in the results page.
</br>
The graph will display closing price and moving average over the time. User can slide through each section by selecting the range slider. In the table below the graph, user can select buy or sell buttons to calculate corresponding VaR. The date is automatically mapped by button ID. This date along with other user inputs are transferred to scalable resources. The date act as an index to identify corresponding price in Lambda or ec2. I have done testing to observe both prices are same in GCP and scalable resources as conflicts in date format may alter the results. All the user input fields in the form are set to mandatory as we require all values for calculation. 

## Results
---
Results are shown below for VaR at 95% and 99% confidence interval for Amazon Dataset. Different simulations and moving average size are selected to observe the change in VaR values. 
</br>
It is observed that the 95% confidence that the buyer or seller lose money increases as the monte-carlo simulations increase. Whereas slight change is only observed at 99%.
