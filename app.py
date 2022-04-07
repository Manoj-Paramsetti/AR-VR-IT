from os import urandom
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha1
from validate_email_address import validate_email

from datetime import datetime
app = Flask(__name__)
app.secret_key=urandom(50)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///registeredStudents.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Register(db.Model):
    __tablename__="registers"

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    email=db.Column(db.String, nullable=False, unique=True)
    phone=db.Column(db.Integer, nullable=False)
    city=db.Column(db.String, nullable=False)
    qualification=db.Column(db.String, nullable=False)
    date=db.Column(db.DateTime, default=datetime.utcnow)
    remark=db.Column(db.String, nullable=False, default="")
    phoneVerified=db.Column(db.Boolean, nullable=False, default=False)

class User(db.Model):
    __tablename__="users"

    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String, nullable=False, unique=True)
    password_hash=db.Column(db.String, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email'].lower()
        phone=request.form['phone']
        city=request.form['city']
        qualification=request.form['qualification']
        if name.strip()=="" or email.strip()=="" or email.strip()=="" or city.strip()=="" or qualification=="":
            return render_template("home.html", "All fields are required!")
        if Register.query.filter_by(email=email).first()!=None:
            return render_template('home.html', error="Email address is already used.")
        new_student = Register(name = name, email = email, phone = phone, city=city, qualification=qualification)
        if validate_email(email):
            if phone.isdigit() and len(phone)==10:
                try:
                    db.session.add(new_student)
                    db.session.commit()
                    return redirect('/registered')
                except Exception as err:
                    return redirect('/error/{}'.format(str(err)))
            else:
                return render_template('home.html', error="Not a valid phone number. Must have only 10 digits!")
        else:
            return render_template('home.html', error="Invalid email address.")
    return render_template('home.html')

@app.route('/dashboard/login', methods=["GET", "POST"])
def dashboard_login():
    if request.method=="POST":
        username=request.form['username']
        passwd=request.form['passwd']
        try:
            user=User.query.filter(User.username==username.strip()).one()
        except:
            return render_template("dash_login.html", error="Invalid Username")
        if user.password_hash==sha1(passwd.encode()).hexdigest():
            session['user']=user.username
            session['userid']=user.id
            session['appsecret']=app.secret_key
            return redirect('/dashboard')
        else:
            return render_template("dash_login.html", error="Invalid Credentials")
    else:
        if session.get("appsecret")!=app.secret_key:
            return render_template('dash_login.html', error=None)
        else:
            return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if session.get("appsecret")!=app.secret_key:
        return redirect('/dashboard/login')
    datas=Register.query.order_by(Register.date)
    return render_template('dashboard.html', datas=datas)

@app.route("/dashboard/users/new", methods=['POST', 'GET'])
def dashboard_new_user():
    if session.get("appsecret")!=app.secret_key:
        return redirect('/dashboard/login')
    if request.method=='POST':
        username=request.form['username']
        password=request.form['passwd']
        confirmpassword=request.form['confirmpasswd']
        if password!=confirmpassword:
            return render_template('newuser.html', message="Passwords don't match!")
        try:
            user=User.query.filter(User.username==username.strip()).one()
            return render_template('newuser.html', message="Username already exists!")
        except:
            pass
        user=User(username=username, password_hash=sha1(password.encode()).hexdigest())
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as err:
            return render_template("newuser.html", error=str(err))
        return render_template('newuser.html', message="User {} created successfully!".format(username))
    return render_template('newuser.html', message=None)

@app.route('/dashboard/users')
def dashboard_view_all_users():
    if session.get("appsecret")!=app.secret_key:
        return redirect('/dashboard/login')
    users=User.query.order_by(User.id)
    return render_template("allusers.html", users=users)

@app.route("/dashboard/entry/delete/<id>", methods=["POST"])
def dashboard_delete_entry(id: int):
    if session.get("appsecret")!=app.secret_key:
        return redirect('/dashboard/login')
    entry=Register.query.get(id)
    if entry==None:
        return {"message": "ID {} does not exist".format(id), "type": "error"}
    else:
        db.session.delete(entry)
        db.session.commit()
        return {"message": "Registration with ID {} deleted successfully.".format(id), "type": "info"}

@app.route("/dashboard/entry/modify/report/<id>", methods=['POST'])
def dashboard_modify_report(id: int):
    if session.get("appsecret")!=app.secret_key:
        return redirect('/dashboard/login')
    remark=request.data
    try:
        registration=Register.query.get(id)
        registration.remark=remark
        db.session.commit()
        return {"message": "Remark updated successfully for ID {}.".format(id), "type": "info"}
    except Exception as err:
        return {"message": str(err), "type": "error"}

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/dashboard/login')

@app.route('/registered')
def registered():
    return render_template('registered.html')

@app.route('/error/<message>')
def error(message: str):
    return render_template('error.html', message=message)

if __name__=="__main__":
    app.run(debug=True)

# https://executive-ed.xpro.mit.edu/virtual-reality-augmented-reality
# https://xrcourse.com/syr/courses/xr-development-with-unity
# https://amityonline.com/lp/tcsion-mca-bca/
# https://www.backstagepass.co.in/landing-page/augmented-reality-virtual-reality/