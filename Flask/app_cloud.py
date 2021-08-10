import random
import requests

from flask import Flask, request, render_template
from joblib import load

API_KEY = "zT1z5T6S4CG9SN6369lVbajORLf64sDZnN2TSMFLdxRt"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token',
                               data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app_cloud = Flask(__name__)

minmaxScaler = load('MinMax.sav')
model = load('engine_model.sav')


@app_cloud.route('/m_predict')
def predict():
    return render_template('Manual_predict.html')


@app_cloud.route('/s_predict')
def spredict():
    return render_template('Sensor_predict.html')


@app_cloud.route('/y_predict', methods=['GET', 'POST'])
def y_predict():
    x_test = [[int(x) for x in request.form.values()]]

    print(x_test)

    payload_scoring = {
        "input_data": [{"field": [['id', 'cycle', 'setting1', 'setting2', 'setting3', 's1', 's2', 's3', 's4', 's5',
                                   's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 's17',
                                   's18',
                                   's19', 's20', 's21', 'Trajectory']],

                        "values": x_test}]}

    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/b13b7c15-73c1-42b1-916d-78f9dfe297d8/predictions?version=2021-08-04',
        json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

    predictions = response_scoring.json()
    result = (predictions['predictions'][0]['values'][0][0])

    if result == 0:
        pred = "No failure expected within 30 days."
    else:
        pred = "Maintenance Required!! Expected a failure within 30 days."

    return render_template('Manual_predict.html', prediction_text=pred)


@app_cloud.route('/sy_predict', methods=['GET', 'POST'])
def sy_predict():
    inp1 = []
    inp1.append(random.randint(0, 100))  # id
    inp1.append(random.randint(0, 365))  # cycle
    for i in range(0, 24):
        inp1.append(random.uniform(0, 1))
    inp1.append(random.randint(0, 365))  # ttf
    inp = [inp1]
    payload_scoring = {
        "input_data": [{"field": [['id', 'cycle', 'setting1', 'setting2', 'setting3', 's1', 's2', 's3', 's4', 's5',
                                   's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 's17',
                                   's18',
                                   's19', 's20', 's21', 'Trajectory']],

                        "values": inp}]}
    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/b13b7c15-73c1-42b1-916d-78f9dfe297d8/predictions?version=2021-08-04',
        json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

    predictions = response_scoring.json()
    result = (predictions['predictions'][0]['values'][0][0])

    if result == 0:
        pred = "No failure expected within 30 days."
    else:
        pred = "Maintenance Required!! Expected a failure within 30 days."

    return render_template('Sensor_predict.html', prediction_text=pred, data=inp1)


if __name__ == '__main__':
    app_cloud.run(host='0.0.0.0', debug=True)
