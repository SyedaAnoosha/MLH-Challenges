from flask import Flask, render_template, request, redirect, session 
from flask_bcrypt import Bcrypt 

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Change this to a secure key
bcrypt = Bcrypt()

# Sample user database (you would typically use a database like SQLAlchemy)
users = {
    'user1': {
        'username': 'user1',
        'password': bcrypt.generate_password_hash('password1').decode('utf-8')
    }
}

@app.route('/')
def home():
    if 'username' in session:
        return f"Hello, {session['username']}! You are logged in."
    return "You are not logged in."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and bcrypt.check_password_hash(users[username]['password'], password):
            session['username'] = username
            return redirect('/')
        else:
            return "Invalid username or password. Please try again."

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
