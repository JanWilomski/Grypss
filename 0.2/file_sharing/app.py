import os
import random
import string
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'supersecretkey'

def generate_unique_code(length=6):
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

codes = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            unique_code = generate_unique_code()
            while unique_code in codes:
                unique_code = generate_unique_code()
            filename = unique_code + "_" + file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            codes[unique_code] = filename
            flash(f'File uploaded successfully! Share this code: {unique_code}')
            return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        code = request.form['code']
        if code in codes:
            filename = codes[code]
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
        else:
            flash('Invalid code!')
            return redirect(url_for('download'))
    return render_template('download.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
