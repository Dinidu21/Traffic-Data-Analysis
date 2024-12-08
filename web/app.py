from flask import Flask, render_template, request, redirect, url_for
import os

# Initialize the Flask application
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ensure the upload folder exists
def ensure_upload_folder_exists():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        print(f"Created new folder: {UPLOAD_FOLDER}")
    else:
        print(f"Using existing folder: {UPLOAD_FOLDER}")

ensure_upload_folder_exists()


# Route to render the form
@app.route('/')
def home():
    return render_template('form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        file = request.files['file']

        if file:
            ensure_upload_folder_exists()
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return redirect(url_for('home'))
        else:
            return "No file selected", 400

if __name__ == '__main__':
    app.run(debug=True)
