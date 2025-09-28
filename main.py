# Library imports
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Create Flask application
app = Flask(__name__)

# Configurations
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taches.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the SQLAlchemy object to manage the database
db = SQLAlchemy(app)

# Define the Task model (represents a task in the database)
class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="todo")

    def __repr__(self):
        return f"<Task {self.name} ({self.status})>"
    
@app.route("/", methods=["GET", "POST"])
def index():
    message = None

    if request.method == "POST": 
        # User new task
        new_task = request.form["new_task"].strip()

        # Warnings
        if new_task == "":
            message = "A task cannot be empty"

        elif Task.query.filter_by(name=new_task).first():
            message = "This task already exists"
        else:
            new = Task(name=new_task, status="todo")
            db.session.add(new)
            db.session.commit()
    # Filled in Task table
    todo = Task.query.filter_by(status="todo").all()
    in_progress = Task.query.filter_by(status="in_progress").all()
    done = Task.query.filter_by(status="done").all()

    return render_template("index.html", 
                           todo=todo,
                           in_progress = in_progress,
                           done = done, 
                           message=message)  

# Delete 
@app.route("/delete", methods=["POST"])
def delete():
    task_to_del = request.form["task"]
    status_to_del = request.form["status"]
    task = Task.query.filter_by(name=task_to_del, status=status_to_del).first()
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect("/")

# Move
@app.route("/move", methods=["POST"])
def move():
    task_to_move= request.form["task"]
    status_to_move = request.form["status"]
    status_dest= request.form["destination"]
    task = Task.query.filter_by(name=task_to_move, status=status_to_move).first()
    if task:
        task.status = status_dest
        db.session.commit()
    return redirect("/")

if __name__ == "__main__": 
    with app.app_context():
        db.create_all()
    app.run(debug=True)

