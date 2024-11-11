from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Route for the home page (dashboard)
@app.route('/')
def home():
    return render_template('dashboard.html')  # Render the dashboard with buttons

# Route for handling button click actions and displaying user-specific content
@app.route('/content/<name>', methods=['GET', 'POST'])
def content(name):
    if request.method == 'POST':
        # Save the submitted input in the session based on the name
        session[name] = request.form['user_input']
    
    # Retrieve the stored content for this user from the session, if it exists
    user_content = session.get(name, "")

    return render_template('content.html', name=name, user_content=user_content)

if __name__ == '__main__':
    app.run(debug=True)
