from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:passwordlol@localhost/simpledb'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kviceqciixjhtf:a34f3d44a4f3dfaebd3127f78e0b85269c1f2055df448d180a53342d45ff0815@ec2-52-45-183-77.compute-1.amazonaws.com:5432/d9v5kfvesodtdf'
   

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200))
    comments = db.Column(db.Text())

    def __init__(self, customer, email, comments):
        self.customer = customer
        self.email = email
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        email = request.form['email']
        comments = request.form['comments']
        #print(customer, email,comments)
        if customer == '' or email == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, email,comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, email, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')


if __name__ == '__main__':
    app.run()
