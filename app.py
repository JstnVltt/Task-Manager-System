from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

app.secret_key = 'our_secret_key'


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Feedback %r>' % self.id



with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('Home.html') # Look automatically in templates/


@app.route('/tasks', methods=['POST', 'GET'])
def index():
    if request.method == 'POST': # if it's an action caused by the submit field
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('tasks.html', tasks=tasks) # Look automatically in templates/


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    return ''


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_content = request.form['feedback']
        new_feedback = Todo(content=feedback_content)

        flash('Thank you for your feedback!')
        return redirect(url_for('feedback'))
    else:
        return render_template('Feedback.html')

if __name__ == "__main__":
    app.run(debug=True)