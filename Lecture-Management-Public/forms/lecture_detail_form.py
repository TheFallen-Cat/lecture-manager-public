from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    IntegerField,
    DateField,
    TimeField,
    SelectField,
    BooleanField,
)
from wtforms.validators import DataRequired


class LectureDetailForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])

    main_class = SelectField(
        "Class",
        choices=[
            "FYBSc",
            "SYBsc",
            "TYBsc",
            "FYBCom",
            "SYBCom",
            "TYBCom",
            "11th Science 1",
            "11th Science 2",
            "11th Science 3",
            "12th Science 1",
            "12th Science 2",
            "12th Science 3",
        ],
        render_kw={"placeholder": "Class Name"},
        validators=[DataRequired()],
    )

    degree_checkbox = BooleanField("Degree")
    junior_checkbox = BooleanField("Junior")

    subject = SelectField(
        "Subject",
        choices=[
            "Numerical Analysis",
            "Computer Programming & System Analysis-1",
            "IT for Business",
            "Computer Systems and applications-1",
            "Real Analysis",
            "Metric Space",
            "Discrete Mathematics",
            "Calculus 3",
            "Mathematics (Jr)",
        ],
        validators=[DataRequired()],
    )

    topic_covered = StringField("Topic covered", validators=[DataRequired()])

    students_present = IntegerField(
        "No of students present", validators=[DataRequired()]
    )

    lectures = IntegerField(
        "Lecture",
        render_kw={"placeholder": "No of lectures"},
        validators=[DataRequired()],
    )

    from_time = TimeField("From", validators=[DataRequired()])

    to_time = TimeField("To", validators=[DataRequired()])

    submit = SubmitField("Submit")
