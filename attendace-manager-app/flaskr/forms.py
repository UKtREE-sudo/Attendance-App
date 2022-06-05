from ast import Pass
from calendar import month
from errno import EALREADY
from time import strftime
from tokenize import String
from wtforms.form import Form
from wtforms.fields import StringField, PasswordField, SubmitField, DateField, HiddenField, TimeField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flaskr.models import Abisol_Member


# ログイン画面で利用
class CalendarForm(Form):
    title = StringField('タイトル: ')
    start = DateField('始業: ')
    end = DateField('終業: ')
    submit = SubmitField('登録')

class AbisolCalendarForm(Form):
    calendar_id = HiddenField('hidden')
    date = StringField('')
    start = TimeField('')
    end = TimeField('')
    submit = SubmitField('更新')

class LoginForm(Form):
    email = StringField('メール: ', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード: ', validators=[DataRequired()])
    submit = SubmitField('ログイン')

class RegisterForm(Form):
    email = StringField('メール: ', validators=[DataRequired(), Email()])
    username = StringField('ユーザー名: ', validators=[DataRequired()])
    password = PasswordField(
        'パスワード: ', 
        validators=[DataRequired(), 
        EqualTo('password_confirm', message='Password do not match.')]
    )
    password_confirm = PasswordField('パスワード(再入力): ', validators=[DataRequired()])
    submit = SubmitField('登録')

    def validate_email(self, field):
        if Abisol_Member.select_by_email(field.data):
            raise ValidationError('このメールアドレスは既に使用されています')

class UpdateWorkTableRecordForm(Form):
    abisol_member_id = HiddenField()
    year = HiddenField()
    month = HiddenField()
    day = HiddenField()
    date_attribute = StringField() 
    late_early = SelectField(u'早/遅', choices=[('', ''), ('早', '早退'), ('遅', '遅刻')])
    start_at = TimeField()
    end_at = TimeField()
    working_hour = TimeField()
    recess_hour = TimeField()
    extra_hour = TimeField()
    graveyard_shift_hour = TimeField()
    holiday_shift_hour = TimeField()
    work_content = StringField()
    about_attendance = StringField()
    submit = SubmitField('更新')