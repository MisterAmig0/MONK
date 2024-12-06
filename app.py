from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key for session management
app.wsgi_app = ProxyFix(app.wsgi_app)

# Dummy users
users = ["Illias", "Sam"]

# --- Login / User Select ---

@app.route('/')
def user_select():
    return render_template('index.html', users=users)

@app.route('/select_user/<username>')
def select_user(username):
    # Ensure valid user
    if username not in users:
        return redirect(url_for('user_select'))
    
    # Set selected user in session
    session['username'] = username
    if 'user_data' not in session:
        session['user_data'] = {}
    
    # Render dashboard.html with the selected username
    return render_template('dashboard.html', username=username)

@app.route('/save_data', methods=['POST'])
def save_data():
    if 'username' not in session:
        return redirect(url_for('user_select'))
    
    username = session['username']
    data = request.form['user_input']
    
    # Save data specifically to the user's session
    session['user_data'][username] = data
    session.modified = True  # Ensure session changes are saved
    
    return redirect(url_for('user_home'))

# --- Journaling ---

@app.route('/journaling')
def journaling():
    if 'username' not in session:
        return redirect(url_for('user_select'))
    current_date = datetime.now().strftime("%B , %Y")  # Format: "Month Year"
    return render_template('journaling.html', username=session['username'], current_date=current_date)

# --- Monk mode ---

@app.route('/monk_mode')
def monk_mode():
    if 'username' not in session:
        return redirect(url_for('user_select'))
    return render_template('monk_mode.html', username=session['username'])

# --- Goals ---

@app.route('/goals')
def goals():
    if 'username' not in session:
        return redirect(url_for('user_select'))
    return render_template('goals.html', username=session['username'])

# --- Health tracker ---

@app.route('/health')
def health():
    if 'username' not in session:
        return redirect(url_for('user_select'))
    # Get current month and year
    current_date = datetime.now().strftime("%B , %Y")  # Format: "Month Year"
    return render_template('health.html', username=session['username'], current_date=current_date)

# --- Bank ---

@app.route('/finance')
def finance():
    if 'username' not in session:
        return redirect(url_for('user_select'))
    return render_template('finance.html', username=session['username'])


if __name__ == '__main__':
    app.run(debug=True)
