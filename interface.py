import json

import flask
from flask import Flask

from my_types import Solution
from optimizer import solution, domain

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return flask.render_template(
        'show.html',
        domain=domain,
        solution=solution,
        bounding_box=[
            min([p.x for p in domain.points]),
            min([p.y for p in domain.points]),
            max([p.x for p in domain.points]),
            max([p.y for p in domain.points])
        ]
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0')
