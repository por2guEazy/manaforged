# Flask Server for Manaforged
from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def render():
    return "Cooooool beans"

@app.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('%s.html' % page_name)
if __name__=='__main__':
    app.run()
