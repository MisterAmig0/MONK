from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journaling.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# --- Database models ---
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    question1 = db.Column(db.Text, nullable=False)
    question2 = db.Column(db.Text, nullable=False)
    question3 = db.Column(db.Text, nullable=False)
    question4 = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "question1": self.question1,
            "question2": self.question2,
            "question3": self.question3,
            "question4": self.question4,
        }

# --- Login page ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_user/<username>')
def select_user(username):
    session['user'] = username
    return redirect(url_for('select_theme'))

# --- Select theme ---
@app.route('/select_theme')
def select_theme():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))
    return render_template('select_theme.html')

# --- Journaling ---
@app.route('/journaling', methods=['GET', 'POST'])
def journaling():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))

    if request.method == 'POST':
        edit_id = request.form.get('edit_id', '')

        if edit_id:  # Update an existing post
            post = Post.query.filter_by(id=int(edit_id), user=user).first()
            if post:
                post.question1 = request.form['question1']
                post.question2 = request.form['question2']
                post.question3 = request.form['question3']
                post.question4 = request.form['question4']
        else:  # Create a new post
            new_post = Post(
                user=user,
                question1=request.form['question1'],
                question2=request.form['question2'],
                question3=request.form['question3'],
                question4=request.form['question4'],
            )
            db.session.add(new_post)

        db.session.commit()  # Save changes to the database

    # Fetch posts for the current user
    user_posts = Post.query.filter_by(user=user).all()
    return render_template('journaling.html', posts=[post.to_dict() for post in user_posts])

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
