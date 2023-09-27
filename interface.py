import flask
from flask import Flask
from optimizer import solution

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return flask.render_template(
        'show.html',
        solution=solution,
        bounding_box=[
            min([p.x for p in solution.domain.points]),
            min([p.y for p in solution.domain.points]),
            max([p.x for p in solution.domain.points]),
            max([p.y for p in solution.domain.points])
        ]
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0')
