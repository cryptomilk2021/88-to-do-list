import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), unique=True, nullable=False)
    due_date = db.Column(db.String(10), nullable=False)
    completed_date = db.Column(db.String(10), nullable=True)


@app.route("/")
def home():
    todo = db.session.query(Tasks).all()
    return render_template("index.html", todo=todo)


@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    due_date = request.form.get("due_date")
    new_todo = Tasks(task=task, due_date=due_date, completed_date=None)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/finish/<int:id>", methods=["POST"])
def finish(id: int):
    x = db.session.query(Tasks).get(int(id))
    print(x.due_date)
    today = date.today()
    x.completed_date = str(today.strftime("%d/%m/%y"))
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
