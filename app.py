import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy


UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1/registry'
db = SQLAlchemy(app)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    count = db.Column(db.Integer, nullable=False)


def parse_csv(path):
    csv_data = pd.read_csv(path)

    for _,row in csv_data.iterrows():
        transaction = Transaction(time=row['time'], status=row['status'], count=row['count'])
        db.session.add(transaction)
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def add_transaction():
    db.create_all()
    uploaded_file = request.files['file']

    if uploaded_file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        parse_csv(file_path)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
