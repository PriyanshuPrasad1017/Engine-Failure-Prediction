import requests
import json

API_KEY = "zT1z5T6S4CG9SN6369lVbajORLf64sDZnN2TSMFLdxRt"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token',
                               data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {
    "input_data": [{"field": [['id', 'cycle', 'setting1', 'setting2', 'setting3', 's1', 's2', 's3', 's4', 's5',
                               's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 's17', 's18',
                               's19', 's20', 's21', 'Trajectory']],

                    "values": [[1.00000000e+00, 1.00000000e+00, 4.59770115e-01, 1.66666667e-01,
                                0.00000000e+00, 0.00000000e+00, 1.83734940e-01, 4.06801831e-01,
                                3.09756921e-01, 0.00000000e+00, 1.00000000e+00, 7.26247987e-01,
                                2.42424242e-01, 1.09755003e-01, 0.00000000e+00, 3.69047619e-01,
                                6.33262260e-01, 2.05882353e-01, 1.99607803e-01, 3.63986149e-01,
                                0.00000000e+00, 3.33333333e-01, 0.00000000e+00, 0.00000000e+00,
                                7.13178295e-01, 7.24661696e-01, 1.91000000e+02]]}]}

response_scoring = requests.post(
    'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/b13b7c15-73c1-42b1-916d-78f9dfe297d8/predictions?version=2021-08-04',
    json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
predictions = response_scoring.json()
result = (predictions['predictions'][0]['values'][0][0])
if result == 0:
    print("No Failure expected within next 30 Cycles")
else:
    print("Maintenance Required!! Expected a failure within 30 cycles.")
