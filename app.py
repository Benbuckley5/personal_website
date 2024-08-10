from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import re


app = Flask(__name__)
app.app_context()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

                # Basic validation checks
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))
        
        # Email validation
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            flash('Invalid email address.', 'danger')
            return redirect(url_for('register'))
        
        # Password validation
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return redirect(url_for('register'))
        
        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please use a different email or log in.', 'danger')
            return redirect(url_for('register'))


        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        #return redirect(url_for('users'))
    return render_template('register.html')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)

# user = User.query.first()
# print(user.username)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/submit', methods = ['POST'])
def submit():
    name = request.form['name']
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run(debug = True)

