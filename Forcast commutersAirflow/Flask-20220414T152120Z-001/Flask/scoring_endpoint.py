# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 12:29:37 2022

@author: Dell
"""

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "MzXQpiZerFG8QjlceAXxVzaTYOPCpcnl9b11_iiRWOuJ"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": [["year", "month"]], "values": [[2000,11]]}]}
response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/173b7d08-7851-4204-9cec-2732559c0764/predictions?version=2022-03-31', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())
pred= response_scoring.json()
print(pred)
output= pred['predictions'][0]['values'][0][0]
print(output)