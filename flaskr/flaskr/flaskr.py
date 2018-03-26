# Flask Server for Manaforged
from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about/')
def about():
    return  render_template('./about.html')


@app.route('/try')
def try_it():
    return  render_template('./try.html')


@app.route('/how')
def how():
    return  render_template('./how.html')

@app.route('/examples')
def examples():
    return  render_template('./examples.html')

if __name__ == '__main__':
    app.run(debug=True)
