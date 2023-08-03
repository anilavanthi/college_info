from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

#db.create_all()
with app.app_context():
    db.create_all()
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get data from the form
        username = request.form['username']
        password = request.form['password']

        # Check if the user already exists in the database
        user = User.query.filter_by(username=username).first()
        if user:
            return "Username already exists."

        # Create a new user object and add it to the database
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Flash a success message
        flash('Registration Successful! Please log in.', 'success')

        # Redirect to the login page after successful registration
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get data from the form
        username = request.form['username']
        password = request.form['password']

        # Validate the username and password against the database
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Set up a session to remember the user (optional)
            # Here, you can use Flask's session to manage user sessions.

            # Redirect to the college website after successful login
            return redirect('http://avanthi.edu.in/sttheressa/')
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
