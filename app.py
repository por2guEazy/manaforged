# Flask Server for Manaforged
import os
import tempfile

from flask import Flask, render_template, url_for, request, redirect, flash, send_file
from werkzeug.utils import secure_filename

import manaforged

UPLOAD_FOLDER = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = set(['pdf'])

print("HI")
print(UPLOAD_FOLDER)

app = Flask(__name__)
app.secret_key = 'kobe'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return  render_template('about.html')


@app.route('/try', methods=['GET', 'POST'])
def try_it():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

	if file.filename == '':
	    flash('No selected file')
	    return redirect(request.url)
	if file and allowed_file(file.filename):
	    flash('VAN DOWN BY THE RIVER')
	    filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            pdf_text = manaforged.pdf_to_text(file_path)
            print(manaforged.inflate(pdf_text))
            inflated = manaforged.inflate(pdf_text)
            document = manaforged.text_to_word_doc(inflated)
            word_doc_filename =  file_path + '-inflated.docx'
            document.save(word_doc_filename)
            return send_file(word_doc_filename) 	

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
