from random import shuffle

from flask import Flask, render_template

from traveler_site.data import title, subtitle, description, departures, tours

app = Flask(__name__)


@app.route('/')
def main():
    id_tours = list(tours.keys())
    shuffle(id_tours)
    return render_template('index.html',
                           title=title,
                           subtitle=subtitle,
                           description=description,
                           departures=departures,
                           tours=tours,
                           id_tours=id_tours[:6])


@app.errorhandler(404)
def render_not_found(error):
    return "Ничего не нашлось! Вот неудача, отправляйтесь на главную!"


@app.errorhandler(500)
def render_server_error(error):
    return "Что-то не так, но мы все починим"


@app.route('/departures/<departure_name>/')
def render_departure(departure_name):
    filter_tours = [info_t for id_t, info_t in tours.items() if info_t['departure'] == departure_name]
    return render_template('departure.html',
                           departure_name=departure_name,
                           tours=tours,
                           departures=departures,
                           filter_tours=filter_tours)


@app.route('/tours/<tour_id>/')
def render_tour(tour_id):
    return render_template('tour.html',
                           departures=departures,
                           tours=tours,
                           tour_id=tour_id)


app.run()
