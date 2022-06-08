from traceback import print_tb
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flaskr.forms import AbisolCalendarForm, LoginForm, RegisterForm, UpdateWorkTableRecordForm
from flaskr.models import db, Abisol_Member, Work_Table_Record
import calendar as cldr
import datetime
import pytz

bp = Blueprint('app', __name__, url_prefix='')

now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
now_year = now.year
now_month = now.month
calendar = cldr.monthcalendar(now_year, now_month)

@bp.route('/')
def home():
    return render_template('index.html')


@bp.route('/abisol_calendar', methods=['GET', 'POST'])
def abisol_calendar():
    form = AbisolCalendarForm(request.form)
    now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    year = now.year
    month = now.month
    if month < 10:
        string_month = '0' + str(month)
    else:
        string_month = str(month)

    cl = cldr.monthcalendar(year, month)
    dates = []

    for week in cl:
        for d in week:
            if d != 0 and d < 10:
                string_d = '0' + str(d)
                date_title = string_month + '月' + string_d + '日'
                dates.append(date_title)
            elif d >= 10:
                string_d = str(d)
                date_title = string_month + '月' + string_d + '日'
                dates.append(date_title)

    return render_template('abisol_calendar.html', form=form, dates=dates)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = Abisol_Member.select_by_email(form.email.data)

        # メールアドレスから取得したUserのパスワードとクライアントが入力したパスワードが一致するか
        if user and user.validate_password(form.password.data):
            login_user(user, remember=True)
            # 次のURL
            next = request.args.get('next')
            if not next:
                next = url_for('app.show_work_table')
            return redirect(next)
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        user = Abisol_Member(
            email = form.email.data,
            username = form.username.data,
            password = form.password.data
        )
        user.add_user()
        return redirect(url_for('app.login'))
    return render_template('register.html', form=form)

@bp.route('/work_table', methods=['GET', 'POST'])
@login_required
def show_work_table():
    form = UpdateWorkTableRecordForm(request.form)
    id = current_user.id
    today = datetime.date.today()
    record = Work_Table_Record.select_by_abisol_member_id_and_date_time(id, now_year, now_month)
    # 今月の勤務表レコードが存在しない場合には作成
    if not record:
        for cl_week in calendar:
            for cl_day in cl_week:
                if cl_day != 0:
                    wtr = Work_Table_Record(
                        abisol_member_id = id,
                        year = now_year,
                        month = now_month,
                        day = cl_day,
                        date_attribute = 'なし',
                        late_early = 'なし',
                        start_at = '09:30',
                        end_at = '18:30',
                        working_hour = '08:00',
                        recess_hour = '00:00',
                        extra_hour = '00:00',
                        graveyard_shift_hour = '00:00',
                        holiday_shift_hour = '00:00',
                        work_content = 'なし',
                        about_attendance = 'なし',
                    )
                    wtr.add_work_table_record()
    
    # リクエストメソッドがPOSTの場合
    if request.method == 'POST':
        abi_id = id
        y = form.year.data
        m = form.month.data
        d = form.day.data

        # データの詰め替え用意
        date_attribute = form.date_attribute.data
        late_early = form.late_early.data
        start_at = form.start_at.data
        end_at = form.end_at.data
        working_hour = form.working_hour.data
        recess_hour = form.recess_hour.data
        extra_hour = form.extra_hour.data
        graveyard_shift_hour = form.graveyard_shift_hour.data
        holiday_shift_hour = form.holiday_shift_hour.data
        work_content = form.work_content.data
        about_attendance = form.about_attendance.data

        # データ詰め替えの実施
        with db.session.begin(subtransactions=True):
            work_table = Work_Table_Record.query.filter_by(abisol_member_id=abi_id, year=y, month=m, day=d).first()

            work_table.date_attribute = date_attribute
            work_table.late_early = late_early
            work_table.start_at = start_at
            work_table.end_at = end_at
            work_table.working_hour = working_hour
            work_table.recess_hour = recess_hour
            work_table.extra_hour = extra_hour
            work_table.graveyard_shift_hour = graveyard_shift_hour
            work_table.holiday_shift_hour = holiday_shift_hour
            work_table.work_content = work_content
            work_table.about_attendance = about_attendance
        db.session.commit()
        return redirect(url_for('app.show_work_table'))

    table_lists = Work_Table_Record.query.order_by(Work_Table_Record.day).filter_by(abisol_member_id=id, year=now_year, month=now_month)
    return render_template('abisol_calendar.html', form=form, table_lists=table_lists)