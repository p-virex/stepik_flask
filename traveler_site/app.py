from flask import Flask, render_template

from traveler_site.data import title, subtitle, description, departures, tours

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html',
                           title=title,
                           subtitle=subtitle,
                           description=description,
                           departures=departures,
                           tours=tours)


@app.errorhandler(404)
def render_not_found(error):
    return "Ничего не нашлось! Вот неудача, отправляйтесь на главную!"


@app.errorhandler(500)
def render_server_error(error):
    return "Что-то не так, но мы все починим"


@app.route('/departures/<departure_name>/')
def render_departure(departure_name):
    select_departure = list()
    for tour_id, tour_info in tours.items():
        if tour_info['departure'] != departure_name:
            continue
        tour_info.update({'tour_id': tour_id})
        select_departure.append(tour_info)
    return render_template('departure.html',
                           departures=select_departure,
                           count=len(select_departure))


@app.route('/tours/<tour_id>/')
def render_tour(tour_id):
    from_departure = tours.get(int(tour_id)).get('departure')
    return render_template('tour.html',
                           departures=departures,
                           tour_info=tours.get(int(tour_id), 'None'),
                           from_departure=departures.get(from_departure))


app.run()
