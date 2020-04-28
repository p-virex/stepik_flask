import time
from random import shuffle

from flask import Flask, request, render_template
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from edu_site.data import goals, teachers, days

from edu_site.collect_data import g_data

app = Flask(__name__)
app.secret_key = "randomstring"


class RequestForm(FlaskForm):
    """
    Форму конечно сделал коряво и не смог понять почему не работает валидация.
    По хорошему стоит вынести choices в отдельный конфиг, не стал этого делать т.к. в задании нет установок.
    """
    name = StringField('name', [InputRequired()])
    client_weekday = StringField('client_weekday', [InputRequired()])
    client_time = StringField('client_time', [InputRequired()])
    client_teacher = StringField('client_teacher', [InputRequired()])
    phone = StringField('phone', [InputRequired()])
    goal = RadioField('goal', validators=[InputRequired()], choices=[(key, value) for key, value in goals.items()], )
    free_time = RadioField('free_time', validators=[InputRequired()],
                           choices=[("1", "1-2 часа в неделю"), ("3", "3-5 часов в неделю"),
                                    ("5", "5-7 часов в неделю"),
                                    ("7", "7-10 часов в неделю")])


@app.route('/')
def render_index():
    """
    Выводим рандомных 6 учителя
    """
    teachers_list = g_data.get_from_data('teachers')
    shuffle(teachers_list)
    return render_template("index.html",
                           goals=g_data.get_from_data('goals'),
                           teachers=teachers_list[:6])


@app.route('/all/')
def render_all():
    """
    Выводим все учителей без рандомайзера
    """
    return render_template("index.html",
                           goals=g_data.get_from_data('goals'),
                           teachers=g_data.get_from_data('teachers'))


@app.route('/request/')
def render_request():
    form = RequestForm()
    return render_template("request.html",
                           form=form)


@app.route('/request_done/', methods=["GET", "POST"])
def render_done():
    form = RequestForm()
    if request.method == 'POST':
        # создаем уникальную id для каждой записи
        req_id = int(time.time())
        request_info = {
            'name': form.name.data,
            'phone': form.phone.data,
            'goal': form.goal.data,
            'free_time': form.free_time.data
        }
        # сохраняем данные из формы в аналог БД
        g_data.set_to_data(str(req_id), request_info, 'request')
        return render_template("request_done.html",
                               form=form,
                               goals=g_data.get_from_data('goals'))
    return render_template("request.html",
                           form=form)


@app.route('/goals/<goal_id>/')
def render_goal(goal_id):
    goal = g_data.get_from_data('goals').get(goal_id)
    return render_template("goal.html",
                           goal=goal,
                           goal_id=goal_id,
                           goals=g_data.get_from_data('goals'),
                           teachers=g_data.get_from_data('teachers'))


@app.route('/profiles/<id_profile>/')
def render_profile(id_profile):
    data_goals = g_data.get_from_data('goals')
    tag_goals = ''
    # наверное эти переборы можно сделать в шаблоне, но мне показалось это усложнением на этом этапе
    for info in g_data.get_from_data('teachers'):
        if info['id'] == int(id_profile):
            for tag in info.get('goals', []):
                # собираем теги в строку для более красивого вывода на персональной страничке
                tag_goals += f' {data_goals.get(tag)}'
            return render_template("profile.html",
                                   teacher=info,
                                   tag_goals=tag_goals,
                                   days=g_data.get_from_data('days'))


@app.route('/booking_done/', methods=["GET", "POST"])
def render_booking_done():
    form = RequestForm()
    if request.method == 'POST':
        # создаем уникальную id для каждой записи
        req_id = int(time.time())
        request_info = {
            'name': form.name.data,
            'phone': form.phone.data,
            'date': form.client_weekday.data,
            'client_time': form.client_time.data,
            'teacher': form.client_teacher.data
        }
        # сохраняем данные из формы в аналог БД
        g_data.set_to_data(str(req_id), request_info, 'booking')
        return render_template("booking_done.html",
                               form=form)
    return render_template("request.html",
                           form=form)


@app.route('/booking/<id_teach>/<day_weekly>/<time>/')
def render_booking(id_teach, day_weekly, time):
    form = RequestForm()
    for info in g_data.get_from_data('teachers'):
        if info['id'] == int(id_teach):
            return render_template("booking.html",
                                   name_teacher=info['name'],
                                   day=g_data.get_from_data('days').get(day_weekly),
                                   time=time,
                                   form=form)


if __name__ == '__main__':
    # сделал контролер для записи в json, мне кажется так удобней, можно засунуть в цикл, но не стал запариваться
    g_data.set_to_data('goals', goals)
    g_data.set_to_data('teachers', teachers)
    g_data.set_to_data('days', days)
    app.run(port=8060)
