from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import datetime, timedelta  # Import timedelta


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# --- Database configuration--
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# --- Database models ---
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
    
class Food(db.Model):  # Define a model for food items
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    kcal = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=True)  # Store image file path

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "kcal": self.kcal,
            "image": self.image,
        }
class Water(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    consumption_ml = db.Column(db.Integer, nullable=False)
    goal_ml = db.Column(db.Integer, nullable=True)  # Allow goal to be null initially

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "consumption_ml": self.consumption_ml,
            "goal_ml": self.goal_ml,
        }
    
class Sleep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    sleep_goal_hours = db.Column(db.Float, nullable=True)  # Goal in hours
    bedtime = db.Column(db.Time, nullable=True)  # Time the user went to bed
    wake_time = db.Column(db.Time, nullable=True)  # Time the user woke up

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "sleep_goal_hours": self.sleep_goal_hours,
            "bedtime": self.bedtime.strftime('%H:%M') if self.bedtime else None,
            "wake_time": self.wake_time.strftime('%H:%M') if self.wake_time else None,
        }



# --- Login ---
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

# --- Monkmode ---
@app.route('/monk_mode')
def monk_mode():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))
    return render_template('monk_mode.html', user=user)

# --- Goals ---
@app.route('/goals')
def goals():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))
    return render_template('goals.html', user=user)

# --- Health ---
@app.route('/health', methods=['GET', 'POST'])
def health():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))

    # Get selected date or default to today
    selected_date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()

    # Fetch water data for the selected date
    water_entry = Water.query.filter_by(user=user, date=selected_date).first()
    total_water = water_entry.consumption_ml if water_entry else 0
    water_goal = water_entry.goal_ml if water_entry else 2000  # Default goal: 2000 ml

    # Handle form submissions
    if request.method == 'POST':
        # Handle water goal and consumption updates
        if 'water_goal' in request.form:
            water_goal = int(request.form['water_goal'])
            if water_entry:
                water_entry.goal_ml = water_goal
            else:
                water_entry = Water(user=user, date=selected_date, consumption_ml=0, goal_ml=water_goal)
                db.session.add(water_entry)

        if 'water_amount' in request.form:
            water_amount = int(request.form['water_amount'])
            if water_entry:
                water_entry.consumption_ml += water_amount
            else:
                water_entry = Water(user=user, date=selected_date, consumption_ml=water_amount, goal_ml=water_goal)
                db.session.add(water_entry)

        # Handle sleep goal and times
        if 'sleep_goal' in request.form:
            sleep_goal = float(request.form.get('sleep_goal'))
            sleep_entry = Sleep.query.filter_by(user=user, date=selected_date).first()
            if sleep_entry:
                sleep_entry.sleep_goal_hours = sleep_goal
            else:
                sleep_entry = Sleep(user=user, date=selected_date, sleep_goal_hours=sleep_goal)
                db.session.add(sleep_entry)

        if 'bedtime' in request.form and 'wake_time' in request.form:
            bedtime = request.form.get('bedtime')
            wake_time = request.form.get('wake_time')
            sleep_entry = Sleep.query.filter_by(user=user, date=selected_date).first()
            if sleep_entry:
                sleep_entry.bedtime = datetime.strptime(bedtime, '%H:%M').time()
                sleep_entry.wake_time = datetime.strptime(wake_time, '%H:%M').time()
            else:
                sleep_entry = Sleep(
                    user=user,
                    date=selected_date,
                    bedtime=datetime.strptime(bedtime, '%H:%M').time(),
                    wake_time=datetime.strptime(wake_time, '%H:%M').time(),
                )
                db.session.add(sleep_entry)

        # Handle food submissions
        if 'title' in request.form:  # Check for food form submission
            title = request.form['title']
            description = request.form['description']
            category = request.form['category']
            kcal = int(request.form['kcal'])

            # Handle image upload
            image_file = request.files['image'] if 'image' in request.files else None
            image_path = None
            if image_file and image_file.filename:
                image_filename = f"{datetime.now().timestamp()}_{image_file.filename}"
                image_path = f"static/uploads/{image_filename}"
                image_file.save(image_path)

            # Create a new food entry
            new_food = Food(
                user=user,
                title=title,
                description=description,
                category=category,
                kcal=kcal,
                image=image_path,
            )
            db.session.add(new_food)

        db.session.commit()
        return redirect(url_for('health', date=selected_date))

    # Calculate progress for water tracking
    percentage = (total_water / water_goal) * 100 if water_goal > 0 else 0
    remaining_ml = max(water_goal - total_water, 0)

    # Fetch sleep data for the selected date
    sleep_entry = Sleep.query.filter_by(user=user, date=selected_date).first()
    sleep_goal_hours = sleep_entry.sleep_goal_hours if sleep_entry else 8
    sleep_duration = None
    sleep_percentage = None
    if sleep_entry and sleep_entry.bedtime and sleep_entry.wake_time:
        bedtime_datetime = datetime.combine(selected_date, sleep_entry.bedtime)
        wake_time_datetime = datetime.combine(selected_date, sleep_entry.wake_time)
        if wake_time_datetime < bedtime_datetime:
            wake_time_datetime += timedelta(days=1)
        sleep_duration = (wake_time_datetime - bedtime_datetime).total_seconds() / 3600
        sleep_percentage = (sleep_duration / sleep_goal_hours) * 100 if sleep_goal_hours > 0 else 0

    # Fetch food data with pagination
    selected_category = request.args.get('category', '')
    search_query = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 4
    query = Food.query.filter_by(user=user)

    if selected_category:
        query = query.filter_by(category=selected_category)
    if search_query:
        query = query.filter(Food.title.ilike(f"%{search_query}%") | Food.description.ilike(f"%{search_query}%"))

    pagination = query.paginate(page=page, per_page=per_page)
    food_items = pagination.items

    return render_template(
        'health.html',
        user=user,
        selected_date=selected_date,
        total_water=total_water,
        water_goal=water_goal,
        percentage=round(percentage, 2),
        remaining_ml=remaining_ml,
        sleep_goal_hours=sleep_goal_hours,
        sleep_duration=round(sleep_duration, 2) if sleep_duration else None,
        sleep_percentage=round(sleep_percentage, 2) if sleep_percentage else None,
        food_items=[item.to_dict() for item in food_items],
        selected_category=selected_category,
        search_query=search_query,
        pagination=pagination,
        timedelta=timedelta,  # Pass timedelta to the template
        datetime=datetime,  # Pass datetime to the template
    )



@app.route('/water', methods=['GET', 'POST'])
def water():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))

    today = datetime.today().date()
    water_entry = Water.query.filter_by(user=user, date=today).first()

    if request.method == 'POST':
        water_amount = int(request.form['water_amount'])

        if water_entry:
            water_entry.consumption_ml += water_amount
        else:
            water_entry = Water(user=user, date=today, consumption_ml=water_amount)
            db.session.add(water_entry)

        db.session.commit()
        return redirect(url_for('water'))

    total_consumption = water_entry.consumption_ml if water_entry else 0
    return render_template('water.html', total_consumption=total_consumption, user=user)






@app.route('/edit_food', methods=['POST'])
def edit_food():
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))

    food_id = request.form['id']
    food = Food.query.filter_by(id=food_id, user=user).first()
    if food:
        food.title = request.form['title']
        food.description = request.form['description']
        food.category = request.form['category']
        food.kcal = request.form['kcal']
        
        # Check if a new image is uploaded
        if 'image' in request.files and request.files['image']:
            image_file = request.files['image']
            image_filename = f"{datetime.now().timestamp()}_{image_file.filename}"
            image_path = f"static/uploads/{image_filename}"
            image_file.save(image_path)
            food.image = image_path
        
        db.session.commit()

    return redirect(url_for('health'))

@app.route('/delete_food/<int:food_id>', methods=['POST'])
def delete_food(food_id):
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))

    food = Food.query.filter_by(id=food_id, user=user).first()
    if food:
        db.session.delete(food)
        db.session.commit()

    return redirect(url_for('health'))



# --- Finance ---
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
