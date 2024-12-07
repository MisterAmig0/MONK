from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulated database for users and posts
users = ["User1", "User2"]
posts = {
    "User1": [],
    "User2": []
}

@app.route('/')
def index():
    return render_template('index.html', users=users)

@app.route('/select_theme', methods=['POST'])
def select_theme():
    session['user'] = request.form['user']
    return render_template('select_theme.html')

@app.route('/journaling', methods=['GET', 'POST'])
def journaling():
    user = session.get('user')
    if request.method == 'POST':
        # Collect the answers from the modal form
        question1 = request.form['question1']
        question2 = request.form['question2']
        question3 = request.form['question3']
        question4 = request.form['question4']
        # Combine the answers into a single post
        post_content = f"1. {question1}\n2. {question2}\n3. {question3}\n4. {question4}"
        posts[user].append(post_content)
    user_posts = posts.get(user, [])
    return render_template('journaling.html', posts=user_posts)

if __name__ == '__main__':
    app.run(debug=True)
