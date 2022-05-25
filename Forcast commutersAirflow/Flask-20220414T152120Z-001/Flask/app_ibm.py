import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
#import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "MzXQpiZerFG8QjlceAXxVzaTYOPCpcnl9b11_iiRWOuJ"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)
#model = pickle.load(open('airpassengers.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def y_predict():
    if request.method == "POST":
        ds = request.form["Date"]
        print(ds)
        print(type(ds))
        a={"ds":[ds]}
        #print(a)
        ds=pd.DataFrame(a)
        #prediction = model.predict(ds)
        #print(prediction)
        #output=round(prediction.iloc[0,15])
        #print(ds)
        ds['year'] = pd.DatetimeIndex(ds['ds']).year
        ds['month'] = pd.DatetimeIndex(ds['ds']).month
        ds['day'] = pd.DatetimeIndex(ds['ds']).day
        #print(ds)
        year= ds['year']
        #print(year)
        y=year.values.tolist()
        #print(y[0])
        month= ds['month']
        #print(month)
        m=month.values.tolist()
        #print(m[0])
        
        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": [["year", "month"]], "values": [[y[0],m[0]]]}]}

        response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/173b7d08-7851-4204-9cec-2732559c0764/predictions?version=2022-03-31', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        pred= response_scoring.json()
        print(pred)
        output= pred['predictions'][0]['values'][0][0]
        print(output)
        return render_template('home.html',prediction_text="Commuters Inflow on selected date is. {} thousands".format(output))
    return render_template("home.html")
    
if __name__ == "__main__":
    app.run(debug=False)