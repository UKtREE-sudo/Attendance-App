# models.py

from flaskr import db, login_manager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Abisol_Member.query.get(user_id)

class Abisol_Member(UserMixin, db.Model):

    __tablename__ = 'abisol_members'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password).decode('utf-8')

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def add_user(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

    @classmethod
    def select_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


class Work_Table_Record(db.Model):

    __tablename__ = 'work_table_records'
    
    abisol_member_id = db.Column(db.Integer, db.ForeignKey('abisol_members.id'), primary_key=True)
    year = db.Column(db.String, primary_key=True)
    month = db.Column(db.String, primary_key=True)
    day = db.Column(db.Integer, primary_key=True)
    date_attribute = db.Column(db.String(64), nullable=True)
    late_early = db.Column(db.String(64))
    start_at = db.Column(db.String(64))
    end_at = db.Column(db.String(64))
    working_hour = db.Column(db.String(64), nullable=True)
    recess_hour = db.Column(db.String(64), nullable=True)
    extra_hour = db.Column(db.String(64), nullable=True)
    graveyard_shift_hour = db.Column(db.String(64), nullable=True)
    holiday_shift_hour = db.Column(db.String(64), nullable=True)
    work_content = db.Column(db.String(128), nullable=True)
    about_attendance = db.Column(db.String(128), nullable=True)

    def __init__(self, abisol_member_id, year, month, day, date_attribute, late_early, start_at, end_at, working_hour, recess_hour, extra_hour, graveyard_shift_hour, holiday_shift_hour, work_content, about_attendance):
        self.abisol_member_id = abisol_member_id
        self.year = year
        self.month = month
        self.day = day
        self.date_attribute = date_attribute
        self.late_early = late_early
        self.start_at = start_at
        self.end_at = end_at
        self.working_hour = working_hour
        self.work_content = work_content
        self.recess_hour = recess_hour
        self.extra_hour = extra_hour
        self.graveyard_shift_hour = graveyard_shift_hour
        self.holiday_shift_hour = holiday_shift_hour
        self.about_attendance = about_attendance

    def add_work_table_record(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

    @classmethod
    def select_by_abisol_member_id_and_date_time(cls, abisol_member_id, year, month):
        return cls.query.filter_by(abisol_member_id=abisol_member_id, year=year, month=month).first()    


class Event():

    def __init__(self, title, start, end):
        self.title = title
        self.start = start
        self.end = end
