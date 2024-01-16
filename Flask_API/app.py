from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sjyqlzgj:a0NuohMAEl_7VqcNgwcAdA1NTbm2DhoN@mel.db.elephantsql.com/sjyqlzgj'
app.app_context().push()
db = SQLAlchemy(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed =db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        
        new_task =Todo(content=task_content)

        try:    
            db.session.add(new_task)
            db.session.commit()
            logger.info('Task Added Successfully')
            return redirect('/')
        except Exception as e:
            logger.error(f'Error adding task: {str(e)}')
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        logger.info(f'Task with ID {id} deleted Successfully')
        return redirect('/')
    except Exception as e:
        logger.error(f'Error deleting task: {str(e)}')
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            logger.info(f'Task with ID {id} updated Successfully')
            return redirect('/')
        except Exception as e:
            logger.error(f'Error updating task: {str(e)}')
            return 'There was a problem updating that task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)
