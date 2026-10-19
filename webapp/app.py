from flask import Flask, render_template, request, redirect, url_for
import pickle
import requests
import os

app = Flask(__name__)
DB_SERVICE_URL = 'http://p5dbapp:8001/add_records'
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        sepal_length = float(request.form['sepal_length'])
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        model_pred=model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
        if model_pred==0:
            prediction = "Iris-Setosa"
        elif model_pred==1:
            prediction = "Iris-Versicolor"
        elif model_pred==2:
            prediction = "Iris-Virginica"

        requests.post(url=DB_SERVICE_URL, json={"sepal_length": sepal_length, "sepal_width": sepal_width, "petal_length": petal_length, "petal_width": petal_width, "prediction": prediction})

        return render_template('predict.html', prediction=prediction)
    else:       
        return "Welcome"

@app.route('/records', methods=['GET'])
def get_records():
    records = requests.get('http://p5dbapp:8001/records')
    return render_template('records.html', records=records.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)