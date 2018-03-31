# Flask Server for Manaforged
from flask import Flask, render_template, url_for
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return  render_template('about.html')


@app.route('/try')
def try_it():
    return  render_template('try.html')


@app.route('/how')
def how():
    return  render_template('./how.html')

@app.route('/examples')
def examples():
    return  render_template('./examples.html')


#Handles cache busting
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    app.run(debug=True)
