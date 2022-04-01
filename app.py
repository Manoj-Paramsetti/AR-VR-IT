from email.policy import default
from flask import (
    Flask,
    render_template,
    request,
    redirect
)
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///registedstudents.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        new_student = Register(name = name, email = email, phone = phone)

        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect('/registered')
        except:
            return redirect('/error')


    else:
        datas=Register.query.order_by(Register.date)
        print(datas)
    return render_template('index.html')

@app.route('/dashboard')
def display():
    datas=Register.query.order_by(Register.date)
    print(datas)
    return render_template('dashboard.html', datas = datas)

@app.route('/registered')
def registered():
    return render_template('registered.html')

@app.route('/error')
def error():
    return render_template('error.html')