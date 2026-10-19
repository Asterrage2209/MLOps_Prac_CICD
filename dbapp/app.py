from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'pred.db')
db_path = db_path.replace('\\', '/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

db=SQLAlchemy(app)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sepal_length = db.Column(db.Float)
    sepal_width = db.Column(db.Float)
    petal_length = db.Column(db.Float)
    petal_width = db.Column(db.Float)
    prediction = db.Column(db.String(50))

@app.route('/add_records', methods=['POST'])
def add_records():
    record=request.get_json()
    record = Prediction (**record)
    db.session.add(record)
    db.session.commit()
    return jsonify({"message": "Record added successfully"}), 201

@app.route('/records', methods=['GET'])
def get_records():
    records = Prediction.query.all()
    result = []
    for record in records:
        result.append({
            'id': record.id,
            'sepal_length': record.sepal_length,
            'sepal_width': record.sepal_width,
            'petal_length': record.petal_length,
            'petal_width': record.petal_width,
            'prediction': record.prediction
        })
    return jsonify(result), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8001,debug=True)