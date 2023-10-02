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


@app.route('/data')
def data():
    optimizer.solve()
    return domain.to_json()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
