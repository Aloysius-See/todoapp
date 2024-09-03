from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__, template_folder="templates")

# Configure the SQLAlchemy connection to PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12345@db:5432/NewDB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database connection
db = SQLAlchemy(app)

# Define the Tasks model
class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String())

    def __init__(self, todo):
        self.todo = todo

# Ensure the database and tables are created
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    todos = Tasks.query.all()  # Query all tasks from the database
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def add():
    todo_name = request.form['todo']
    # Create a new task instance
    new_task = Tasks(todo=todo_name)  
    # Add the task to the database
    db.session.add(new_task)  
    db.session.commit()  
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    task = Tasks.query.get_or_404(id)
    if request.method == "POST":
        task.todo = request.form['todo']
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", task= task)

@app.route("/check/<int:id>", methods=['POST'])
def check(id):
    task = Tasks.query.get_or_404(id)
    # task.done = not task.done  
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    task = Tasks.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

