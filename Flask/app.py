import random

from flask import Flask, request, render_template
from joblib import load

app = Flask(__name__)

minmaxScaler = load('MinMax.sav')
model = load('engine_model.sav')


@app.route('/m_predict')
def predict():
    return render_template('Manual_predict.html')


@app.route('/s_predict')
def spredict():
    return render_template('Sensor_predict.html')


@app.route('/y_predict', methods=['GET', 'POST'])
def y_predict():
    tmplist = [[int(x) for x in request.form.values()]]
    listforscale = [[tmplist[0][2], tmplist[0][3], tmplist[0][4], tmplist[0][5], tmplist[0][6], tmplist[0][7],
                     tmplist[0][8], tmplist[0][9], tmplist[0][10], tmplist[0][11], tmplist[0][12], tmplist[0][13],
                     tmplist[0][14], tmplist[0][15], tmplist[0][16], tmplist[0][17], tmplist[0][18], tmplist[0][19],
                     tmplist[0][20], tmplist[0][21], tmplist[0][22], tmplist[0][23], tmplist[0][24], tmplist[0][25]]]
    scaled = minmaxScaler.transform(listforscale)
    x_test = [[tmplist[0][0], tmplist[0][1], scaled[0][0], scaled[0][1], scaled[0][2], scaled[0][3], scaled[0][4],
               scaled[0][5], scaled[0][6], scaled[0][7], scaled[0][8], scaled[0][9], scaled[0][10], scaled[0][11],
               scaled[0][12], scaled[0][13], scaled[0][14], scaled[0][15], scaled[0][16], scaled[0][17], scaled[0][18],
               scaled[0][19], scaled[0][20], scaled[0][21], scaled[0][22], scaled[0][23], tmplist[0][26]]]
    print(x_test)
    a = model.predict(x_test)
    pred = a[0]
    if pred == 0:
        pred = "No failure expected within 30 days."
    else:
        pred = "Maintenance Required!! Expected a failure within 30 days."
    # print(request.form.values()[0][2])
    return render_template('Manual_predict.html', prediction_text=pred)


@app.route('/sy_predict', methods=['GET', 'POST'])
def sy_predict():
    inp1 = []
    inp1.append(random.randint(0, 100))  # id
    inp1.append(random.randint(0, 365))  # cycle
    for i in range(0, 24):
        inp1.append(random.uniform(0, 1))
    inp1.append(random.randint(0, 365))  # ttf
    pred = model.predict([inp1])
    if (pred == 0):
        pred = "No failure expected within 30 days."
    else:
        pred = "Maintenance Required!! Expected a failure within 30 days."
    return render_template('Sensor_predict.html', prediction_text=pred, data=inp1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
