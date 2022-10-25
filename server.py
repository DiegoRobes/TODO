import os
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.environ.get('SERVER_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///many_2_many_weeks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class Days(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), unique=False, nullable=False)
    pets = db.relationship('Tasks', backref="day")


class Tasks(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), unique=False, nullable=False)
    task_description = db.Column(db.String(500), unique=False, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('days.id'))


with app.app_context():
    db.create_all()

days_names = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}


# all Flask routes below
@app.route("/", methods=["GET", "POST"])
def home():
    days_table = Days.query.order_by(Days.id).all()
    ordered_tasks = Tasks.query.order_by(Tasks.owner_id).all()
    if request.method == "POST":
        raw_day = [i for i in days_names if days_names[i] == request.form["day-OW"]]
        new_task = Tasks(
            task_name=request.form["name"],
            task_description=request.form["description"],
            owner_id=raw_day[0]
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("index.html", days=days_names, tasks=ordered_tasks, table=days_table)


@app.route("/add", methods=["GET", "POST"])
def add():
    return render_template("add.html")


if __name__ == '__main__':
    app.run(debug=True)
