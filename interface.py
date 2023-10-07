import json

import flask
from flask import Flask, request

from my_types import Point, Domain
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
    optimizer.domain = domain
    optimizer.fill_distances()
    domain.solutions = []
    domain.bad_solutions = []
    domain.num_iterations = 0
    return domain.to_json()


@app.route('/increase/<int:idx>')
def increase(idx):
    point = domain.points[idx]
    point.value += 1
    optimizer.domain = domain
    optimizer.fill_distances()
    domain.solutions = []
    domain.bad_solutions = []
    domain.num_iterations = 0
    return domain.to_json()


@app.route('/create')
def create():
    x = request.args.get("x")
    y = request.args.get('y')
    point = Point(
        x=round(float(x), 2),
        y=round(float(y), 2)
    )
    optimizer.domain.points.append(point)
    optimizer.fill_distances()
    domain.solutions = []
    domain.bad_solutions = []
    domain.num_iterations = 0
    return domain.to_json()


@app.route('/setDist')
def setDist():
    optimizer.domain.time_limit = float(request.args.get('dst'))
    optimizer.fill_distances()
    domain.solutions = []
    domain.bad_solutions = []
    domain.num_iterations = 0
    return domain.to_json()


@app.route('/load', methods=['post'])
def load():
    global optimizer, domain
    domain = Domain.from_dict(request.json)
    optimizer = Optimizer(domain)
    optimizer.solve()
    return optimizer.domain.to_json()


@app.route('/reset')
def reset():
    global optimizer, domain
    domain = create_test_domain()
    optimizer = Optimizer(domain)
    optimizer.solve()
    return optimizer.domain.to_json()


@app.route('/reset_solutions')
def reset_solutions():
    domain.num_iterations = 0
    domain.solutions = []
    domain.bad_solutions = []
    return optimizer.domain.to_json()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
