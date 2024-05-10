from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'mybestsecretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.secret_key = 'our_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Feedback %r>' % self.id


class RegisterForm(FlaskForm):
    username = StringField(validators={InputRequired(), Length(min=4, max=20)}, render_kw={"placeholder": "Username"})
    email = StringField(validators={InputRequired(), Length(max=100)}, render_kw={"placeholder": "Email"})
    password = PasswordField(validators={InputRequired(), Length(min=4, max=20)}, render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")


    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("Username already existing ! Enter a new one.")


class LoginForm(FlaskForm):
    username = StringField(validators={InputRequired(), Length(min=4, max=20)}, render_kw={"placeholder": "Username"})
    password = PasswordField(validators={InputRequired(), Length(min=4, max=20)}, render_kw={"placeholder": "Password"})

    submit = SubmitField("Log in")



with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('Home.html') # Look automatically in templates/


@app.route('/tasks', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST': # if it's an action caused by the submit field
        task_content = request.form['content']
        new_task = Todo(content=task_content, user_id=current_user.id)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/tasks')
        except:
            return 'There was an issue adding the task'
    else:
        tasks = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.date_created).all()
        return render_template('tasks.html', tasks=tasks) # Look automatically in templates/


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    return ''


@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        feedback_content = request.form['feedback']
        new_feedback = Feedback(content=feedback_content)

        flash('Thank you for your feedback!')
        return redirect(url_for('feedback'))
    else:
        return render_template('Feedback.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect('/')


    return render_template('Login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




    return render_template('Login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)





