from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import datetime, timedelta  # Import timedelta


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journaling.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Database models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    question1 = db.Column(db.Text, nullable=False)
    question2 = db.Column(db.Text, nullable=False)
    question3 = db.Column(db.Text, nullable=False)
    question4 = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "question1": self.question1,
            "question2": self.question2,
            "question3": self.question3,
            "question4": self.question4,
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_user/<username>')
def select_user(username):
    session['user'] = username
    return redirect(url_for('select_theme'))

@app.route('/select_theme')
def select_theme():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))
    return render_template('select_theme.html')
@app.route('/journaling', methods=['GET', 'POST'])
def journaling():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))

    # Get selected date or default to today
    selected_date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()

    # Format day and date
    formatted_day_date = selected_date.strftime('%A, %d %B')  # Example: "Monday, 05 December 2024"

    if request.method == 'POST':
        # Check if a post for the selected date already exists
        existing_post = Post.query.filter_by(user=user, date=selected_date).first()
        if existing_post and not request.form.get('edit_id'):  # Prevent multiple posts for the same day
            return redirect(url_for('journaling', date=selected_date.strftime('%Y-%m-%d')))

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
                date=selected_date,
                question1=request.form['question1'],
                question2=request.form['question2'],
                question3=request.form['question3'],
                question4=request.form['question4'],
            )
            db.session.add(new_post)

        db.session.commit()  # Save changes to the database

    # Fetch posts for the selected date
    user_posts = Post.query.filter_by(user=user, date=selected_date).all()
    return render_template(
        'journaling.html',
        posts=[post.to_dict() for post in user_posts],
        selected_date=selected_date,
        formatted_day_date=formatted_day_date,  # Pass formatted day and date
        timedelta=timedelta,  # Pass timedelta to the template
        datetime=datetime  # Pass datetime to the template
    )

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))

    post = Post.query.filter_by(id=post_id, user=user).first()
    if post:
        db.session.delete(post)
        db.session.commit()

    selected_date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    return redirect(url_for('journaling', date=selected_date))

# Placeholder routes for other themes
@app.route('/monk_mode')
def monk_mode():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))
    return render_template('monk_mode.html', user=user)

@app.route('/goals')
def goals():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))
    return render_template('goals.html', user=user)

@app.route('/health')
def health():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))
    return render_template('health.html', user=user)

@app.route('/finance')
def finance():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))
    return render_template('finance.html', user=user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
