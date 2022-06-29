#This app is for Customer Segmentation
#user have to provide details of the 1 customer at a time and then app will predict the cluster of that customer it belongs to
from flask import Flask ,render_template,request
from bs4 import BeautifulSoup
import pickle
import pandas as pd
import numpy as np
app = Flask(__name__)

#this is our logictic regression model trained after creating cluster using k-means method
lrmodel=pickle.load(open('cslrmodel.pkl','rb'))

#add various transactions details of customer
customeridList=[]
invoiceNoList=[]
dateList=[]
unitpriceList=[]
quantityList=[]

#this method will calculate the R,F and M of the data input 
#same code used in the jupyter notebook
def getRFM(df):
    df['TotalSum']=df.Quantity*df.UnitPrice
    compare_date=pd.to_datetime('2012/12/10')
    customerdf=df.groupby(['CustomerID']).agg({'InvoiceDate':lambda x: (compare_date-x.max()).days,
'InvoiceNo':'count','TotalSum':'sum'})
    customerdf.rename(columns = {'InvoiceDate': 'Recency','InvoiceNo': 'Frequency',
                            'TotalSum': 'MonetaryValue'}, inplace=True)
    return customerdf

@app.route("/",methods=['GET','POST'])
def home_page():
    #get all the inputs and add into the lists after data type changes
    if request.method=='POST':
        invoiceNo=request.form['Invoice']
        date=request.form['Date']
        customerid=request.form['Customer']
        unitprice=request.form['UP']
        quantity=request.form['Quantity']
        date=pd.to_datetime(date)
        customerid=int(customerid)
        unitprice=float(unitprice)
        quantity=float(quantity)        
        customeridList.append(customerid)
        invoiceNoList.append(invoiceNo)
        dateList.append(date)
        unitpriceList.append(unitprice)
        quantityList.append(quantity)
        
    return render_template('index.html')

@app.route("/prediction",methods=['GET','POST'])
def prediction_page():
    #create dataframe from the above lists created and get the rfm dataframe from it
    df=pd.DataFrame({
        'InvoiceDate':dateList,'Quantity':quantityList,'UnitPrice':unitpriceList,'CustomerID':customeridList,'InvoiceNo':invoiceNoList
    })
    customerdf=getRFM(df)
    customers_logT=customerdf.copy()
    #getting log tranformation matrix since model is trained on this only
    customers_logT.Recency=np.log(customerdf.Recency)
    customers_logT.Frequency=np.log(customerdf.Frequency)
    customers_logT.MonetaryValue=np.log(customerdf.MonetaryValue)
    prediction=lrmodel.predict(customers_logT)
    #based on prediction getting the type of the customer
    prediction=prediction[0]
    ctype=''
    if prediction==0:
        ctype='Loyal Customer'
    elif prediction==1:
        ctype='Churn Customer'
    elif prediction==2:
        ctype='New Customer'
    # clearing all the list so that new user input can be added
    customeridList.clear()
    invoiceNoList.clear()
    dateList.clear()
    unitpriceList.clear()
    quantityList.clear()
    return render_template('prediction.html',prediction=prediction,ctype=ctype)

if __name__=="__main__":
    app.run(debug=True)


