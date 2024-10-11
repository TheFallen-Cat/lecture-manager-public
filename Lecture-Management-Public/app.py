from flask import Flask, render_template, redirect, request, session, flash, send_file
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from dotenv import load_dotenv
from datetime import timedelta
import openpyxl
import json
import os

# * External Imports
from forms.login_form import LoginForm
from forms.lecture_detail_form import LectureDetailForm
import utils as util

app = Flask(__name__)
app.config["SECRET_KEY"] = "Testkey"
app.permanent_session_lifetime = timedelta(days=100)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "databases/records.db"
)

app.config["SQLALCHEMY_BINDS"] = {
    "users": f"sqlite:///{os.path.join(basedir, 'databases/users.db')}"
}


login_manager = LoginManager(app=app)
login_manager.login_view = "login"


# * ==================== Loading .env variables ====================

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN1_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN1_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PORT = os.getenv("DATABASE_PORT")

USER_LIST = json.loads(os.getenv("USER_LIST"))
ADMIN_LIST = json.loads(os.getenv("ADMIN_LIST"))
DICT_NAMES = json.loads(os.getenv("DICT_NAMES"))

db = SQLAlchemy(app=app)


connection = mysql.connector.connect(
    host=DATABASE_HOST,
    database=DATABASE_NAME,
    user=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
)
cursor = connection.cursor(dictionary=True)

# * ==================== DB Models ====================


class Record(db.Model):
    _id = db.Column("Id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(30))
    date = db.Column("date", db.String(30), nullable=False)
    main_class = db.Column("main_class", db.String(30), nullable=False)
    subject = db.Column("subject", db.String(30), nullable=False)
    topic = db.Column("topic", db.String(30), nullable=False)
    students_present = db.Column("students_present", db.Integer, nullable=False)
    no_of_lectures = db.Column("no_of_lectures", db.Integer, nullable=False)
    lecture_from = db.Column("lecture_from", db.String(30), nullable=False)
    lecture_to = db.Column("lecture_to", db.String(30), nullable=False)
    submitted_at = db.Column("Submitted_at", db.String(30), nullable=False)

    def __init__(
        self,
        name,
        date,
        main_class,
        subject,
        topic,
        students_present,
        no_of_lectures,
        lecture_from,
        lecture_to,
        submitted_at,
    ):
        self.name = name
        self.date = date
        self.main_class = main_class
        self.subject = subject
        self.topic = topic
        self.students_present = students_present
        self.no_of_lectures = no_of_lectures
        self.lecture_from = lecture_from
        self.lecture_to = lecture_to
        self.submitted_at = submitted_at


class User(db.Model):
    __bind_key__ = "users"
    _id = db.Column("Id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(30), nullable=False)
    password = db.Column("password", db.String(30), nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password


def save_records(
    name: str,
    date: str,
    main_class: str,
    subject: str,
    topic: str,
    students_present: str,
    no_of_lectures: int,
    lecture_from: str,
    lecture_to: str,
    submitted_at: str,
):
    cursor = connection.cursor(dictionary=True)
    
    data_dict = (name, date, main_class, subject, topic, students_present, no_of_lectures, lecture_from, lecture_to, submitted_at)

    try:
        cursor.execute("""INSERT INTO records (name, date, main_class, subject, topic, students_present, no_of_lectures, lecture_from, lecture_to, submitted_at)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", data_dict)

        connection.commit()

        flash("Successfully submitted the form.", "alert-success")

    except Exception as error:
        
        cursor.execute("""INSERT INTO records (name, date, main_class, subject, topic, students_present, no_of_lectures, lecture_from, lecture_to, submitted_at)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", data_dict)

        connection.commit()

        print(error)
        flash("Successfully submitted the form. 2", "alert-success")



    


# ========================================================
# * User loader and Auth Class
# ========================================================


class Auth(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    # * Fetch user from the database

    try:
        _user = User.query.filter_by(_id=user_id)
        result = _user.first()

    except Exception as e:
        return None

    if result:
        user = Auth(id=result._id, username=result.name)
        return user

    return None


# ========================================================
# * Login Page
# ========================================================


@app.route("/", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if current_user.is_authenticated:
        if current_user.username in ADMIN_LIST:
            return redirect("/admin")

        elif current_user.username in USER_LIST:
            return redirect("/user")

    if login_form.validate_on_submit():
        username = login_form.name.data

        try:
            _user_data = User.query.filter_by(name=username)
            user_data = _user_data.first()

        except Exception as e:
            return redirect(request.url)

        if user_data:
            passwd = user_data.password

            if login_form.password.data == passwd:
                user = Auth(id=user_data._id, username=user_data.name)
                login_user(user, remember=True)

                if username in ADMIN_LIST:
                    return redirect("/admin")

                elif username in USER_LIST:
                    return redirect("/user")

            else:
                flash("Incorrect username or password.", "alert-danger")

        else:
            flash("No user found.", "alert-danger")

    else:
        print(login_form.errors)

    return render_template("login.html", form=login_form, loggedInMessage=True)


# ========================================================
# * User Form for passing the data
# ========================================================


@app.route("/user", methods=["GET", "POST"])
@login_required
def user_submit():
    lecture_detail_form = LectureDetailForm()

    if lecture_detail_form.validate_on_submit():
        date = lecture_detail_form.date.data
        main = lecture_detail_form.main_class.data
        topic = lecture_detail_form.topic_covered.data
        students_present = lecture_detail_form.students_present.data
        no_of_lectures = lecture_detail_form.lectures.data
        from_time = lecture_detail_form.from_time.data
        to_time = lecture_detail_form.to_time.data
        subject = lecture_detail_form.subject.data

        # try:
        save_records(
                name=DICT_NAMES[current_user.username],
                date="{:%B %d, %Y}".format(date),
                main_class=main,
                subject=subject,
                topic=topic,
                students_present=students_present,
                no_of_lectures=no_of_lectures,
                lecture_from="{:%I:%M %p}".format(from_time),
                lecture_to="{:%I:%M %p}".format(to_time),
                submitted_at=util.get_current_time(),
        )

        # except Exception as e:
        #     save_records(
        #         name=DICT_NAMES[current_user.username],
        #         date="{:%B %d, %Y}".format(date),
        #         main_class=main,
        #         subject=subject,
        #         topic=topic,
        #         students_present=students_present,
        #         no_of_lectures=no_of_lectures,
        #         lecture_from="{:%I:%M %p}".format(from_time),
        #         lecture_to="{:%I:%M %p}".format(to_time),
        #         submitted_at=util.get_current_time(),
        #     )
        #     flash("Successfully submitted the form.", "alert-success")

        return redirect("/user")

    else:
        print(lecture_detail_form.errors)

    return render_template(
        "user_panel.html",
        lecture_detail_form=lecture_detail_form,
        name=current_user.username,
    )

# ========================================================
# * Admin Page
# ========================================================


@app.route("/admin")
@login_required
def admin_page():
    if current_user.username in ADMIN_LIST:
        return render_template("admin_panel.html", name=current_user.username)

    else:
        return redirect("/")


# ========================================================
# * Download Redirect
# ========================================================


@app.route("/download")
@login_required
def download_file():
    cursor = connection.cursor(dictionary=True)
    if current_user.username in ADMIN_LIST:
        cursor.execute("SELECT * FROM records")
        records = cursor.fetchall()
        if records:
            try:
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Records"
                ws.append(
                    [
                        "Name",
                        "Date",
                        "Class",
                        "Subject",
                        "Topic",
                        "Students Present",
                        "Lectures",
                        "From",
                        "To",
                        "Submitted At",
                    ]
                )
                for record in records:
                    temp_list = list(record.values())[1:]
                    data_row = temp_list
                    ws.append(data_row)

                file_path = "record.xlsx"
                wb.save(file_path)
                wb.close()

                return send_file(
                    file_path,
                    as_attachment=True,
                    download_name="record.xlsx"
                )

            except Exception as e:
                flash("Error creating the excel file!", "alert-danger")
                return "Error creating the excel file."

        else:
            return "No records were found in the database."




# ========================================================
# * Logout User
# ========================================================


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    app.run()
