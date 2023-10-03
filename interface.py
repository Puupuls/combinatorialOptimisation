import json

import flask
from flask import Flask

from optimizer import create_test_domain, Optimizer

app = Flask(__name__)


domain = create_test_domain()
optimizer = Optimizer(domain)
# optimizer.start()


@app.route('/')
def ui():
    return flask.render_template('show.html')


@app.route('/iterate')
def iterate():
    optimizer.solve()
    return domain.to_json()


@app.route('/data')
def data():
    return domain.to_json()


@app.route('/decrease/<int:idx>')
def decrease(idx):
    point = domain.points[idx]
    if point.value == 1:
        domain.points.pop(idx)
    else:
        point.value -= 1
    optimizer.fill_distances()
    domain.solutions = []
    domain.bad_solutions = []
    return domain.to_json()


@app.route('/reset')
def reset():
    domain = create_test_domain()
    optimizer.domain = domain
    optimizer.fill_distances()
    domain.solutions = []
    domain.bad_solutions = []
    return {}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
