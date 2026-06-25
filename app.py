from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '1234'

db = SQLAlchemy(app)

# ---------------- DATABASE ----------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

# ---------------- LED STATE ----------------

led_status = "OFF"

# ---------------- HOME ----------------

@app.route('/')
def home():
    return redirect('/login')

# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        return redirect('/dashboard')

    return render_template('login.html')

# ---------------- REGISTER ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        user = User(
            username=request.form['username'],
            password=request.form['password']
        )

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():

    temp = random.randint(20, 35)
    humidity = random.randint(40, 80)

    global led_status

    return render_template(
        'dashboard.html',
        temp=temp,
        humidity=humidity,
        led=led_status
    )

# ---------------- LED CONTROL ----------------

@app.route('/led/on')
def led_on():

    global led_status
    led_status = "ON"

    return redirect('/dashboard')

@app.route('/led/off')
def led_off():

    global led_status
    led_status = "OFF"

    return redirect('/dashboard')

# ---------------- API ----------------

@app.route('/api/sensor')
def api():

    return jsonify({
        "temperature": random.randint(20, 35),
        "humidity": random.randint(40, 80),
        "led": led_status
    })

# ---------------- RUN ----------------

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5001)